from celery import Celery
from celery.schedules import crontab

app = Celery()



@app.task
def add():
    # Thực hiện các công việc cần thiết
    print("hihihih")