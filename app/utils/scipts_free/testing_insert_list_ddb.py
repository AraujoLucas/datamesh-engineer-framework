import unittest
from unittest.mock import patch, Mock
from lambda_function import lambda_handler, read_s3_file, insert_into_dynamodb

class TestLambdaFunction(unittest.TestCase):
    @patch('boto3.client')
    @patch('boto3.resource')
    def test_read_s3_file(self, mock_resource, mock_client):
        # Simule os retornos do S3
        s3_response = {
            'Body': Mock()
        }
        s3_client = mock_client.return_value
        s3_client.get_object.return_value = s3_response

        # Dados fictícios
        event = {
            'Records': [
                {
                    'Sns': {
                        'Message': 'Seu evento S3 aqui'
                    }
                }
            ]
        }

        # Chame a função da lambda
        context = None
        lambda_handler(event, context)

        # Verifique se a função lambda fez a leitura do S3 corretamente
        s3_client.get_object.assert_called_once_with(Bucket='seu_bucket', Key='seu_arquivo')
        # Faça as asserções necessárias para verificar os dados lidos

    @patch('boto3.client')
    @patch('boto3.resource')
    def test_insert_into_dynamodb(self, mock_resource, mock_client):
        # Simule os retornos do DynamoDB
        dynamodb = mock_resource.return_value
        table = dynamodb.Table.return_value

        # Dados fictícios
        data = [
            {
                'col1': 'valor1',
                'col2': 'valor2',
                # Adicione outros campos aqui
            }
        ]

        # Chame a função de inserção no DynamoDB
        table_name = 'NomeDaSuaTabelaDynamoDB'
        insert_into_dynamodb(data, table_name)

        # Verifique se a função inseriu os itens no DynamoDB corretamente
        table.batch_writer.assert_called_once()
        # Faça as asserções necessárias para verificar os itens inseridos

if __name__ == '__main__':
    unittest.main()
