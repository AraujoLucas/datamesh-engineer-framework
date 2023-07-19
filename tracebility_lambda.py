# ingestion
import uuid
import logging
import boto3
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

lambda_client = boto3.client('lambda')
sns_client = boto3.client('sns')
sns_topic_arn = '<ARN do tópico SNS>'

def lambda_handler(event, context):
    try:
        # Gerar um identificador único
        execution_id = str(uuid.uuid4())

        # Incluir o identificador único no payload do evento
        event['execution_id'] = execution_id

        # Registrar informações relevantes nos logs
        logger.info(f"Lambda A - Execution ID: {execution_id}")
        
        logger.info(f"Invokation Lambda Persist")        
        # Chamar o Lambda B
        response = lambda_client.invoke(
            FunctionName='persist',
            InvocationType='RequestResponse',
            Payload=bytes(json.dumps(event), 'utf-8')
        )
        result = response['ResponseMetadata']["HTTPStatusCode"]
        if result == 200:
            logger.info(f"Invokation is success HTTPStatusCode:{result}!!! ") 
        
    except Exception as e:
        # Registrar o erro nos logs
        logger.error(f"response Invokation error: {str(e)}")
        
        raise

# persist
import logging
import boto3
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

lambda_client = boto3.client('lambda')
sns_client = boto3.client('sns')
sns_topic_arn = '<ARN do tópico SNS>'

def lambda_handler(event, context):
    
    print(f"event input ingestion {event}")
    try:
        # Extrair o identificador único do evento
        execution_id = event['execution_id']

        # Registrar informações relevantes nos logs
        logger.info(f"Lambda B - Execution ID: {execution_id}")
        
        logger.info(f"Invokation Lambda Catalog") 
        # Chamar o Lambda C
        response = lambda_client.invoke(
            FunctionName='catalog',
            InvocationType='RequestResponse',
            Payload=bytes(json.dumps(event), 'utf-8')
        )
        result = response['ResponseMetadata']["HTTPStatusCode"]
        if result == 200:
            logger.info(f"Invokation is success HTTPStatusCode:{result}!!! ") 
        
    except Exception as e:
        # Registrar o erro nos logs
        logger.error(f"response Invokation error: {str(e)}")
      
# catalog
import logging
import boto3
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns_client = boto3.client('sns')
sns_topic_arn = '<ARN do tópico SNS>'

def lambda_handler(event, context):
    print(f"event input ingestion {event}")
    try:
        # Extrair o identificador único do evento
        execution_id = event['execution_id']

        # Registrar informações relevantes nos logs
        logger.info(f"Lambda C - Execution ID: {execution_id}")

        return {
            'statusCode': 200,
            'body': 'Lambda C executed successfully'
        }
    except Exception as e:
        # Registrar o erro nos logs
        logger.error(f"Lambda C - Error: {str(e)}")

        raise
