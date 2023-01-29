'''
# Collect Data Class
class CollectAction:
    def perform(self):
	print('Collecting data...')
'''

class CollectAction:
    
        def __init__(self, event):
	        self.event = event
		        self.data = None

 	def perform(self):
		import json
		self.data = json.loads(self.event['Records'][0]['Sns']['Message'])
	
	def get_data(self):
	        return self.data


