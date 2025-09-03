import sys
import os
from pathlib import Path

# Добавляем все подпапки в sys.path
project_root = Path(__file__).parent
for item in project_root.iterdir():
    if item.is_dir() and not item.name.startswith('.'):
        sys.path.insert(0, str(item))
pytest_plugins = ['pytest_django']