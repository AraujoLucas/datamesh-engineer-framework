import json
import boto3
import os

def get_partitions(glue_client, database, table):
    response = glue_client.get_partitions(
        DatabaseName=database,
        TableName=table
    )
    partitions = response['Partitions']
    return partitions

def fetch_partitions(tables):
    partitions_by_table = {}
    glue_client = boto3.client('glue',
                               aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                               aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

    for table_info in tables.get('tables_details', []):
        database = table_info.get('database')
        table = table_info.get('table')

        try:
            current_partitions = get_partitions(glue_client, database=database, table=table)

            if table not in partitions_by_table:
                partitions_by_table[table] = []
            partitions_by_table[table].extend(current_partitions)
        except Exception as e:
            print(f"Erro ao obter partições para a tabela {table} no banco de dados {database}: {e}\n")

    return partitions_by_table

def upload_json_to_s3(json_data, bucket, key):
    s3_client = boto3.client('s3',
                             aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                             aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

    response = s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=json_data
    )
    print(f"Arquivo JSON enviado para o S3 com sucesso. Objeto criado: {response['ResponseMetadata']['HTTPHeaders']['x-amz-id-2']}")

def main():
    tables = {
        "tables_details": [
            {"database": "db1", "table": "tb_teste_post_sns_v2", "partition": "anomesdia"},
            {"database": "db1", "table": "tb_study_quality_output", "partition": "anomesdia"},
            {"database": "db1", "table": "tb_data_input_study_quality", "partition": "anomesdia"}
        ]
    }

    print(f"List input verify {tables}\n")

    partitions_by_table = fetch_partitions(tables)

    print("Partições encontradas:\n")
    for table, partitions in partitions_by_table.items():
        print(f"Partições para a tabela '{table}':")
        for partition in partitions:
            print(partition['Values'])

    # Converta as partições para JSON
    json_data = json.dumps(partitions_by_table)

    # Faça upload do JSON para o Amazon S3
    bucket_name = 'seu-bucket-s3'
    object_key = 'partitions.json'
    upload_json_to_s3(json_data, bucket_name, object_key)

if __name__ == "__main__":
    main()
