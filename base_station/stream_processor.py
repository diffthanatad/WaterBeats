import json
import time

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
            async with session.post('https://datamanagement.purpleforest-dca89b1d.uksouth.azurecontainerapps.io/sensor_data', json=sensor_json_message(message)) as resp:
                print("Response Status: {}".format(resp.status))
    except aiohttp.ClientConnectorError as e:
        print(f"connection is not available: {e}")

def sensor_json_message(message):
    dic = {
        "sensor_id" : message.sensor_id,
        "sensor_type" : message.sensor_type,
        "data" : message.reading,
        "unit" : message.reading_unit,
        "longitude" : message.longitude,
        "latitude" : message.latitude,
        "timestamp" : time.time_ns()
    }
    return dic

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