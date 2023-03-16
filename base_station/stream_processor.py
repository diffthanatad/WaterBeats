import json

import aiohttp
import websockets

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

def task_json_message(message):
    if message.state:
        command = 'on'
    else:
        command = 'off'
    return {
        "type" : "instruction",
        "target" : message.actuator_target,
        "command" : command
    }

# forward to main hub for task
async def send_task_to_server(message):
    try:
        async with websockets.connect("ws://localhost:8765", ping_timeout=None) as ws:
            json_message = json.dumps(task_json_message(message))
            await ws.send(json_message)
            # await ws.close()
    except Exception as e:
        print("Connection error with the {}".format("ws://localhost:8765"))
        print(e)

# forward to main hub
async def send_to_hub(message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post('http://localhost:5555/sensor_data', json=message) as resp:
                print("Response Status: {}".format(resp.status))
    except aiohttp.ClientConnectorError as e:
        print(f"connection is not available: {e}")