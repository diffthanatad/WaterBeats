import pytest
import random
import asyncio
import datetime
from base_station_app import stream_agent_sensor, batch_agent_sensor, tasks_agent, rules_agent, time_agent, send_time_message
from records import *
from unittest.mock import patch, AsyncMock, Mock



def get_timestamp():
    timestamp = datetime.datetime.now()
    return timestamp

# Sensor batch agent receives batch messages and calls the batch processor to store each message
@pytest.mark.asyncio()
async def test_batch_agent_sensor_yield(test_app):
    reading = random.randint(10, 30)
    sensor_id, sensor_type, reading_unit  = 'F4:12:FA:83:00:F0_A', 'temperature sensor', 'Celsius'
    timestamp = ''
    latitude, longitude = '51.509865', '-0.118092'
    sensor_message = SensorMessage(sensor_id, reading, sensor_type, reading_unit, timestamp, latitude, longitude)

    with patch('base_station_app.bp') as mock_bp:
        async with batch_agent_sensor.test_context() as agent:
            await agent.put(sensor_message)
            mock_bp.store_locally.assert_called_with([sensor_message])

# Sensor stream agent gets sensor metadata, correctly fills in the full sensor message and sends to sink
@pytest.mark.asyncio()
async def test_stream_agent_sensor_yield(test_app):
    async with stream_agent_sensor.test_context() as agent:
        sensor_message = SensorMessage('30:AE:A4:14:C2:90_A', 15)
        event = await agent.put(sensor_message)
        actual_output = agent.results[event.message.offset]
        actual_output.timestamp = '' # don't compare timestamps
        expected_output = SensorMessage('30:AE:A4:14:C2:90_A', 15, 'temperature sensor', 'Celsius', '', '51.509865', '-0.118092')
        assert actual_output == expected_output

# Sensor stream agent is able to finish processing 1000 messages sent concurrently with minimal delay
@pytest.mark.asyncio()
async def test_stream_agent_sensor_performance(test_app):
    async with stream_agent_sensor.test_context() as agent:
        messages = []
        NUM_MESSAGES = 1000
        for _ in range(NUM_MESSAGES):
            reading = random.randint(10, 30)
            sensor_message = SensorMessage('F4:12:FA:83:00:F0_A', reading) # temperature message
            messages.append(sensor_message)

        async def send_message(sensor_message):
            await agent.put(sensor_message)

        start_time = get_timestamp()
        await asyncio.gather(*map(send_message, messages))
        finish_time = get_timestamp()
        process_time = finish_time - start_time
        print(f'Processing {NUM_MESSAGES} sensor messages took {process_time.total_seconds()} seconds')
        assert process_time < datetime.timedelta(milliseconds = 1000)

# Task stream agent gets sensor metadata, correctly fills in the full sensor message and sends to sink
@pytest.mark.asyncio()
async def test_tasks_agent_yield(test_app):
    async with tasks_agent.test_context() as agent:
        task_message = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.1, '', 10)
        event = await agent.put(task_message)
        actual_output = agent.results[event.message.offset]
        expected_output = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.1, 'sprinkler', 10)
        assert actual_output == expected_output

def mock_task_coro(return_value=None, **kwargs):
    """Create mock coroutine function."""
    async def wrapped(*args, **kwargs):
        return return_value
    return Mock(wraps=wrapped, **kwargs)

# Rule stream agent sends task if rule contains no conditions
@pytest.mark.asyncio()
async def test_rules_agent_sends_tasks(test_app):
    task_message = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.1, '', 10)
    rule_message = RuleMessage(task_message)
    with patch('base_station_app.task_stream') as mocked_task_stream:
        mocked_task_stream.send = mock_task_coro()
        async with rules_agent.test_context() as agent:
            await agent.put(rule_message)
            mocked_task_stream.send.assert_called_with(value=task_message)

# Rule stream agent calls loads and stores rule using rule engine if rule contains conditions
@pytest.mark.asyncio()
async def test_rules_agent_sends_rules(test_app):
    task_message = TaskMessage('F4:12:FA:83:00:F0_D', True, 0.1, '', 10)
    sensor_condition_message = SensorConditionMessage('F4:12:FA:83:00:F0_A', 20, '<')
    next_minute = str(get_timestamp() + datetime.timedelta(minutes = 1))
    time_condition_message = TimeConditionMessage(next_minute)
    rule_message = RuleMessage(task_message, sensor_condition_message, time_condition_message)
    with patch('base_station_app.re') as mocked_re:
        async with rules_agent.test_context() as agent:
            await agent.put(rule_message)
            mocked_re.load_rule.assert_called_with(rule_message)
            mocked_re.store_rule.assert_called_with(rule_message)

# Time stream agent gets time message and sends to stream processor for time-based rule processing
@pytest.mark.asyncio()
async def test_time_agent_sends(test_app):
    timestamp = str(get_timestamp().replace(second = 0, microsecond = 0))
    time_message = TimeMessage(timestamp)

    with patch('base_station_app.sp.process_time_message') as mock_sp:
        async with time_agent.test_context() as agent:
            await agent.put(time_message)
            mock_sp.assert_called_with(time_message)

# Timer executes task every interval and sends time message to time stream
# @pytest.mark.asyncio()
# async def test_send_time_message_sends(test_app):
#     timestamp = str(get_timestamp().replace(second = 0, microsecond = 0))
#     time_message = TimeMessage(timestamp)

#     with patch('base_station_app.time_stream.send') as mocked_time_stream:
#         await send_time_message()
#         mocked_time_stream.assert_called_with(time_message)