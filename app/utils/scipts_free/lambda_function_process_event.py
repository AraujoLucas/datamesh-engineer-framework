Lambda ler eventos do dynamo

import boto3

dynamodb_streams = boto3.client('dynamodbstreams')
stream_arn = 'arn:aws:dynamodb:region:account-id:table/ExampleTable/stream/2020-07-09T20:34:56.123'

# Executa um loop infinito para ler eventos do stream
while True:
    # Realiza uma chamada para o método `get_records` para ler os eventos do stream
    response = dynamodb_streams.get_records(StreamArn=stream_arn, Limit=100)
    
    for record in response['Records']:
        print(record)
