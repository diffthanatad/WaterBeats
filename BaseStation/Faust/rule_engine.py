import operator
from pathlib import Path
import json

ops = {
    '<': operator.lt,
    '<=': operator.le,
    '=': operator.eq,
    '>=': operator.ge,
    '>': operator.gt,
}


class Task:
    """Tasks for an actuator

    Attributes:
        target      The actuatorid/target to control
        state       The intended on/off state of the instruction to the target
        intensity   E.g., rotational speed of motor, pressure of sprinkler. Between 0 and 1.
        duration    Optional duration until reversion to previous state in seconds. -1 for indefinite duration.
    """

    def __init__(self, target: str, state: str, intensity: float, duration: int):
        self.target = target
        self.state = state
        self.intensity = intensity
        self.duration = duration
    
    def __str__(self):
        return(f"Task({self.target}, {self.state}, {self.intensity}, {self.duration})")

class Condition:
    def __init__(self, time: str, recurring: bool):
        pass



class TimeCondition(Condition):
    def __init__(self, time: str, recurring: bool):
        self.time = time
        self.recurring = recurring

class Rule:
    def __init__(self, task: Task, condition: Condition):
        self.task = task
        self.condition = condition

# conditionTime = datetime.datetime.now() + datetime.timedelta(seconds=10)

# condition1 = Condition(conditionTime, False, 'test_sensor3', 20, '<')

ruleID = 0

stored_rules = {}

relevant_sensors = {}

def analyse(sensor_message):
    tasks = []
    for ruleID in relevant_sensors[sensor_message.sensor_id]:
        task = stored_rules[ruleID].task_message
        condition = stored_rules[ruleID].condition_message
        if ops[condition.relation](sensor_message.reading, condition.reading):
            tasks.append(task)

    return tasks
    


script_location = Path(__file__).absolute().parent


def saveRule(rule_message):
    try:
        file_location = script_location / 'local_data/rules.txt'

        with open(file_location, 'a', newline='', encoding='utf8') as f:

            f.write(str(rule_message))

    except Exception as e:
        print(e)

def addRule(rule_message):
    saveRule(rule_message)
    global ruleID
    stored_rules[ruleID] = rule_message
    sensor_id = rule_message.condition_message.sensor_subject
    if sensor_id in relevant_sensors: 
        relevant_sensors[sensor_id].add(ruleID)
    else:
        new_set = set()
        new_set.add(ruleID)
        relevant_sensors[sensor_id] = new_set
    ruleID += 1