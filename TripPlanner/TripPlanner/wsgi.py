"""
WSGI config for TripPlanner project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""
'''
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TripPlanner.settings")

application = get_wsgi_application()

'''

import os
import sys
sys.path.append('/opt/bitnami/projects/Win24-Team19/TripPlanner')
os.environ.setdefault("PYTHON_EGG_CACHE", '/opt/bitnami/projects/Win24-Team19/TripPlanner/egg_cache')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'TripPlanner.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
