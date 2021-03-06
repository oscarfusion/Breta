from __future__ import absolute_import

import os

from celery import Celery, schedules

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'breta.settings')

app = Celery('breta')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
