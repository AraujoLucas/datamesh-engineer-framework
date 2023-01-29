'''
# Serialize Data Class
class SerializeAction:
    def perform(self):
        print('Serializing data...')
'''

class SerializeAction:
    def __init__(self, data):
            self.data = data
            self.serialized_data = None
            self.schema = avro.schema.Parse(open("schema.avsc", "rb").read().decode('utf-8'))
			        
    def perform(self):
            print(f'Serializing data... {self.data}')
            writer = DataFileWriter(open("data.avro", "wb"), DatumWriter(), self.schema)
            writer.append(self.data)
            writer.close()
            with open("data.avro", "rb") as f:
            self.serialized_data = f.read()
				        
    def get_serialized_data(self):
            return self.serialized_data


