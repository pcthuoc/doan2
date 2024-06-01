from django.apps import AppConfig
import os

class JobsConfig(AppConfig):
    name = 'jobs'
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'jobs')  # Đường dẫn tương đối
