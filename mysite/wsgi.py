"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application
from os.path import join, dirname, abspath

# ---
PROJECT_DIR = dirname(dirname(abspath(__file__)))


sys.path.insert(0, PROJECT_DIR)
# ---

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = get_wsgi_application()
