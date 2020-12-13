class Condition:
    def __init__(self, attribute_json):
        name = attribute_json.get('name')
        operator = attribute_json.get('operator')
        value = attribute_json.get('value')
        self.attribute = Attribute(name, operator, value)

    def evaluate(self, model_object):
        return self.attribute.evaluate(model_object)


class Attribute:
    def __init__(self, name, operator, value):
        self.name = name
        self.operator = operator
        self.value = value

    def evaluate(self, model_object):
        object_attr = getattr(model_object,self.name)
        if self.operator == 'eq':
            return object_attr == self.value
        elif self.operator == 'neq':
            return object_attr != self.value

        raise Exception("Not Supported")

