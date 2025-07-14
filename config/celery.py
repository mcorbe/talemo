"""
Celery configuration for the Talemo project.
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Create the Celery app
app = Celery('talemo')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Configure the Celery Beat schedule
app.conf.beat_schedule = {
    # No scheduled tasks
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """
    Debug task to verify Celery is working.
    """
    print(f'Request: {self.request!r}')
