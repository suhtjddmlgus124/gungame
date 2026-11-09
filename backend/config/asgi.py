"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django_asgi_app = ASGIStaticFilesHandler(get_asgi_application())

from game.consumers import GameConsumer
from game.workers import GameWorker

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(URLRouter([
        path('ws/game/instance/<int:instance_id>/', GameConsumer.as_asgi())
    ])),
    'channel': ChannelNameRouter({
        'game.worker': GameWorker.as_asgi()
    }),
})