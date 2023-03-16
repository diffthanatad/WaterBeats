import asyncio

import websockets
import json

async def sendCommand(end_point, target, command):
    try:
        async with websockets.connect(end_point, ping_timeout=None) as ws:
            message = {
                "type": "instruction",
                "target": target,
                "command": command
            }
            await ws.send(json.dumps(message))
            await ws.close()
    except Exception as e:
        print("Connection error with the {}".format(end_point))

if __name__ == '__main__':
    end_point = "ws://localhost:8765"
    target = 'F4:12:FA:83:00:F0_D'
    command = "on"
    asyncio.run(sendCommand(end_point, target, command))

