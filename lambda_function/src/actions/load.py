'''
# Load Data Class
class LoadAction:
    def perform(self):
        print('Loading data...')
'''


class LoadAction:
    def __init__(self, serialized_data):
            self.serialized_data = serialized_data
            print('import boto')
            import boto3
            self.s3 = boto3.client('s3')
            print(f'client {self.s3}')
					            
    def perform(self):
	    print(f'Loading data into sor... {self.serialized_data}')
	    self.s3.put_object(Bucket='s3://s3-bktkey', Key='sor/tb_xpto_layer/data.avro', Body=self.serialized_data)


