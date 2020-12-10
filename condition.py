class Condition:
    def __init__(self, attribute_json, model_object):
        name = attribute_json.get('name')
        operator = attribute_json.get('operator')
        value = attribute_json.get('value')
        self.attribute = Attribute(name, operator, value)
        self.model_object = model_object


class Attribute:
    def __init__(self, name, operator, value):
        self.name = name
        self.operator = operator
        self.value = value
