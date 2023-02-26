# import aiohttp
from aiohttp import web
import subprocess
import json

def changeToCommand(command):
    newcommand = 'cd Faust && faust -A bs_hub send @soil_moisture_readings "{"""sensor_id""": """External_Sensor""", """reading_value""": """123"""}"'
    result = subprocess.run(newcommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #print('hi')
    if result.returncode == 0:
        print(result.stdout.decode('utf-8'))
    else:
        print(result.stderr.decode('utf-8'))

async def handle_request(request):
    if request.method == 'POST':
        json_data = await request.text()
        data = json.loads(json_data)
        id = data["sensor_id"]
        timestamp = data["timestamp"]
        if 'temperature' in data:
            # temperature sensor
            topic = "temperature_readings"
            value = data["temperature"]
        elif 'soil_moisture' in data:
            topic = "soil_moisture_readings"
            value = data["soil_moisture"]
        elif 'water_level' in data:
            topic = "humidity_readings"
            value = data["water_level"]
        command = "cd Faust && faust -A bs_hub send @{} '{{\"\"\"sensor_id\"\"\": \"\"\"{}\"\"\", \"\"\"reading_value\"\"\": \"\"\"{}\"\"\"}}'".format(
            topic, id, value)
        #print(command)
        changeToCommand(command)
        response = web.Response(text="Received data: {}".format(data))
    else:
        response = web.Response(status=405)
    return response

app = web.Application()
app.add_routes([web.post('/new_data', handle_request)])

if __name__ == '__main__':
    PORT = 23333
    web.run_app(app, port=PORT)