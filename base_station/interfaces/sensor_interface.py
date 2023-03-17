import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import socket
import json
import producer as p
from aiohttp import web
from base_station import device_controller as dc

hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
print("Device Name: "+hostname)
print("Device IP Address: "+IPAddr)

async def handle_request(request):
    if request.method == 'POST':
        data = await request.json()
        response = web.Response(text="Received data: {}".format(data))
        dic_data = json.loads(data)
        message = {'sensor_id': dic_data["sensor_id"], 'reading': dic_data["reading"]}
        p.send_sensor_msg(message, True)
    else:
        response = web.Response(status=405)
    return response

app = web.Application()
app.add_routes([web.post('/sensor_data', handle_request)])

if __name__ == '__main__':
    PORT = 23333
    web.run_app(app, port=PORT)