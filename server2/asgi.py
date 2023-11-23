"""
ASGI config for server2 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server2.settings')
from django import setup
setup()
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from .auth_middleware import TokenAuthMiddlewareStack
from django.urls import path
from chatbot.views import ChatPDFConsumer
from chat.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server2.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddlewareStack(
        URLRouter([
            path("ws/chatpdf/", ChatPDFConsumer.as_asgi()),
            path("ws/chat/", ChatConsumer.as_asgi())
        ])
    )
})
