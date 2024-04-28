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

def extract_params(record_kafka):
    table_name = record_kafka['detail']['tableName']
    changed_partitions = record_kafka['detail']['changedPartitions'][0]
    return table_name, changed_partitions

def get_item_ddb(dynamodb_client, ddb_control, changed_partitions):
    try:
        response = dynamodb_client.get_item(
            TableName=ddb_control,
            Key={"PartitionKey": {"S": changed_partitions}}
        )
        return 'Item' in response
    except Exception as e:
        print(f'Error in get_item_ddb: {e}')
        return False

def update_item_ddb(dynamodb_client, ddb_control, changed_partitions, table_name):
    updated_second_table_name = f"{table_name}"
    updated_status_trigger = 'start ETL'
    update_expression = 'SET #partition_status = :partition_status, #table_2 = :updated_table, #trigger = :trigger'
    expression_attribute_names = {'#partition_status': 'table_2_partitionStatus', '#table_2': 'table_2', '#trigger': 'trigger'}
    expression_attribute_values = {
        ':partition_status': {'S': 'disponivel'},
        ':updated_table': {'S': updated_second_table_name},
        ':trigger': {'S': updated_status_trigger}
    }

    try:
        update_item = dynamodb_client.update_item(
            TableName=ddb_control,
            Key={"PartitionKey": {"S": changed_partitions}},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )
        return update_item['ResponseMetadata']['HTTPStatusCode']
    except Exception as e:
        print(f'Error in update_item_ddb: {e}')
        return None

def insert_item_ddb(dynamodb_client, ddb_control, changed_partitions, table_name):
    dynamodb_payload = {
        "TableName": ddb_control,
        "Item": {
            "PartitionKey": {"S": changed_partitions},
            "table_1": {"S": table_name},
            "table_1_partitionStatus": {"S": "disponivel"}
        }
    }

    try:
        response_put_item = dynamodb_client.put_item(**dynamodb_payload)
        return response_put_item['ResponseMetadata']['HTTPStatusCode']
    except Exception as e:
        print(f'Error in insert_item_ddb: {e}')
        return None

def lambda_handler(event, context):
    dynamodb_client = boto3.client('dynamodb')
    record_kafka = event
    ddb_control = 'ddb_control_ingestion'

    print('::: Running task extract params for job :::')
    table_name, changed_partitions = extract_params(record_kafka)

    print('::: Running task if item already exists :::')
    item_exists = get_item_ddb(dynamodb_client, ddb_control, changed_partitions)

    print('::: Running task insert/update in DynamoDB :::')
    if item_exists:
        status = update_item_ddb(dynamodb_client, ddb_control, changed_partitions, table_name)
    else:
        status = insert_item_ddb(dynamodb_client, ddb_control, changed_partitions, table_name)

    if status is not None:
        print(f'::: Processing executed successfully Status Code: {status}')
    else:
        print('::: Processing failed!')

    
