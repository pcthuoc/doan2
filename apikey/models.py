from django.db import models

class APIKey(models.Model):
    """
    Model for storing API keys.
    """
    api_key = models.CharField(max_length=90, unique=True, help_text="Global API key")


    def __str__(self):
        return self.api_key
