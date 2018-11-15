"""
Celery
"""
from __future__ import absolute_import
from datetime import timedelta
import os
from django.conf import settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ims.settings')

app = Celery('ims')
app.config_from_object('ims.celeryconfig')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'run-all-checks': {
        'task': 'core.tasks.debug_task',
        'schedule': timedelta(seconds=60),
    },
    # 'update-shifts': {
    #     'task': 'cabot.cabotapp.tasks.update_shifts',
    #     'schedule': timedelta(seconds=1800),
    # },
    # 'clean-db': {
    #     'task': 'cabot.cabotapp.tasks.clean_db',
    #     'schedule': timedelta(seconds=60 * 60 * 24),
    # },
}