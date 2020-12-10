import json

from condition import Condition
from consequence import Consequence


class RuleList:
    rules = []
    def __init__(self, file="rules.json", model_object=None):
        with open(file) as f:
            json_file = json.load(f)

        for rule_json in json_file.get('rules'):
            self.rules.append(Rule(rule_json, model_object))

class Rule:
    def __init__(self, rule_json, model_object):
        self.name = rule_json.get('name')
        self.conditions = []
        self.consequences = []

        for conditions_json in rule_json.get('conditions'):
            attribute_json = conditions_json.get('attribute')
            self.conditions.append(Condition(attribute_json, model_object))

        for consequence_json in rule_json.get('consequences'):
            self.consequences.append(Consequence(consequence_json, model_object))

RuleList()
