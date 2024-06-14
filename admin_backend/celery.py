from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_backend.settings')

app = Celery('admin_backend')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'update-coin-information': {
        'task': 'admin_backend.tasks.updateCoinInfo',
        'schedule': 300,  # runs every 1 second
    },
}

app.autodiscover_tasks(['admin_backend'])