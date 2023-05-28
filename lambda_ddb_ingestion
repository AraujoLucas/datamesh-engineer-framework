import json
import boto3

def lambda_handler(event, context):
    data_dict = {
    'Records': [
                {
                    "Sns": {
                        "Message": {
                            "data_product": "v1",
                            "contract": "10",
                            "key": "get/domain_xxx",
                            "data": {
                                "default": {
                                    "dt_get": "28-05-2023 19:01:47",
                                    "request": "{\"data\":[{\"key_rr_1\":\"xxx\",\"key_rr_2\":\"yy\"}]}",
                                    "response": "{\"data\":[{\"key_rp_1\":\"zzz\",\"key_rp_2\":\"kkk\"}]}"
                                }
                            }
                        }
                    }
                }
            ]
    }
    
    for record in data_dict['Records']:
        sns_message = record['Sns']['Message']
    
        data_product = sns_message.get('data_product', '')
        contract = sns_message.get('contract', '')
        key = sns_message.get('key', '')
        dt_get = sns_message['data']['default'].get('dt_get', '')
        request_data = json.loads(sns_message['data']['default'].get('request', ''))
        response_data = json.loads(sns_message['data']['default'].get('response', ''))
     
        tb = {
            'id': contract,
            **request_data,
            **response_data
        }
        print(f'payload {tb}')
    
        # Payload de entrada para o DynamoDB
        payload = {
            "bkt_key": {"S": "bkt-name/layer/path"},
            "tb_name": {"S": "tb_name"},
            "date_ingestion": {"S": "2023-1-29-14:27:00"},
            "partition": {"S": "20230528"},
            "pf": {"S": "false"},
            "status": {"S": "starting load"},
            "data": {"S": json.dumps(tb)}
        }
    
        print(f'payload {payload}')
        
        try:
            dynamodb = boto3.client('dynamodb')
            response = dynamodb.put_item(TableName='tb_load', Item=payload)
        except Exception as e:
            print('except: ', e)
            
        return response
