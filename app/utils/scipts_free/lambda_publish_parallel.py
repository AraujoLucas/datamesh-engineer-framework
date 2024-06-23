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

testes


import unittest
from unittest.mock import patch, MagicMock
import json
import boto3
from moto import mock_ssm, mock_logs, mock_sns
import time

from lambda_function import (
    load_config,
    get_log_group_names,
    start_log_query,
    get_query_results,
    extract_payload_data,
    publish_event,
    lambda_handler
)

# Teste para carregar as configurações
@patch("builtins.open", new_callable=unittest.mock.mock_open, read_data='{"parameter_name": "test-parameters", "query": "fields @timestamp, @message, statusCode | sort @timestamp desc | limit 20", "topic_arn": "arn:aws:sns:::topic_test_notification"}')
def test_load_config(mock_open):
    config = load_config()
    assert config['parameter_name'] == 'test-parameters'
    assert config['query'] == 'fields @timestamp, @message, statusCode | sort @timestamp desc | limit 20'
    assert config['topic_arn'] == 'arn:aws:sns:::topic_test_notification'

# Teste para recuperar nomes dos log groups
@mock_ssm
def test_get_log_group_names():
    ssm_client = boto3.client('ssm', region_name='us-east-1')
    ssm_client.put_parameter(
        Name='test-parameters',
        Value='log-group-1,log-group-2',
        Type='String'
    )
    parameter_name = 'test-parameters'
    log_group_names = get_log_group_names(parameter_name)
    assert log_group_names == ['log-group-1', 'log-group-2']

# Teste para iniciar consulta de logs
@mock_logs
def test_start_log_query():
    start_time = int((time.time() - 3600) * 1000)
    end_time = int(time.time() * 1000)
    query = "fields @timestamp, @message, statusCode | sort @timestamp desc | limit 20"
    log_group_name = 'log-group-1'
    
    query_id = start_log_query(log_group_name, query, start_time, end_time)
    assert query_id is not None

# Teste para obter resultados da consulta
@mock_logs
def test_get_query_results():
    query_id = "sample-query-id"
    
    def mock_get_query_results(queryId):
        if queryId == query_id:
            return {
                'status': 'Complete',
                'results': [
                    [{'field': '@timestamp', 'value': '12345'}, {'field': '@message', 'value': 'event input ingestion'}, {'field': 'statusCode', 'value': '200'}]
                ]
            }
    
    with patch('boto3.client') as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.get_query_results.side_effect = mock_get_query_results
        query_results = get_query_results(query_id)
        assert len(query_results) == 1

# Teste para extrair dados da payload
def test_extract_payload_data():
    query_results = [
        [{'field': '@timestamp', 'value': '12345'}, {'field': '@message', 'value': 'event input ingestion'}, {'field': 'statusCode', 'value': '200'}]
    ]
    status_code, event_input_ingestion = extract_payload_data(query_results)
    assert status_code == '200'
    assert event_input_ingestion == 'event input ingestion'

# Teste para publicar evento
@mock_sns
def test_publish_event():
    topic_arn = 'arn:aws:sns:::topic_test_notification'
    status_code = '200'
    event_input_ingestion = 'event input ingestion'

    response = publish_event(topic_arn, status_code, event_input_ingestion)
    assert 'MessageId' in response

# Teste para o handler do Lambda
@patch("lambda_function.load_config")
@patch("lambda_function.get_log_group_names")
@patch("lambda_function.start_log_query")
@patch("lambda_function.get_query_results")
@patch("lambda_function.publish_event")
def test_lambda_handler(mock_publish_event, mock_get_query_results, mock_start_log_query, mock_get_log_group_names, mock_load_config):
    mock_load_config.return_value = {
        'parameter_name': 'test-parameters',
        'query': 'fields @timestamp, @message, statusCode | sort @timestamp desc | limit 20',
        'topic_arn': 'arn:aws:sns:::topic_test_notification'
    }
    mock_get_log_group_names.return_value = ['log-group-1']
    mock_start_log_query.return_value = 'sample-query-id'
    mock_get_query_results.return_value = [
        [{'field': '@timestamp', 'value': '12345'}, {'field': '@message', 'value': 'event input ingestion'}, {'field': 'statusCode', 'value': '200'}]
    ]
    mock_publish_event.return_value = {'MessageId': 'sample-message-id'}

    event = {}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert 'Processamento concluido com sucesso' in json.loads(response['body'])['message']

# Executar todos os testes
if __name__ == '__main__':
    test_load_config()
    test_get_log_group_names()
    test_start_log_query()
    test_get_query_results()
    test_extract_payload_data()
    test_publish_event()
    test_lambda_handler()
    print("Todos os testes passaram com sucesso!")


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

