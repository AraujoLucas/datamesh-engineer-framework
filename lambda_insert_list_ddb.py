import json
import boto3
import pandas as pd
from botocore.exceptions import NoCredentialsError

def read_s3_file(bucket_name, file_key):
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        xls_data = pd.read_excel(response['Body'])
        return xls_data.to_dict(orient='records')
    except NoCredentialsError:
        return None

def insert_into_dynamodb(data, table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    with table.batch_writer() as batch:
        for item in data:
            batch.put_item(Item=item)

def lambda_handler(event, context):
    for record in event['Records']:
        s3_event = json.loads(record['Sns']['Message'])
        bucket_name = s3_event['Records'][0]['s3']['bucket']['name']
        file_key = s3_event['Records'][0]['s3']['object']['key']
        table_name = 'NomeDaSuaTabelaDynamoDB'
        xls_data = read_s3_file(bucket_name, file_key)
        if xls_data is not None:
            insert_into_dynamodb(xls_data, table_name)
    
    return {
        'statusCode': 200,
        'body': 'Itens inseridos no DynamoDB.'
    }
