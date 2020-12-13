import json

from condition import Condition
from consequence import Consequence


class RuleList:
    rules = []

    def __init__(self, file="rules.json"):
        with open(file) as f:
            json_file = json.load(f)

        for rule_json in json_file.get('rules'):
            self.rules.append(Rule(rule_json))


class Rule:
    def __init__(self, rule_json):
        self.name = rule_json.get('name')
        self.conditions = []
        self.consequences = []

        for conditions_json in rule_json.get('conditions'):
            attribute_json = conditions_json.get('attribute')
            self.conditions.append(Condition(attribute_json))

        for consequence_json in rule_json.get('consequences'):
            self.consequences.append(Consequence(consequence_json))

