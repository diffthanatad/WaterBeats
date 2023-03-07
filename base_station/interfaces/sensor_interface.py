import socket
import json
import producer as p
from aiohttp import web

import device_controller as dc

hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
print("Device Name: "+hostname)
print("Device IP Address: "+IPAddr)

async def handle_request(request):
    if request.method == 'POST':
        data = await request.text()
        print(data)
        response = web.Response(text="Received data: {}".format(data))
        json_data = json.loads(data)
        sensor_data = dc.getSensorData(json_data['sensor_id'])
        if not sensor_data == None:
            p.send_sensor_msg(json_data, sensor_data.device_type, True)
        else:
            print('sensor_id not found in record:', json_data['sensor_id'])
    else:
        response = web.Response(status=405)
    return response

app = web.Application()
app.add_routes([web.post('/sensor_data', handle_request)])

if __name__ == '__main__':
    PORT = 23333
    web.run_app(app, port=PORT)