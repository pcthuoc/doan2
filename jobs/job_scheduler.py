import django
import logging
from datetime import datetime
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.blocking import BlockingScheduler
import time

from jobs.task import auto_van_task, check_auto_tasks, check_hengio_tasks, auto_pump_task

django.setup()

logger = logging.getLogger(__name__)


def create_scheduler():
    jobstores = {
        'default': MemoryJobStore()
    }
    executors = {
        'default': ProcessPoolExecutor()
    }
    job_defaults = {
        'coalese': True,
        'max_instances': 100,
        'misfire_grace_time': 60
    }
    scheduler = BlockingScheduler(jobstores=jobstores,
                                  executors=executors,
                                  job_defaults=job_defaults,
                                  timezone="Asia/Ho_Chi_Minh")
    return scheduler


def config_job(scheduler):
    scheduler.add_job(schedule_complete_event, 'interval', seconds=20)
    scheduler.add_job(schedule_interval_auto, 'interval', seconds=5)
    scheduler.add_job(schedule_interval_pump_event, 'interval', seconds=5)  # Thêm tác vụ 9 giây
    scheduler.add_job(schedule_van_auto, 'interval', seconds=1)
    return scheduler


def start_scheduler():
    while True:
        try:
            scheduler = create_scheduler()
            config_job(scheduler)
            scheduler.start()
        except Exception as e:
            print(f"Error: {e}")
            print("Restarting scheduler...")
            time.sleep(10)
   

def schedule_complete_event():
    #print('---task hen gio')
    # Auto start event
    epoch_time_now = int((datetime.now() - datetime(1970, 1, 1)).total_seconds())
    #print('Time: ', epoch_time_now)
    check_hengio_tasks()

def schedule_van_auto():
    #print('---task van')
    # Auto start event
    epoch_time_now = int((datetime.now() - datetime(1970, 1, 1)).total_seconds())
    #print('Time: ', epoch_time_now)
    auto_van_task()
def schedule_interval_auto():
    #print('---task auto')
    # Auto start event
    epoch_time_now = int((datetime.now() - datetime(1970, 1, 1)).total_seconds())
   # print('Time: ', epoch_time_now)
    check_auto_tasks()

def schedule_interval_pump_event():
    #print('---Start interval pump scheduler')
    # Auto start event
   # epoch_time_now = int((datetime.now() - datetime(1970, 1, 1)).total_seconds())
    auto_pump_task()

