from django.db import models
from multiselectfield import MultiSelectField

class Hengio(models.Model):
    ON = 1
    OFF = 2
    VALUE_TYPE_CHOICES = (
        (ON, 'On'),
        (OFF, 'Off'),
    )

    DAYS_OF_WEEK_CHOICES = [
        (0, 'Hai'),
        (1, 'Ba'),
        (2, 'Tư'),
        (3, 'Năm'),
        (4, 'Sáu'),
        (5, 'Bảy'),
        (6, 'Chủ Nhật'),
    ]

    api_key = models.CharField(max_length=30, help_text="Device API Key")
    pin = models.CharField(max_length=3, help_text="PIN value from V0 to V50")
    name = models.CharField(max_length=30, help_text="Device name")
    status = models.IntegerField(choices=VALUE_TYPE_CHOICES, default=ON, help_text="Value of the sensor")
    value = models.IntegerField(choices=VALUE_TYPE_CHOICES, default=ON, help_text="Type")
    time = models.TimeField(help_text="Time to trigger the event")
    days_of_week = MultiSelectField(
        choices=DAYS_OF_WEEK_CHOICES,
        default=[0, 1, 2, 3, 4, 5, 6],
        max_choices=7,  
        max_length=13, 
        help_text="Days of the week when the event should trigger"
    )

    def __str__(self):
        return f"{self.name} - {self.get_value_display()} at {self.time} on {self.get_days_of_week_display()}"

    class Meta:
        verbose_name_plural = "Hengios"
