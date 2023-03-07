import asyncio
import time
import producer as ps
import websockets
import json

clients = dict()
message_buffer = []
check = False

async def handle_message(websocket, path):
    while True:
        json_message = await websocket.recv()
        check = False
        data = json.loads(json_message)
        if data["actuatorId"] not in clients:
            clients[data["actuatorId"]] = websocket
        #     shared_dict.set_shared_value(data["actuatorId"],websocket)
        # print(shared_dict.shared_dict)
        print(json_message)
        # print(clients)
        # time.sleep(2)
        # command = "on"
        # # print(f"Received message: {message}")
        # data = {"instruction" : command}
        # await websocket.send(json.dumps(data))

async def sendCommand(actuatorId, command):
    print(clients)
    if actuatorId not in clients:
        print("No such actuator")
        return
    websocket = clients[actuatorId]
    print(websocket)
    data = json.dumps({"instruction":command})
    await websocket.send(data)
    check = True

if __name__ == '__main__':
    start_server = websockets.serve(handle_message, "0.0.0.0", 8765)
    # start_server = websockets.serve(server.handle_message, "localhost", 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

