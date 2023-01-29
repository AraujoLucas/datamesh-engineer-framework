'''
# main.py
import json
from src.hermes import Hermes
from src.actions.collect import CollectAction
from src.actions.serialize import SerializeAction
from src.actions.load import LoadAction

def lambda_handler(event, context):

    print('Running')
        ingestion = Hermes(CollectAction())
	ingestion.execute_action()

	serialize_in_avro = Hermes(SerializeAction())
	serialize_in_avro.execute_action()

	load_in_s3 = Hermes(LoadAction())
	load_in_s3.execute_action()

    return print('build to component')
'''

from src.hermes import Hermes
from src.actions.collect import CollectAction
from src.actions.serialize import SerializeAction
from src.actions.load import LoadAction
from datetime import datetime

now = datetime.now()
date_process = "%s%02d%s" % (now.year, now.month,now.day)

def lambda_handler(event, context):
	print(f'{datetime.now()} - Collecting SNS data {event}')
	ingestion = Hermes(CollectAction(event))
	ingestion.execute_action()
	data = ingestion.get_data()
	print(f'{datetime.now()} - data generated from backend <app-x>  - {data}')
						        
        '''
	serialize_in_avro = Hermes(SerializeAction(data))
	serialize_in_avro.execute_action()
	 '''
									    
	print(f'{datetime.now()} - initial loaded into data mesh')
	load_in_s3 = Hermes(LoadAction(data))
	load_in_s3.execute_action()
	print(f'{datetime.now()} - data loaded successfully into data mesh')
		        
	return {
	'statusCode': 200,
	'body': json.dumps('Hello from Lambda!')
	}
														        }
