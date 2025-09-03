# setup_path.py в корне task-manager/
import sys
import os
from pathlib import Path

def setup_paths():
    """Принудительно настраивает пути для любого окружения"""
    # Находим корневую директорию
    root_dir = Path(__file__).parent
    
    # Добавляем все возможные пути
    sys.path.insert(0, str(root_dir))
    
    # Также добавляем все поддиректории
    for item in os.listdir(root_dir):
        item_path = root_dir / item
        if item_path.is_dir() and not item.startswith('.'):
            sys.path.insert(0, str(item_path))
    
    print(f"DEBUG: sys.path = {sys.path}")

# Немедленно выполняем при импорте
setup_paths()