import aiohttp

import base_station_app as bs
import rule_engine as re



# process sensor messages
# apply rules using rule engine, send new tasks to task stream
async def process_sensor_message(message):
    tasks = re.apply_rules(message)
    for task in tasks:
        await bs.task_stream.send(value=task)

# process time messages
# apply rules using rule engine, send new tasks to task stream
async def process_time_message(message):
    tasks = re.check_task_schedule(message)
    for task in tasks:
        await bs.task_stream.send(value=task)

# forward to main hub
async def send_to_hub(message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post('http://localhost:5555/sensor_data', json=message) as resp:
                print("Response Status: {}".format(resp.status))
    except aiohttp.ClientConnectorError as e:
        print(f"connection is not available: {e}")