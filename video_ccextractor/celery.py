from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_ccextractor.settings')

# Create an instance of Celery application.
app = Celery('video_ccextractor')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Optionally, configure additional settings for Celery
# Example: Set default task queue (if not using default)
# app.conf.task_default_queue = 'default'

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
