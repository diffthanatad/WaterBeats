import pytest
import random
import rule_engine
import datetime
from records import *
from unittest.mock import call, patch, mock_open, Mock
from pathlib import Path



def get_timestamp():
    timestamp = datetime.datetime.now()
    return timestamp

# Rule engine finds applicable rules but only updates the latest sensor reading if the rule contains a time condition
@pytest.mark.asyncio()
async def test_apply_rule_updates_for_time_conditions(test_app):
    OLD_SENSOR_READING = 10
    NEW_SENSOR_READING = 15
    TEST_SENSOR_ID = '30:AE:A4:14:C2:90_A'
    
    task_message = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.1, '', 10)
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