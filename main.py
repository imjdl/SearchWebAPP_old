# coding=utf-8
import sys
import os
from django.core.management import execute_from_command_line
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute_from_command_line(['manage.py', 'runserver', '80'])
