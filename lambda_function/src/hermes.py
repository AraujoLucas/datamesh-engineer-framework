'''
# Entity Class
class Hermes:
    def __init__(self, start_action):
            self.start_action = start_action
	        
    def execute_action(self):
            self.start_action.perform()
'''

# Entity Class
class Hermes:
    def __init__(self, start_action):
            self.start_action = start_action
	        
    def execute_action(self):
            self.start_action.perform()

    def execute_action(self):
 	    self.start_action.perform()
	    self.data = self.start_action.get_data()
						        
    def get_data(self):
        return self.data

