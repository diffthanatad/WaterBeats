import asyncio
import time

import websockets
import json

async def handle_message(websocket, path):
    while True:
        message = await websocket.recv()
        print(message)
        time.sleep(2)
        command = "on"
        # print(f"Received message: {message}")
        data = {"instruction" : command}
        await websocket.send(json.dumps(data))

start_server = websockets.serve(handle_message, "0.0.0.0", 8765)
# start_server = websockets.serve(handle_message, "localhost", 8765)


asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
