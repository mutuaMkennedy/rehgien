#!/usr/bin/env python
import os
import sys
from homey.settings import base

if __name__ == '__main__':
    if base.DEBUG==False:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homey.settings.prod')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homey.settings.local')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
