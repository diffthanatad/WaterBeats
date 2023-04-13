import pytest
import stream_processor
import datetime
from records import *
from unittest.mock import call, patch, AsyncMock, Mock



def get_timestamp(exact = True):
    timestamp = datetime.datetime.now()
    if not exact:
        timestamp = timestamp.replace(second = 0, microsecond = 0)
    return timestamp

@pytest.mark.asyncio()
async def test_process_sensor_message(test_app):
    SENSOR_READING = 15
    TEST_SENSOR_ID = '30:AE:A4:14:C2:90_A'

    sensor_message = SensorMessage(TEST_SENSOR_ID, SENSOR_READING)
    task_message_1 = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.1, '', 10)
    task_message_2 = TaskMessage('F4:12:FA:83:00:F0_E', True, 0.2, '', 10)
    with(
        patch('stream_processor.re.apply_rules') as mocked_apply_rules,
        patch('stream_processor.bs.task_stream.send', new_callable=AsyncMock) as mocked_send
        ):
        mocked_apply_rules.return_value = [task_message_1, task_message_2]
        await stream_processor.process_sensor_message(sensor_message)
        expected_calls = [call(value = task_message_1), call(value = task_message_2)]
        mocked_send.assert_has_calls(expected_calls)

@pytest.mark.asyncio()
async def test_process_time_message(test_app):
    time_message = TimeMessage(get_timestamp(exact = False))
    task_message_1 = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.1, '', 10)
    task_message_2 = TaskMessage('F4:12:FA:83:00:F0_E', True, 0.2, '', 10)
    with(
        patch('stream_processor.re.check_task_schedule') as mocked_check_task_schedule,
        patch('stream_processor.bs.task_stream.send', new_callable=AsyncMock) as mocked_send
        ):
        mocked_check_task_schedule.return_value = [task_message_1, task_message_2]
        await stream_processor.process_time_message(time_message)
        expected_calls = [call(value = task_message_1), call(value = task_message_2)]
        mocked_send.assert_has_calls(expected_calls)