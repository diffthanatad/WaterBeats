import pytest
import random
import rule_engine
import datetime
from records import *
from unittest.mock import call, patch, mock_open, Mock, ANY
from pathlib import Path



def get_timestamp(exact = True):
    timestamp = datetime.datetime.now()
    if not exact:
        timestamp = timestamp.replace(second = 0, microsecond = 0)
    return timestamp

# Rule engine finds applicable rules but only updates the latest sensor reading if the rule contains a time condition
@pytest.mark.asyncio()
async def test_apply_rule_updates_for_time_conditions(test_app):
    OLD_SENSOR_READING = 10
    NEW_SENSOR_READING = 15
    TEST_SENSOR_ID = '30:AE:A4:14:C2:90_A'
    
    task_message = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.1, 'sprinkler', 10)
    next_minute = str(get_timestamp() + datetime.timedelta(minutes = 1))
    time_condition_message = TimeConditionMessage(next_minute)
    rule_message = RuleMessage(task_message, None, time_condition_message)
    mocked_rules = {0 : rule_message}
    mocked_sensor_rules = {TEST_SENSOR_ID : [0]}
    mocked_latest_sensor_readings = {TEST_SENSOR_ID : OLD_SENSOR_READING}
    mocked_check_relative_condition = Mock()
    with patch.multiple("rule_engine", 
                        sensor_rules = mocked_sensor_rules, 
                        rules = mocked_rules, 
                        latest_sensor_readings = mocked_latest_sensor_readings,
                        check_relative_condition = mocked_check_relative_condition):
        sensor_message = SensorMessage(TEST_SENSOR_ID, NEW_SENSOR_READING)
        rule_engine.apply_rules(sensor_message)
        assert(mocked_latest_sensor_readings[TEST_SENSOR_ID] == NEW_SENSOR_READING)
        mocked_check_relative_condition.assert_not_called()

@pytest.mark.asyncio()
async def test_apply_rule_appends_no_tasks(test_app):
    OLD_SENSOR_READING = 10
    NEW_SENSOR_READING = 15
    SENSOR_CONDITION = 15
    CONDITION_RELATION = '<'
    TEST_SENSOR_ID = '30:AE:A4:14:C2:90_A'
    
    task_message = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.1, 'sprinkler', 10)
    sensor_condition_message = SensorConditionMessage(TEST_SENSOR_ID, SENSOR_CONDITION, CONDITION_RELATION)
    rule_message = RuleMessage(task_message, sensor_condition_message, None)

    mocked_rules = {0 : rule_message}
    mocked_sensor_rules = {TEST_SENSOR_ID : [0]}
    mocked_latest_sensor_readings = {TEST_SENSOR_ID : OLD_SENSOR_READING}
    with patch.multiple("rule_engine", 
                        sensor_rules = mocked_sensor_rules, 
                        rules = mocked_rules, 
                        latest_sensor_readings = mocked_latest_sensor_readings):
        sensor_message = SensorMessage(TEST_SENSOR_ID, NEW_SENSOR_READING)
        
        assert(rule_engine.apply_rules(sensor_message) == [])

@pytest.mark.asyncio()
async def test_apply_rule_appends_one_task(test_app):
    OLD_SENSOR_READING = 10
    NEW_SENSOR_READING = 15
    CONDITION_RELATION = '<='
    TEST_SENSOR_ID = '30:AE:A4:14:C2:90_A'
    
    task_message = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.1, 'sprinkler', 10)
    sensor_condition_message = SensorConditionMessage(TEST_SENSOR_ID, NEW_SENSOR_READING, CONDITION_RELATION)
    rule_message = RuleMessage(task_message, sensor_condition_message, None)

    mocked_rules = {0 : rule_message}
    mocked_sensor_rules = {TEST_SENSOR_ID : [0]}
    mocked_latest_sensor_readings = {TEST_SENSOR_ID : OLD_SENSOR_READING}
    with patch.multiple("rule_engine", 
                        sensor_rules = mocked_sensor_rules, 
                        rules = mocked_rules, 
                        latest_sensor_readings = mocked_latest_sensor_readings):
        sensor_message = SensorMessage(TEST_SENSOR_ID, NEW_SENSOR_READING)
        
        assert(rule_engine.apply_rules(sensor_message) == [task_message])

@pytest.mark.asyncio()
async def test_apply_rule_appends_two_tasks(test_app):
    OLD_SENSOR_READING = 10
    NEW_SENSOR_READING = 15
    CONDITION_RELATION = '<='
    TEST_SENSOR_ID = '30:AE:A4:14:C2:90_A'
    
    task_message_1 = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.1, 'sprinkler', 10)
    sensor_condition_message_1 = SensorConditionMessage(TEST_SENSOR_ID, NEW_SENSOR_READING, CONDITION_RELATION)
    rule_message_1 = RuleMessage(task_message_1, sensor_condition_message_1, None)
    
    task_message_2 = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.2, 'sprinkler', 20)
    sensor_condition_message_2 = SensorConditionMessage(TEST_SENSOR_ID, NEW_SENSOR_READING, CONDITION_RELATION)
    rule_message_2 = RuleMessage(task_message_2, sensor_condition_message_2, None)

    mocked_rules = {0 : rule_message_1, 1 : rule_message_2}
    mocked_sensor_rules = {TEST_SENSOR_ID : [0, 1]}
    mocked_latest_sensor_readings = {TEST_SENSOR_ID : OLD_SENSOR_READING}
    with patch.multiple("rule_engine", 
                        sensor_rules = mocked_sensor_rules, 
                        rules = mocked_rules, 
                        latest_sensor_readings = mocked_latest_sensor_readings):
        sensor_message = SensorMessage(TEST_SENSOR_ID, NEW_SENSOR_READING)
        
        assert(sorted(rule_engine.apply_rules(sensor_message)) == sorted([task_message_1, task_message_2]))

@pytest.mark.asyncio()
async def test_load_rule_new_sensor(test_app):
    NEW_SENSOR_READING = 15
    CONDITION_RELATION = '<='
    TEST_SENSOR_ID = '30:AE:A4:14:C2:90_A'

    task_message_1 = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.1, 'sprinkler', 10)
    sensor_condition_message_1 = SensorConditionMessage(TEST_SENSOR_ID, NEW_SENSOR_READING, CONDITION_RELATION)
    rule_message_1 = RuleMessage(task_message_1, sensor_condition_message_1, None)

    start_ruleID = 0
    mocked_ruleID = 1
    mocked_rules = {}
    mocked_sensor_rules = {}

    with patch.multiple("rule_engine",
                        ruleID = mocked_ruleID,
                        rules = mocked_rules,
                        sensor_rules = mocked_sensor_rules):
        rule_engine.load_rule(rule_message_1)
        assert(mocked_rules[mocked_ruleID] == rule_message_1)
        assert(mocked_sensor_rules[TEST_SENSOR_ID] == {mocked_ruleID})
        assert(mocked_ruleID == start_ruleID + 1)



@pytest.mark.asyncio()
async def test_load_rule_existing_sensor(test_app):
    NEW_SENSOR_READING = 15
    CONDITION_RELATION = '<='
    TEST_SENSOR_ID = '30:AE:A4:14:C2:90_A'

    task_message_1 = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.1, 'sprinkler', 10)
    sensor_condition_message_1 = SensorConditionMessage(TEST_SENSOR_ID, NEW_SENSOR_READING, CONDITION_RELATION)
    rule_message_1 = RuleMessage(task_message_1, sensor_condition_message_1, None)

    start_ruleID = 1
    mocked_rules = {}
    mocked_sensor_rules = {TEST_SENSOR_ID : {0}}

    with patch.multiple("rule_engine",
                        ruleID = 1,
                        rules = mocked_rules,
                        sensor_rules = mocked_sensor_rules):
        rule_engine.load_rule(rule_message_1)
        assert(mocked_rules[start_ruleID] == rule_message_1)
        assert(mocked_sensor_rules[TEST_SENSOR_ID] == {0, start_ruleID})
        assert(rule_engine.ruleID == start_ruleID + 1)

@pytest.mark.asyncio()
async def test_store_rule_with_both_conditions(test_app):
    NEW_SENSOR_READING = 15
    CONDITION_RELATION = '<='
    TEST_SENSOR_ID = '30:AE:A4:14:C2:90_A'

    task_message_1 = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.1, 'sprinkler', 10)
    sensor_condition_message_1 = SensorConditionMessage(TEST_SENSOR_ID, NEW_SENSOR_READING, CONDITION_RELATION)
    next_minute = str(get_timestamp() + datetime.timedelta(minutes = 1))
    time_condition_message = TimeConditionMessage(next_minute)
    rule_message_1 = RuleMessage(task_message_1, sensor_condition_message_1, time_condition_message)

    mocked_open = mock_open()
    with patch("rule_engine.open", mocked_open, create=True):
        rule_engine.store_rule(rule_message_1)

    script_location = Path(__file__).absolute().parent.parent
    file_location = script_location / 'local_data/rules.txt'

    mocked_open.assert_called_with(file_location, 'a', newline='', encoding='utf8')
    expected_calls = [
        call('{"actuator_target": "F4:12:FA:83:00:F0_D", "state": true, "intensity": 0.1, "actuator_type": "sprinkler", "duration": 10}\t'), 
        call('{"sensor_subject": "30:AE:A4:14:C2:90_A", "reading": 15, "relation": "<="}\t'), 
        call(ANY)]
    mocked_open.return_value.write.assert_has_calls(expected_calls)

@pytest.mark.asyncio()
async def test_store_rule_missing_sensor_condition(test_app):
    task_message_1 = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.1, 'sprinkler', 10)
    next_minute = str(get_timestamp() + datetime.timedelta(minutes = 1))
    time_condition_message = TimeConditionMessage(next_minute)
    rule_message_1 = RuleMessage(task_message_1, None, time_condition_message)

    mocked_open = mock_open()
    with patch("rule_engine.open", mocked_open, create=True):
        rule_engine.store_rule(rule_message_1)

    script_location = Path(__file__).absolute().parent.parent
    file_location = script_location / 'local_data/rules.txt'

    mocked_open.assert_called_with(file_location, 'a', newline='', encoding='utf8')
    expected_calls = [
        call('{"actuator_target": "F4:12:FA:83:00:F0_D", "state": true, "intensity": 0.1, "actuator_type": "sprinkler", "duration": 10}\t'), 
        call('{"msg": "empty"}\t'), 
        call(ANY)]
    mocked_open.return_value.write.assert_has_calls(expected_calls)

@pytest.mark.asyncio()
async def test_store_rule_missing_time_condition(test_app):
    NEW_SENSOR_READING = 15
    CONDITION_RELATION = '<='
    TEST_SENSOR_ID = '30:AE:A4:14:C2:90_A'

    task_message_1 = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.1, 'sprinkler', 10)
    sensor_condition_message_1 = SensorConditionMessage(TEST_SENSOR_ID, NEW_SENSOR_READING, CONDITION_RELATION)
    rule_message_1 = RuleMessage(task_message_1, sensor_condition_message_1, None)

    mocked_open = mock_open()
    with patch("rule_engine.open", mocked_open, create=True):
        rule_engine.store_rule(rule_message_1)

    script_location = Path(__file__).absolute().parent.parent
    file_location = script_location / 'local_data/rules.txt'

    mocked_open.assert_called_with(file_location, 'a', newline='', encoding='utf8')
    expected_calls = [
        call('{"actuator_target": "F4:12:FA:83:00:F0_D", "state": true, "intensity": 0.1, "actuator_type": "sprinkler", "duration": 10}\t'), 
        call('{"sensor_subject": "30:AE:A4:14:C2:90_A", "reading": 15, "relation": "<="}\t'), 
        call('{"msg": "empty"}\n')]
    mocked_open.return_value.write.assert_has_calls(expected_calls)

@pytest.mark.asyncio()
async def test_check_task_schedule_no_rules(test_app):
    time_message = TimeConditionMessage(get_timestamp())
    mocked_rules = {}
    with patch.multiple("rule_engine", rules = mocked_rules):
        assert(rule_engine.check_task_schedule(time_message) == [])

@pytest.mark.asyncio()
async def test_check_task_schedule_no_valid_rules(test_app):
    current_time = get_timestamp(exact = False)
    current_time_message = TimeMessage(current_time)
    NEW_SENSOR_READING = 30
    READING_CONDITION = 15
    CONDITION_RELATION = '<='
    TEST_SENSOR_ID_1 = '30:AE:A4:14:C2:90_A'
    TEST_SENSOR_ID_2 = '30:AE:A4:14:C2:90_B'

    sensor_condition_message_1 = SensorConditionMessage(TEST_SENSOR_ID_1, READING_CONDITION, CONDITION_RELATION)
    task_message_1 = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.1, 'sprinkler', 10)
    rule_message_1 = RuleMessage(task_message_1, sensor_condition_message_1, None)

    sensor_condition_message_2 = SensorConditionMessage(TEST_SENSOR_ID_1, READING_CONDITION, CONDITION_RELATION)
    task_message_2 = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.2, 'sprinkler', 10)
    time_message_2 = TimeConditionMessage(current_time)
    rule_message_2 = RuleMessage(task_message_2, sensor_condition_message_2, time_message_2)

    sensor_condition_message_3 = SensorConditionMessage(TEST_SENSOR_ID_1, READING_CONDITION, CONDITION_RELATION)
    task_message_3 = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.2, 'sprinkler', 10)
    time_message_3 = TimeConditionMessage(current_time + datetime.timedelta(minutes = 1))
    rule_message_3 = RuleMessage(task_message_3, sensor_condition_message_3, time_message_3)

    sensor_condition_message_4 = SensorConditionMessage(TEST_SENSOR_ID_2, READING_CONDITION, CONDITION_RELATION)
    task_message_4 = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.2, 'sprinkler', 10)
    time_message_4 = TimeConditionMessage(current_time)
    rule_message_4 = RuleMessage(task_message_4, sensor_condition_message_4, time_message_4)
    
    mocked_rules = {0 : rule_message_1, 1 : rule_message_2, 2 : rule_message_3, 3 : rule_message_4}
    mocked_latest_sensor_readings = {TEST_SENSOR_ID_1 : NEW_SENSOR_READING}
    with patch.multiple("rule_engine", 
                        rules = mocked_rules,
                        latest_sensor_readings = mocked_latest_sensor_readings):
        assert(rule_engine.check_task_schedule(current_time_message) == [])

@pytest.mark.asyncio()
async def test_check_task_schedule_some_valid_rules(test_app):
    current_time = get_timestamp(exact = False)
    current_time_message = TimeMessage(current_time)
    NEW_SENSOR_READING = 10
    READING_CONDITION = 15
    CONDITION_RELATION = '<='
    TEST_SENSOR_ID_1 = '30:AE:A4:14:C2:90_A'
    TEST_SENSOR_ID_2 = '30:AE:A4:14:C2:90_B'
    
    task_message_1 = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.1, 'sprinkler', 10)
    time_condition_message_1 = TimeConditionMessage(current_time)
    rule_message_1 = RuleMessage(task_message_1, None, time_condition_message_1)

    task_message_2 = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.2, 'sprinkler', 10)
    sensor_condition_message_2 = SensorConditionMessage(TEST_SENSOR_ID_1, READING_CONDITION, CONDITION_RELATION)
    time_condition_message_2 = TimeConditionMessage(current_time)
    rule_message_2 = RuleMessage(task_message_2, sensor_condition_message_2, time_condition_message_2)

    task_message_3 = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.2, 'sprinkler', 10)
    sensor_condition_message_3 = SensorConditionMessage(TEST_SENSOR_ID_2, READING_CONDITION, CONDITION_RELATION)
    time_condition_message_3 = TimeConditionMessage(current_time)
    rule_message_3 = RuleMessage(task_message_3, sensor_condition_message_3, time_condition_message_3)
    
    mocked_rules = {0 : rule_message_1, 1 : rule_message_2, 2 : rule_message_3}
    mocked_latest_sensor_readings = {TEST_SENSOR_ID_1 : NEW_SENSOR_READING}
    with patch.multiple("rule_engine", 
                        rules = mocked_rules,
                        latest_sensor_readings = mocked_latest_sensor_readings):
        assert(rule_engine.check_task_schedule(current_time_message) == [task_message_1, task_message_2])