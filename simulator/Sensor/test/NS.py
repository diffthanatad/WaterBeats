# import aiohttp
import aiohttp
from aiohttp import web
import asyncio
import socket

hostname=socket.gethostname()   
IPAddr=socket.gethostbyname(hostname)   
print("Your Computer Name is:"+hostname)   
print("Your Computer IP Address is:"+IPAddr) 

async def handle_request(request):
    if request.method == 'POST':
        data = await request.text()
        print(data)
        response = web.Response(text="Received data: {}".format(data))
        # async with aiohttp.ClientSession() as session:
        #     async with session.post('http://localhost:5555/sensor_data', json=data) as resp:
        #         print("Response Status: {}".format(resp.status))
    else:
        response = web.Response(status=405)
    return response

app = web.Application()
app.add_routes([web.post('/new_data', handle_request)])

if __name__ == '__main__':
    PORT = 23333
    web.run_app(app, port=PORT)