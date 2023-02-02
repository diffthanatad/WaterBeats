import asyncio
import websockets
import json

async def handle_message(websocket, path):
    while True:
        message = await websocket.recv()
        print(message)
        command = input("命令：")
        # print(f"Received message: {message}")
        data = {"instruction" : command}
        await websocket.send(json.dumps(data))

start_server = websockets.serve(handle_message, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
