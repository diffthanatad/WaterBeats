import operator
from pathlib import Path
import json
from records import *




ruleID = 0
rules = {} # ruleID : RuleMessage
sensor_rules = {} # sensorID : ruleID[] to find rules applicable to a sensor
latest_sensor_readings = {} # sensorID : reading

ops = {
    '<': operator.lt,
    '<=': operator.le,
    '=': operator.eq,
    '>=': operator.ge,
    '>': operator.gt,
}

def check_relative_condition(relation, sensor_reading, condition_reading):
    return ops[relation](sensor_reading, condition_reading)

# check if sensor readings match any rule conditions
def apply_rules(sensor_message):
    tasks = []
    for ruleID in sensor_rules.get(sensor_message.sensor_id, {}):
        # if rule has a time condition, update the latest sensor reading
        # leave decision making to the event scheduling component
        if not rules[ruleID].time_condition_message == None:
            latest_sensor_readings[sensor_message.sensor_id] = sensor_message.reading
        # else rule does not have a time condition, check if sensor condition is fulfilled
        else:
            task = rules[ruleID].task_message
            condition = rules[ruleID].sensor_condition_message
            if check_relative_condition(condition.relation, sensor_message.reading, condition.reading):
                tasks.append(task)

    return tasks

# make rule active in rule engine
def load_rule(rule_message):
    global ruleID
    rules[ruleID] = rule_message
    if not rule_message.sensor_condition_message == None:
        sensor_id = rule_message.sensor_condition_message.sensor_subject
        if sensor_id in sensor_rules:
            sensor_rules[sensor_id].add(ruleID)
        else:
            sensor_rules[sensor_id] = {ruleID}
        ruleID += 1

# store rule locally for persistence
def store_rule(rule_message):
    try:
        file_location = script_location / 'local_data/rules.txt'
        with open(file_location, 'a', newline='', encoding='utf8') as f:
            f.write(json.dumps(rule_message.task_message.toDict()) + '\t')
            if rule_message.sensor_condition_message == None:
                f.write(json.dumps({'msg': 'empty'}) + '\t')
            else:
                f.write(json.dumps(rule_message.sensor_condition_message.toDict()) + '\t')
            if rule_message.time_condition_message == None:
                f.write(json.dumps({'msg': 'empty'}) + '\n')
            else:
                f.write(json.dumps(rule_message.time_condition_message.toDict()) + '\n')

    except Exception as e:
        print(e)


# apply scheduler
def check_task_schedule(time_message):
    tasks = []
    for rule in rules.values():
        if rule.time_condition_message == None:
            continue
        time_condition = (rule.time_condition_message.execute_time == time_message.timestamp)
        if not time_condition:
            continue
        sensor_condition_message = rule.sensor_condition_message
        if not sensor_condition_message == None:
            relation = sensor_condition_message.relation
            sensor_reading = latest_sensor_readings.get(sensor_condition_message.sensor_subject)
            if sensor_reading == None:
                sensor_condition = False
            else:
                condition_reading = sensor_condition_message.reading
                sensor_condition = check_relative_condition(relation, sensor_reading, condition_reading)
            if sensor_condition:
                tasks.append(rule.task_message)
        else:
            tasks.append(rule.task_message)
    return tasks


### load existing rules from local storage
script_location = Path(__file__).absolute().parent

try:
    file_location = script_location / 'local_data/rules.txt'
    with open(file_location, 'r', newline='') as f:
        for line in f:
            (task, sensor_condition, time_condition) = [json.loads(x) for x in line.split('\t')]
            task_message = TaskMessage(task['actuator_target'], task['state'], task['intensity'], task['actuator_type'], task['duration'])
            if sensor_condition.get('msg') == 'empty':
                sensor_condition_message = None
            else:
                sensor_condition_message = SensorConditionMessage(sensor_condition['sensor_subject'], sensor_condition['reading'], sensor_condition['relation'])
            if time_condition.get('msg') == 'empty':
                time_condition_message = None
            else:
                time_condition_message = TimeConditionMessage(time_condition['execute_time'])
            rule_message = RuleMessage(task_message, sensor_condition_message, time_condition_message)
            load_rule(rule_message)

except Exception as e:
    print('rule engine load local rules failed', e)