from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from .settings import INSTALLED_APPS

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "catalyst_count.settings")

app = Celery("catalyst_count")

# Load task modules from all registered Django app configs.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.task_time_limit = 1000
# app.autodiscover_tasks()
app.autodiscover_tasks(lambda: INSTALLED_APPS)


# celery -A catalyst_count.celery worker --pool=solo -l info
