from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/fibonacci/', consumers.FibonacciConsumer.as_asgi()),
]