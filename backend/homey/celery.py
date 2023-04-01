import os
from celery import Celery
from homey.settings import base

# set the default Django settings module for the 'celery' program.
if base.DEBUG==False:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homey.settings.prod')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homey.settings.local')

app = Celery('homey',
             broker='redis://',
             backend='rpc://'
             )

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
