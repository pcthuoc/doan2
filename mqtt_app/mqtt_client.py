import paho.mqtt.client as mqtt
import json
import logging
import threading
import queue
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404

# Cấu hình logging
logger = logging.getLogger(__name__)

# Khởi tạo hàng đợi tin nhắn
message_queue = queue.Queue()

def on_connect(client, userdata, flags, rc):
    logger.info(f"Connected to MQTT broker with result code {rc}")
    if rc == 0:
        client.subscribe(settings.MQTT_TOPIC)  # Thay thế bằng chủ đề bạn muốn lắng nghe
    else:
        logger.error(f"Connect failed with result code {rc}")

def on_message(client, userdata, msg):
    try:
        # Đưa tin nhắn vào hàng đợi
        message_queue.put(msg)
    except Exception as e:
        logger.error(f"Error putting message in queue: {e}")

def process_message_queue():
    while True:
        try:
            # Lấy tin nhắn từ hàng đợi
            msg = message_queue.get()
            payload = msg.payload.decode("utf-8")
            data = json.loads(payload)
            value = data.get("value")
            event_type = data.get("event_type")
            topic_parts = msg.topic.split('/')
            
            if len(topic_parts) >= 3:
                api = topic_parts[1]
                pin = topic_parts[2]
            else:
                api = "unknown"
                pin = "unknown"
            
            if event_type == "update":
                try:
                    from devices.models import Device
                    device = get_object_or_404(Device, api_key__api_key=api, pin=pin)
                    if device:
                        device.value = value
                        device.save()
                        channel_layer = get_channel_layer()
                        async_to_sync(channel_layer.group_send)(
                            'notifications',
                            {
                                'type': 'send_notification',
                                'message': f"Value updated to {value} for device with pin {pin}"
                            }
                        )
                    else:
                        logger.warning(f"No device found with API: {api} and Pin: {pin}")
                except Exception as e:
                    logger.error(f"An error occurred while handling the message: {e}")
            
            message_queue.task_done()
        except Exception as e:
            logger.error(f"Error processing message from queue: {e}")

def publish_message(topic, payload):
    client = connect_mqtt()
    if client:
        try:
            client.publish(topic, json.dumps(payload))
            logger.info(f"Published to topic '{topic}' with payload '{payload}'")
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
    else:
        logger.error("MQTT client connection failed")

def connect_mqtt():
    client = mqtt.Client()
    client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    broker_address = settings.MQTT_BROKER_HOST
    broker_port = settings.MQTT_BROKER_PORT

    try:
        client.connect(broker_address, broker_port, 60)
        logger.info("MQTT client connected")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to MQTT broker: {e}")
        return None

def start_mqtt_client():
    client = connect_mqtt()
    if client:
        client.loop_start()
        # Bắt đầu một luồng để xử lý hàng đợi
        processing_thread = threading.Thread(target=process_message_queue)
        processing_thread.daemon = True  # Đảm bảo thread dừng khi chương trình dừng
        processing_thread.start()
    else:
        logger.error("MQTT client failed to start")
