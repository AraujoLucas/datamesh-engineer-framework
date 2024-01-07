# dynamodb model
'''
{
  "PartitionKey": {
    "S": ""
  }
}
'''

import json
import boto3

dynamodb_client = boto3.client('dynamodb')

def extract_params(record_kafka):        
    table_name = record_kafka['detail']['tableName']
    changed_partitions = record_kafka['detail']['changedPartitions'][0]

    print(f'> table name: {table_name}')
    print(f'> partition value: {changed_partitions}')

    return table_name, changed_partitions

def get_item_ddb(dynamodb_client,ddb_control,changed_partitions):
    response = dynamodb_client.get_item(
            TableName= ddb_control,
            Key={"PartitionKey": {"S": changed_partitions}}
        )
    item_exists = 'Item' in response
    print(f'> Item is {item_exists}')
    return item_exists
    
def insert_ddb(dynamodb_client,ddb_control,item_exists,changed_partitions,table_name):
    
    if item_exists:
        # realizar update no item existente adicionando nova tb e pt disponivel para ETL
        print(f'> update the existing key {changed_partitions} adding new table {table_name} and partition available')
        
        updated_second_table_name = f"{table_name}"
        updated_status_trigger = 'start ETL'
        update_expression = 'SET #partition_status = :partition_status, #table_2 = :updated_table, #trigger = :trigger'
        expression_attribute_names = {'#partition_status': 'table_2_partitionStatus', '#table_2': 'table_2', '#trigger': 'trigger'}
        expression_attribute_values = {
                    ':partition_status': {'S': 'disponivel'},
                    ':updated_table': {'S': updated_second_table_name},
                    ':trigger': {'S': updated_status_trigger}
                }
        
        update_item = dynamodb_client.update_item(
                TableName= ddb_control,
                Key={"PartitionKey": {"S": changed_partitions}},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values
            )
        status = update_item['ResponseMetadata']['HTTPStatusCode']
        print(f'> status code for update_item in ddb: {status} ')
        
    else:
        print(f'> the item does not exist in ddb, executing the insert task: {changed_partitions}')
        dynamodb_payload = {
            "TableName": "ddb_control_ingestion",
            "Item": {
                "PartitionKey": {"S": changed_partitions},
                "table_1": {"S": table_name},
                "table_1_partitionStatus": {"S": "disponivel"}
            }
        }
        response_put_item = dynamodb_client.put_item(**dynamodb_payload)
        status = response_put_item['ResponseMetadata']['HTTPStatusCode']
        print(f'> status code for put_item in ddb: {status} ')
        
    return 0

def lambda_handler(event, context):
    record_kafka=event
    ddb_control = 'name_ddb_control_workflow'
    
    print(f'::: running task extract params for job :::')
    table_name, changed_partitions = extract_params(record_kafka)
    
    print(f'::: running task if item already exists :::')
    item_exists = get_item_ddb(dynamodb_client,ddb_control,changed_partitions)
    
    print(f'::: running task insert in ddb :::')
    insert_ddb(dynamodb_client,ddb_control,item_exists,changed_partitions,table_name)

    return print('::: Processing executed successfully! :::')
    
