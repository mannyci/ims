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
