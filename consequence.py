class Consequence:
    def __init__(self, consequence_json, model_object):
        self.method = consequence_json.get('method')
        self.arguments = consequence_json.get('args')
        self.model_object = model_object
