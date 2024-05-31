from django.db import models
from multiselectfield import MultiSelectField

class Auto(models.Model):
    ON = 1
    OFF = 0
    VALUE_TYPE_CHOICES = (
        (ON, 'On'),
        (OFF, 'Off'),
    )
    CONTINUOUS = 1
    INTERVAL = 2
    OFF_PUMP = 2
    PUMP_TYPE_CHOICES = (
        (CONTINUOUS, 'Cozantinuous Mode (Always On)'),
        (INTERVAL, 'Interval Mode (On for 5s, Off for 5s)'),
    )
    VAN_TYPE_CHOICES = (
        (ON, 'Tu dong'),
        (OFF, 'thu cong'),
    )

    api_key = models.CharField(max_length=30,default="TEY8OO5iafAV96gRKcZohbO6ED", help_text="Device API Key")
    auto_name = models.CharField(max_length=100, help_text="Tên cây trồng")
    auto_status = models.IntegerField(choices=VALUE_TYPE_CHOICES, default=OFF, help_text="Type")

    pump_choice = models.IntegerField(choices=PUMP_TYPE_CHOICES, default=CONTINUOUS, help_text="Type")
    pump_pin = models.CharField(max_length=3,default='V0' ,help_text="PIN value from V0 to V50")
    
    van_status = models.IntegerField(choices=VAN_TYPE_CHOICES, default=ON, help_text="Type")
    van_pin = models.CharField(max_length=3, default='V3', help_text="PIN value from V0 to V50")
    
    min_ph =models.CharField(max_length=100, help_text="ph min")
    max_ph =models.CharField(max_length=100, help_text="ph max")
    ph_status = models.IntegerField(choices=VALUE_TYPE_CHOICES, default=ON, help_text="Type")
    ph_pin = models.CharField(max_length=3,default='V1' ,help_text="PIN value from V0 to V50")
    
    min_light =models.CharField(max_length=100, help_text="light min")
    light_status = models.IntegerField(choices=VALUE_TYPE_CHOICES, default=ON, help_text="Type")
    light_pin = models.CharField(max_length=3, default='V2', help_text="PIN value from V0 to V50")
    def __str__(self):
        return self.auto_name