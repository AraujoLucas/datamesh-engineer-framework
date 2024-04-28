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
