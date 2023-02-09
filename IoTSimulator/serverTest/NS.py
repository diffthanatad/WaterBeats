# import aiohttp
from aiohttp import web
import asyncio

async def handle_request(request):
    if request.method == 'POST':
        data = await request.text()
        print(data)
        response = web.Response(text="Received data: {}".format(data))
    else:
        response = web.Response(status=405)
    return response

app = web.Application()
app.add_routes([web.post('/new_data', handle_request)])

if __name__ == '__main__':
    PORT = 23333
    web.run_app(app, port=PORT)