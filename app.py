import sys, csv

from intellect.Intellect import Intellect
from enum import Enum

from rule_list import RuleList


class Time(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Budget(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Appetite(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Skill(Enum):
    AMATEUR = 1
    PROFESSIONAL = 2


class Food(object):
    def __init__(self, saciety, cost, nutritional_value, difficulty, time):
        self.saciety = saciety
        self.cost = cost
        self.nutritional_value = nutritional_value
        self.difficulty = difficulty
        self.time = time
        self.points = 0

    def __str__(self):
        #return "Points {}, name {}".format(str(self.points), type(self).__name__)
        return str(type(self).__name__)


class Omellette(Food):
    def __init__(self):
        super(Omellette, self).__init__(3, 4, 5, 3, 1)


class Pollo(Food):
    def __init__(self):
        super(Pollo, self).__init__(2, 3, 4, 2, 4)


class Milanesa(Food):
    def __init__(self):
        super(Milanesa, self).__init__(1, 3, 2, 3, 2)


class Noquis(Food):
    def __init__(self):
        super(Noquis, self).__init__(5, 2, 2, 5, 3)


class Tarta(Food):
    def __init__(self):
        super(Tarta, self).__init__(3, 3, 5, 5, 3)


class Model(object):
    def __init__(self, time=None, budget=None, appetite=None, skill=None):
        self._time = time
        self._budget = budget
        self._appetite = appetite
        self._skill = skill
        self._proposals = [Omellette(), Pollo(), Milanesa(), Noquis(), Tarta()]

    def evaluate_time_points(self, time):
        time = Time(time)
        for proposal in self._proposals:
            if time == Time.LOW:
                if proposal.time in [1]:
                    proposal.points += 10
                elif proposal.time in [2, 3]:
                    proposal.points += 5

            if time == Time.MEDIUM:
                if proposal.time in [4, 2]:
                    proposal.points += 5
                elif proposal.time in [3]:
                    proposal.points += 10

            if time == Time.HIGH:
                if proposal.time in [3, 4]:
                    proposal.points += 5
                elif proposal.time in [5]:
                    proposal.points += 10
    
    def evaluate_budget_points(self, budget):
        budget = Budget(budget)
        for proposal in self._proposals:
            if budget == Budget.LOW:
                if proposal.cost in [1]:
                    proposal.points += 10
                elif proposal.cost in [2, 3]:
                    proposal.points += 5

            if budget == Budget.MEDIUM:
                if proposal.cost in [4, 2]:
                    proposal.points += 5
                elif proposal.cost in [3]:
                    proposal.points += 10

            if budget == Budget.HIGH:
                if proposal.cost in [3, 4]:
                    proposal.points += 5
                elif proposal.cost in [5]:
                    proposal.points += 10

    def evaluate_appetite_points(self, appetite):
        appetite = Appetite(appetite)
        for proposal in self._proposals:
            if appetite == Appetite.LOW:
                if proposal.saciety in [1]:
                    proposal.points += 10
                elif proposal.saciety in [2, 3]:
                    proposal.points += 5

            if appetite == Appetite.MEDIUM:
                if proposal.saciety in [4, 2]:
                    proposal.points += 5
                elif proposal.saciety in [3]:
                    proposal.points += 10

            if appetite == Appetite.HIGH:
                if proposal.saciety in [3, 4]:
                    proposal.points += 5
                elif proposal.saciety in [5]:
                    proposal.points += 10


    def evaluate_skill_points(self, skill):
        skill = Skill(skill)
        for proposal in self._proposals:
            if skill == Skill.AMATEUR:
                proposal.points -= proposal.difficulty * 5

    def best_proposal(self):
        l = sorted(self._proposals, key=lambda proposal: proposal.points, reverse=True)
        max_points = l[0].points
        l = [proposal for proposal in l if proposal.points == max_points]
        return sorted(l, key=lambda proposal: proposal.nutritional_value, reverse=True)[0]

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    @property
    def budget(self):
        return self._budget

    @budget.setter
    def budget(self, value):
        self._budget = value

    @property
    def appetite(self):
        return self._appetite

    @appetite.setter
    def appetite(self, value):
        self._appetite = value

    @property
    def skill(self):
        return self._skill

    @skill.setter
    def skill(self, value):
        self._skill = value

    @property
    def proposal(self):
        return self._proposal

    @proposal.setter
    def proposal(self, value):
        self._proposal = value



    def __str__(self):
        return "Time: {}, budget: {}, appetite: {}, skill: {} ".format(str(self._time), str(self._budget), str(self._appetite), self._skill)

class MyIntellect(Intellect):
    pass

def evaluate(appetite, time, budget, skill):
    myIntellect = MyIntellect()

    policy_d = myIntellect.learn(
        Intellect.local_file_uri("./rulesets/policies.policy"))

    model = Model(appetite=appetite, budget=budget, time=time, skill=skill)

    myIntellect.learn(model)
    myIntellect.reason()

    for item in myIntellect.knowledge:
        return item.best_proposal()

from flask import Flask
app = Flask(__name__)
from flask import request, jsonify
from flask_cors import CORS

CORS(app)

@app.route('/fallas1', methods=['POST'])
def suggestion_fallas1():
    parameters = request.get_json()
    suggestion = evaluate(
        parameters.get('appetite', None),
        parameters.get('time', None),
        parameters.get('budget', None),
        parameters.get('skill', None))

    return jsonify({'suggestion': str(suggestion)})

@app.route('/fallas2', methods=['POST'])
def suggestion_fallas2():
    parameters = request.get_json()
    suggestion = evaluate_v2(
        parameters.get('appetite', None),
        parameters.get('time', None),
        parameters.get('budget', None),
        parameters.get('skill', None))

    return jsonify({'suggestion': str(suggestion)})

class MorfiEngine:

    def learn(self, rules_file,learning_method='forward_chaining'):
        self.rule_list = RuleList(rules_file)
        self.learning_method = learning_method

    def learn_model(self, model_object):
        self.model_object = model_object

    def reason(self):
        if self.learning_method == 'forward_chaining':
            self.forward_chaining()
        else:
            raise Exception('Not Supported learning method')

    def forward_chaining(self):
        for rule in self.rule_list.rules:
            applies_rule = all(condition.evaluate(self.model_object) for condition in rule.conditions)
            if applies_rule:
                map(lambda consequence: consequence.apply(self.model_object), rule.consequences)

    @property
    def knowledge(self):
        return self.model_object


def evaluate_v2(appetite, time, budget, skill):
    engine = MorfiEngine()

    engine.learn("rules.json")

    model = Model(appetite=appetite, budget=budget, time=time, skill=skill)

    engine.learn_model(model)
    engine.reason()

    return engine.knowledge.best_proposal()

