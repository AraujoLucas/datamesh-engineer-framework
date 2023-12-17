
import json
import boto3
import uuid
import datetime

def insert_into_dynamodb(data, table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    with table.batch_writer() as batch:
        for item in data:
            batch.put_item(Item=item)
            
            
def lambda_handler(event, context):
    start_time = datetime.datetime.now()
    print(f"Início da execução: {start_time}")
    print(f'event -> {event}')
    items_to_insert = []
    for record in event['Records']:
        sns_message_str = record['Sns']['Message']
        sns_message = json.loads(sns_message_str)
        data_product = sns_message.get('data_product', '')
        contract = sns_message.get('contract', '')
        key = sns_message.get('key', '')
        dt_get = sns_message.get('dt_get', '')
        request_data = sns_message.get('request', {}).get('data', [])[0] 
        response_data = sns_message.get('response', {}).get('data', [])[0]  
    
        tb = {
            'id': contract,
            **request_data,
            **response_data
        }
        print(f'payload {tb}')
        random_str = str(uuid.uuid4().hex)[:8]
        payload = {
            "bkt_key": f"bkt-name/layer/path_{random_str}",
            "tb_name": "tb_name",
            "date_ingestion": "2023-12-17-15:56:00",
            "partition": "20231217",
            "pf": "false",
            "status": "starting load",
            "data": tb
        }
        print(f'payload {payload}')
        items_to_insert.append(payload)
        
        try:
            
            table_name='ddb_ingestion'
    
            insert_into_dynamodb(items_to_insert, table_name)
            
            '''
            dynamodb = boto3.client('dynamodb')
            response = dynamodb.put_item(TableName='ddb_ingestion', Item=payload)
            '''
        except Exception as e:
            print('except: ', e)
            
    end_time = datetime.datetime.now()
    print(f"Término da execução: {end_time}")
            
    duration = end_time - start_time
    print(f"Duração da execução: {duration}")
    return {
        'statusCode': 200,
        'body': json.dumps(f'{duration} eventos publicados no dynamo!')
    }
