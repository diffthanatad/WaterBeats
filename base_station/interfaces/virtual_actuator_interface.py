import asyncio
import time

import aiohttp
import websockets
import json
from base_station import device_controller as dc

clients = dict()

async def handle_message(websocket, path):
    global check, clients
    try:
        while True:
            json_message = await websocket.recv()
            check = False
            data = json.loads(json_message)
            if data["type"] == "actuator":
                clients[data["actuatorId"]] = websocket
                print("Receive Actuator message: {}".format(json_message))
                await sendToDB(fill_db_message(data))
            elif data["type"] == "instruction":
                target = data["target"]
                command = data["command"]
                print("Receive Instruction message: {}".format(json_message))
                await sendCommand(target, command)
            else:
                print("Received Message: {}".format(data))
                await sendToDB(fill_db_message(data))

    except Exception as e:
        print("Connection Closed with exception: {}".format(e))

async def sendCommand(actuatorId, command):
    global clients
    if actuatorId not in clients:
        print("No such actuator")
        return
    websocket = clients[actuatorId]
    data = json.dumps({"instruction":command})
    await websocket.send(data)

def fill_db_message(data):
    actuator = dc.get_device(data["actuatorId"])
    message = dict()
    message['actuator_id'] = data["actuatorId"]
    message['actuator_type'] = actuator.actuator_type
    message['status'] = data['status']
    message["longitude"] = actuator.longitude
    message["latitude"] = actuator.latitude
    message['timestamp'] = time.time_ns()
    return message

async def sendToDB(message):
    try:
        async with aiohttp.ClientSession() as session:
            print(type(message))
            async with session.post('https://datamanagement.purpleforest-dca89b1d.uksouth.azurecontainerapps.io/actuator_data', json=message) as resp:
                print("Response Status: {}".format(resp.status))
    except aiohttp.ClientConnectorError as e:
        print(f"connection is not available: {e}")

if __name__ == '__main__':
    start_server = websockets.serve(handle_message, "0.0.0.0", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

