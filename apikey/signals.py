import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import APIKey
from mqtt_app.mqtt_client import connect_mqtt 
import json
# Cấu hình logger
logger = logging.getLogger(__name__)
@receiver(post_save, sender=User)
def create_user_api_key(sender, instance, created, **kwargs):
    if created:
        # Tạo API key cho người dùng mới
        api_key = APIKey.objects.create(user=instance)
        
        # Kết nối tới MQTT broker
        client = connect_mqtt()
        if client:
            # Tạo payload với thông tin người dùng và API key
            payload = {
                'username': instance.username,
                'api_key': api_key.api_key
            }
            
            # Tạo topic dựa trên API key
            topic = f'API/{api_key.api_key}'
            
            # Gửi payload tới topic cụ thể
            client.publish(topic)
            logger.info(f"Published API key to topic '{topic}'")
