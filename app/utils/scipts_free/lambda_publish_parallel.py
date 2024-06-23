import json
import boto3
from concurrent.futures import ThreadPoolExecutor

def publish_event(payload, topic_arn):
    sns_client = boto3.client('sns')

    for event_data in payload['data']:
        message = {
            'data_product': payload['data_product'],
            'contract': payload['contract'],
            'key': payload['key'],
            'event_data': event_data
        }
        message.update(payload['data'])

    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=json.dumps(message),
        Subject='event_teste'
    )

    print(f"Evento publicado com sucesso: {response['MessageId']}")
    

def lambda_handler(event, context):
    payload = {
        "data_product": "v1",
        "contract": "10",
        "key": "get/domain_xxx",
        "data": {
            "dt_get": "28-05-2023 19:01:47",
            "request": {"data":[{"key_rr_1":"xxx","key_rr_2":"yy"}]},
            "response": {"data":[{"key_rp_1":"zzz","key_rp_2":"kkk"}]}
        }
    }

    topic_arn = 'arn:aws:sns:regio:account-id:topic_test_notification'
    num_parallel_publish = 50 

    with ThreadPoolExecutor(max_workers=num_parallel_publish) as executor:
        print(payload)
        futures = [executor.submit(publish_event, payload, topic_arn) for _ in range(num_parallel_publish)]
        for future in futures:
            future.result()

    return {
        'statusCode': 200,
        'body': json.dumps(f'{num_parallel_publish} eventos publicados em paralelo com sucesso!')
    }

____________________________________________________________________________________________________

import json
import boto3
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carrega as configurações do arquivo config.json
def load_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config

def get_log_group_names(parameter_name):
    """Recupera os nomes dos log groups do Parameter Store."""
    logger.info('Recuperando o nome dos log groups do Parameter Store')
    ssm_client = boto3.client('ssm')
    try:
        response = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
        return response['Parameter']['Value'].split(',')
    except Exception as e:
        logger.error(f"Erro ao recuperar o parâmetro: {str(e)}")
        raise

def start_log_query(log_group_name, query, start_time, end_time):
    """Inicia a consulta de logs no CloudWatch."""
    logger.info(f'Iniciando consulta de logs para {log_group_name}')
    logs_client = boto3.client('logs')
    try:
        start_query_response = logs_client.start_query(
            logGroupName=log_group_name.strip(),
            startTime=start_time,
            endTime=end_time,
            queryString=query,
        )
        return start_query_response['queryId']
    except Exception as e:
        logger.error(f"Erro ao iniciar a consulta de logs para {log_group_name}: {str(e)}")
        raise

def get_query_results(query_id):
    """Obtém os resultados da consulta de logs."""
    logger.info('Obtendo resultados da consulta de logs')
    logs_client = boto3.client('logs')
    try:
        response = None
        while response is None or response['status'] == 'Running':
            time.sleep(0.5)  # Reduzido o tempo de espera
            response = logs_client.get_query_results(queryId=query_id)
        return response['results']
    except Exception as e:
        logger.error(f"Erro ao obter os resultados da consulta: {str(e)}")
        raise

def extract_payload_data(query_results):
    """Extrai statusCode e @message dos resultados da consulta."""
    logger.info('Extraindo statusCode e @message dos resultados da consulta')
    status_code = None
    event_input_ingestion = None

    for result in query_results:
        log_entry = {field['field']: field['value'] for field in result}
        
        status_code = log_entry.get('statusCode', None)
        
        message = log_entry.get('@message', None)
        if message and 'event input ingestion' in message:
            event_input_ingestion = message

    return status_code, event_input_ingestion

def publish_event(topic_arn, status_code, event_input_ingestion):
    """Publica msg no sns target"""
    logger.info('Publicando mensagem no SNS')
    sns_client = boto3.client('sns')
    
    payload = {
        "data_product": "v1",
        "contract": "10",
        "key": "get/domain_xxx",
        "status_response": status_code,
        "data": {
            "dt_get": time.strftime('%d-%m-%Y %H:%M:%S', time.localtime()),
            "request": {"data": [{"key_rr_1": event_input_ingestion}]},
            "response": {"data": [{"key_rp_1": "zzz", "key_rp_2": "kkk"}]}
        }
    }

    for event_data in payload['data']:
        message = {
            'data_product': payload['data_product'],
            'contract': payload['contract'],
            'key': payload['key'],
            'status_response': payload['status_response'],
            'event_data': event_data
        }
        message.update(payload['data'])
    
    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=json.dumps(message),
            Subject='event_teste'
        )
        logger.info(f"Evento publicado com sucesso: {response['MessageId']}")
    except Exception as e:
        logger.error(f"Erro ao publicar evento no SNS: {str(e)}")
        raise

def lambda_handler(event, context):
    """Função principal do Lambda."""
    logger.info('Iniciando execução da função lambda')
    
    try:
        config = load_config()
        parameter_name = config['parameter_name']
        query = config['query']
        topic_arn = config['topic_arn']
        
        start_time = int((time.time() - 3600) * 1000)  # Uma hora atrás
        end_time = int(time.time() * 1000)
        
        log_group_names = get_log_group_names(parameter_name)
        logger.info(f'Log group names: {log_group_names}')
        
        for log_group_name in log_group_names:
            query_id = start_log_query(log_group_name, query, start_time, end_time)
            query_results = get_query_results(query_id)
            logger.info(f'Query ID -> {query_id}')
    
            status_code, event_input_ingestion = extract_payload_data(query_results)
            
            publish_event(topic_arn, status_code, event_input_ingestion)
    
        logger.info('Processamento concluído com sucesso')
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Processamento concluido com sucesso'})
        }
    except Exception as e:
        logger.error(f'Erro durante a execução da lambda: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }



'''
import json
import boto3
import time

def get_log_group_names(parameter_name):
    """Recupera os nomes dos log groups do Parameter Store."""
    print(f'::: Recupera o nome do log group do Parameter Store :::')
    ssm_client = boto3.client('ssm')
    try:
        response = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
        return response['Parameter']['Value'].split(',')
    except Exception as e:
        raise Exception(f"Erro ao recuperar o parâmetro: {str(e)}")

def start_log_query(log_group_name, query, start_time, end_time):
    """Inicia a consulta de logs no CloudWatch."""
    print(f'::: Inicia a consulta de logs {log_group_name} :::')
    logs_client = boto3.client('logs')
    try:
        start_query_response = logs_client.start_query(
            logGroupName=log_group_name.strip(),
            startTime=start_time,
            endTime=end_time,
            queryString=query,
        )
        return start_query_response['queryId']
    except Exception as e:
        raise Exception(f"Erro ao iniciar a consulta de logs para {log_group_name}: {str(e)}")

def get_query_results(query_id):
    """Obtém os resultados da consulta de logs."""
    print(f'::: Obtém os resultados da consulta de logs :::')
    logs_client = boto3.client('logs')
    try:
        response = None
        while response is None or response['status'] == 'Running':
            time.sleep(0.5)  # Reduzido o tempo de espera
            response = logs_client.get_query_results(queryId=query_id)
        return response['results']
    except Exception as e:
        raise Exception(f"Erro ao obter os resultados da consulta: {str(e)}")

def extract_payload_data(query_results):
    """Extrai statusCode e @message dos resultados da consulta."""
    print(f'::: Extrai statusCode e @message dos resultados da consulta :::')
    status_code = None
    event_input_ingestion = None

    for result in query_results:
        log_entry = {field['field']: field['value'] for field in result}
        
        status_code = log_entry.get('statusCode', None)
        
        message = log_entry.get('@message', None)
        if message and 'event input ingestion' in message:
            event_input_ingestion = message

    return status_code, event_input_ingestion

def publish_event(topic_arn,status_code,event_input_ingestion):
    """Publica msg no sns target"""
    print(f'::: Publica msg no sns target :::')
    sns_client = boto3.client('sns')
    
    payload = {
                "data_product": "v1",
                "contract": "10",
                "key": "get/domain_xxx",
                "status_response": status_code,
                "data": {
                    "dt_get": time.strftime('%d-%m-%Y %H:%M:%S', time.localtime()),
                    "request": {"data": [{"key_rr_1": event_input_ingestion}]},
                    "response": {"data": [{"key_rp_1": "zzz", "key_rp_2": "kkk"}]}
                }
            }

    for event_data in payload['data']:
        message = {
            'data_product': payload['data_product'],
            'contract': payload['contract'],
            'key': payload['key'],
            'status_response': payload['status_response'],
            'event_data': event_data
        }
        message.update(payload['data'])
    
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=json.dumps(message),
        Subject='event_teste'
    )

    return print(f"Evento publicado com sucesso: {response['MessageId']}")

def lambda_handler(event, context):
    """Função principal do Lambda."""
    print(f'::: Start extraction :::')
    parameter_name = 'test-parameters'
    query = """
    fields @timestamp, @message, statusCode
    | sort @timestamp desc
    | limit 20
    """
    
    start_time = int((time.time() - 3600) * 1000)  # Uma hora atrás
    end_time = int(time.time() * 1000)
    
    try:
        log_group_names = get_log_group_names(parameter_name)
        print(f'Log group names: {log_group_names}')
        
        for log_group_name in log_group_names:
            query_id = start_log_query(
                log_group_name, query, start_time, end_time)
            
            query_results = get_query_results(query_id)
            print(f'query_id -> {query_id}')
    
            status_code, event_input_ingestion = extract_payload_data(query_results)
            
            topic_arn = 'arn:aws:sns:us-east-1:587791419323:topic_test_notification'
            response_publish = publish_event(
                topic_arn,status_code,event_input_ingestion)
            print(f'response_publish -> {response_publish}')
    
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Processamento concluido com sucesso'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
'''

