import setup_path  # ← обязательно первой строкой!

import pytest
import django
import os

def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')
    django.setup()