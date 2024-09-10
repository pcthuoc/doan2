from django.apps import AppConfig
from .mqtt_client import start_mqtt_client

class MqttAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mqtt_app'
    def ready(self):
        start_mqtt_client()
