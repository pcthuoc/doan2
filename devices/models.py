import binascii
import os

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
class Device(models.Model):
    """
    IoT Device manager.
    """
    RELAY = 1
    SENSOR = 2
    DEVICE_TYPE_CHOICES = (
        (RELAY, 'Relay'),
        (SENSOR, 'Sensor'),
    )
    api_key = models.ForeignKey('apikey.APIKey', on_delete=models.SET_NULL, null=True, blank=True, help_text=u"API_KEY")
    type = models.IntegerField(choices=DEVICE_TYPE_CHOICES, default=RELAY, help_text="type")
    name = models.CharField(max_length=30, help_text="Device name")
    pin = models.CharField(max_length=3, help_text="PIN value from V0 to V50", choices=[(f'V{i}', f'V{i}') for i in range(51)])
    unit = models.CharField(max_length=20, help_text="Unit of measurement", blank=True)  
    value = models.CharField(max_length=20, default='0', help_text="Value of the sensor")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        """
        Return Device Name and Private Key
        """
        return "{}-{}".format(self.name, self.pk)
