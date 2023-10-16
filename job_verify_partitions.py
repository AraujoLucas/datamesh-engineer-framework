import sys
import boto3
import logging

glue_client = boto3.client('glue')

db = 'db'
tb = 'tb'

partition_values_to_check = ['string']

def check_partition_existence(partition_values):
    try:
        response = glue_client.get_partition(
            DatabaseName=db,
            TableName=tb,
            PartitionValues=partition_values
        )
        return response['Partition']['Values']
    except glue_client.exceptions.EntityNotFoundException:
        return None

for partition_values in partition_values_to_check:
    result = check_partition_existence([partition_values])
    if result:
        print(f"Partition '{partition_values}' exists.")
        print("=" * 50)
    else:
        print(f"Partition '{partition_values}' does not exist.")
        print("=" * 50)
