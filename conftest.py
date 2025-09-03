import sys
import os
import django
from pathlib import Path

def pytest_configure():
    """Принудительная настройка Django перед всеми тестами"""
    
    # Находим корневую директорию проекта
    root_dir = Path(__file__).parent
    
    # Добавляем ВСЕ возможные пути
    sys.path.insert(0, str(root_dir))
    
    # Рекурсивно ищем папки с приложениями
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            if dirname in ['tasks', 'labels', 'accounts']:
                sys.path.insert(0, os.path.join(dirpath, dirname))
    
    # Принудительно настраиваем Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    django.setup()
pytest_plugins = ['pytest_django']