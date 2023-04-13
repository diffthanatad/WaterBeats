import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import socket
import json
import producer as p
import records
from aiohttp import web

hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
print("Device Name: "+hostname)
print("Device IP Address: "+IPAddr)

async def handle_request(request):
    if request.method == 'POST':
        data = await request.text()
        response = web.Response(text="Received data: {}".format(data))
        json_data = json.loads(data)
        sensor_message = records.SensorMessage(json_data.get("sensor_id"), json_data.get("reading"))
        p.send_sensor_msg(sensor_message, True)
    else:
        response = web.Response(status=405)
    return response

app = web.Application()
app.add_routes([web.post('/sensor_data', handle_request)])

if __name__ == '__main__':
    PORT = 23333
    web.run_app(app, port=PORT)