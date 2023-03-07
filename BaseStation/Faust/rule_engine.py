import operator
import sys
from pathlib import Path
import json
from records import *



ops = {
    '<': operator.lt,
    '<=': operator.le,
    '=': operator.eq,
    '>=': operator.ge,
    '>': operator.gt,
}

ruleID = 0
rules = {} # ruleID : RuleMessage
sensor_rules = {} # sensorID : ruleID[] to find rules applicable to a sensor

# check if sensor readings match any rule conditions
def applyRules(sensor_message):
    tasks = []
    for ruleID in sensor_rules.get(sensor_message.sensor_id):
        task = rules[ruleID].task_message
        condition = rules[ruleID].condition_message
        if ops[condition.relation](sensor_message.reading, condition.reading):
            tasks.append(task)

    return tasks

# make rule active in rule engine
def loadRule(rule_message):
    global ruleID
    rules[ruleID] = rule_message
    sensor_id = rule_message.condition_message.sensor_subject
    if sensor_id in sensor_rules:
        sensor_rules[sensor_id].add(ruleID)
    else:
        sensor_rules[sensor_id] = {ruleID}
    ruleID += 1

# store rule locally for persistence
def storeRule(rule_message):
    try:
        file_location = script_location / 'local_data/rules.txt'
        with open(file_location, 'a', newline='', encoding='utf8') as f:
            f.write(json.dumps(rule_message.task_message.toDict()) + '\t')
            f.write(json.dumps(rule_message.condition_message.toDict()) + '\n')

    except Exception as e:
        print(e)



### load existing rules from local storage
script_location = Path(__file__).absolute().parent

try:
    file_location = script_location / 'local_data/rules.txt'
    with open(file_location, 'r', newline='') as f:
        for line in f:
            (task, condition) = [json.loads(x) for x in line.split('\t')]
            task_message = TaskMessage(task['actuator_target'], task['state'], task['intensity'], task['actuator_type'], task['duration'])
            condition_message = ConditionMessage(condition['sensor_subject'], condition['reading'], condition['relation'])
            rule_message = RuleMessage(task_message, condition_message)
            loadRule(rule_message)

except Exception as e:
    print('rule engine load local rules failed', e)