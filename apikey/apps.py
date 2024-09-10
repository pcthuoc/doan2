from django.apps import AppConfig

class ApikeyConfig(AppConfig):
    name = 'apikey'
    def ready(self):
        import apikey.signals 

