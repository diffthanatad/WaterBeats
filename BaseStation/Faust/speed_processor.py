import aiohttp

import base_station as bs
import rule_engine as re
import device_controller as dc



# send to rule engine and retrieve applicable tasks
async def process(message):
    tasks = re.analyse(message)
    for task in tasks:
        actuator_data = dc.getActuatorData(task.target)
        task_msg = bs.TaskMessage(task.target, actuator_data.device_type, task.state, task.intensity, task.duration)

        await bs.task_stream.send(value=task_msg)



# forward to main hub
async def sendToHub(message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post('http://localhost:5555/sensor_data', json=message) as resp:
                print("Response Status: {}".format(resp.status))
    except aiohttp.ClientConnectorError as e:
        print(f"connection is not available: {e}")