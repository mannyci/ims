"""
Celery
"""
from __future__ import absolute_import

import os
from django.conf import settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ims.settings')

app = Celery('ims')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug(self):
    print('Request: {0!r}'.format(self.request))