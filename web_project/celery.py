import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
# this is also used in manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project.settings')


app = Celery('celery_jobs')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.broker_url = 'redis://0.0.0.0:6379/0'
app.conf.result_backend = 'redis://0.0.0.0:6379/0'
