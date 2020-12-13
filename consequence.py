class Consequence:
    def __init__(self, consequence_json):
        self.method = consequence_json.get('method')
        self.arguments = consequence_json.get('args')

    def apply(self, model_object):
        method = getattr(model_object,self.method)
        method(*self.arguments)