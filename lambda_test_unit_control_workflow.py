import unittest
from unittest import TestCase
from moto import mock_dynamodb2
import boto3
from your_module import extract_params, get_item_ddb, update_item_ddb, insert_item_ddb

class TestYourFunctions(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dynamodb_client = boto3.client('dynamodb')

    @mock_dynamodb2
    def test_extract_params(self):
        # Setup
        record_kafka = {'detail': {'tableName': 'test_table', 'changedPartitions': ['partition_value']}}

        # Test
        table_name, changed_partitions = extract_params(record_kafka)

        # Assert
        self.assertEqual(table_name, 'test_table')
        self.assertEqual(changed_partitions, 'partition_value')

    @mock_dynamodb2
    def test_get_item_ddb_item_exists(self):
        # Setup
        ddb_control = 'ddb_control_ingestion'
        changed_partitions = 'partition_value'
        self.dynamodb_client.create_table(
            TableName=ddb_control,
            KeySchema=[{'AttributeName': 'PartitionKey', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'PartitionKey', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        self.dynamodb_client.put_item(
            TableName=ddb_control,
            Item={'PartitionKey': {'S': changed_partitions}}
        )

        # Test
        item_exists = get_item_ddb(self.dynamodb_client, ddb_control, changed_partitions)

        # Assert
        self.assertTrue(item_exists)

    @mock_dynamodb2
    def test_get_item_ddb_item_not_exists(self):
        # Setup
        ddb_control = 'ddb_control_ingestion'
        changed_partitions = 'non_existing_partition'

        # Test
        item_exists = get_item_ddb(self.dynamodb_client, ddb_control, changed_partitions)

        # Assert
        self.assertFalse(item_exists)

    @mock_dynamodb2
    def test_update_item_ddb(self):
        # Setup
        ddb_control = 'ddb_control_ingestion'
        changed_partitions = 'partition_value'
        table_name = 'test_table'
        self.dynamodb_client.create_table(
            TableName=ddb_control,
            KeySchema=[{'AttributeName': 'PartitionKey', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'PartitionKey', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        self.dynamodb_client.put_item(
            TableName=ddb_control,
            Item={'PartitionKey': {'S': changed_partitions}}
        )

        # Test
        status = update_item_ddb(self.dynamodb_client, ddb_control, changed_partitions, table_name)

        # Assert
        self.assertEqual(status, 200)

    @mock_dynamodb2
    def test_insert_item_ddb(self):
        # Setup
        ddb_control = 'ddb_control_ingestion'
        changed_partitions = 'partition_value'
        table_name = 'test_table'
        self.dynamodb_client.create_table(
            TableName=ddb_control,
            KeySchema=[{'AttributeName': 'PartitionKey', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'PartitionKey', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )

        # Test
        status = insert_item_ddb(self.dynamodb_client, ddb_control, changed_partitions, table_name)

        # Assert
        self.assertEqual(status, 200)

if __name__ == '__main__':
    unittest.main()
