import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homey.settings.prod') #change this to match environment

application = get_wsgi_application()
