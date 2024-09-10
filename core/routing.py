from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r'ws/update_relay/$', consumers.RelayConsumer.as_asgi()),
    re_path(r'ws/update_sensor/$', consumers.SensorConsumer.as_asgi()),
]