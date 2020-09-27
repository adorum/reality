import os
from celery import Celery
from . import celeryconfig

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reality.settings')

app = Celery('reality_worker', include=['reality_worker.tasks'])
app.config_from_object(celeryconfig)


