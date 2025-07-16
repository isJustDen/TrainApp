# файл templates.py
import json
import os
from datetime import datetime

from model.data import session

TEMPLATE_FILE = 'data/training_templates.json'

def save_template(template_name: str):
    """Сохраняет текущую тренировку в файл шаблонов с заданным именем"""
    os.makedirs('data', exist_ok=True)

    new_template = {'name': template_name,
                    'type': session.type,
                    'exercises': session.exercises,
                    'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    if os.path.exists(TEMPLATE_FILE):
        with open(TEMPLATE_FILE, 'r', encoding='UTF-8') as f:
            templates = json.load(f)
    else:
        templates = []

    templates.append(new_template)

    with open(TEMPLATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(templates, f, ensure_ascii=False, indent=4)

    print(f'✅ Шаблон "{template_name}" сохранен')

def load_templates():
    """Загружает все шаблоны тренировок из файла """
    if os.path.exists(TEMPLATE_FILE):
        with open(TEMPLATE_FILE, 'r', encoding= 'UTF-8') as f:
            return json.load(f)
    return []