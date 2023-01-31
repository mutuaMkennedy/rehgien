import os
from django.core.wsgi import get_wsgi_application
from homey.settings import base

if base.DEBUG==False:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homey.settings.prod')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homey.settings.local')

application = get_wsgi_application()
