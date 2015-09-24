from __future__ import absolute_import, unicode_literals

import os
from django.conf import settings
from celery import Celery

__author__ = 'kenneth'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whatapp.settings')

app = Celery('whatapp')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)