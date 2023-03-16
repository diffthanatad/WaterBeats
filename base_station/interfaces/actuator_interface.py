import asyncio
import websockets
import json

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
            elif data["type"] == "instruction":
                target = data["target"]
                command = data["command"]
                print("Receive Instruction message: {}".format(json_message))
                await sendCommand(target, command)
            else:
                print("Received Message: {}".format(data))
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

if __name__ == '__main__':
    start_server = websockets.serve(handle_message, "0.0.0.0", 8765)
    # start_server = websockets.serve(server.handle_message, "localhost", 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

