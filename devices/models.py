# devices/models.py

from django.db import models
from django.contrib.auth.models import User
from apikey.models import APIKey

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
    api_key = models.ForeignKey(APIKey, on_delete=models.SET_NULL, null=True, blank=True, help_text="API_KEY")
    type = models.IntegerField(choices=DEVICE_TYPE_CHOICES, default=RELAY, help_text="type")
    name = models.CharField(max_length=30, help_text="Device name")
    pin = models.CharField(max_length=3, help_text="PIN value from V0 to V50", choices=[(f'V{i}', f'V{i}') for i in range(51)])
    unit = models.CharField(max_length=20, help_text="Unit of measurement", blank=True)
    value = models.CharField(max_length=20, default='0', help_text="Value of the sensor")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        """
        Return Device Name and Private Key
        """
        return "{}-{}".format(self.name, self.pk)

    def save(self, *args, **kwargs):
        """
        Override save method to automatically assign APIKey for the user.
        """
        if self.user and not self.api_key:
            # Retrieve or create the APIKey for the user
            try:
                self.api_key = APIKey.objects.get(user=self.user)
            except APIKey.DoesNotExist:
                # Optionally handle the case where the API key does not exist
                pass
        super().save(*args, **kwargs)
