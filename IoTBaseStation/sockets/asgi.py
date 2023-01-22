"""
ASGI config for sockets project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sockets.settings')

# application = get_asgi_application()

import os

from sockets.websocket import websocket_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websocket_app.settings')
async def application(scope, receive, send):
        await websocket_application(scope, receive, send)