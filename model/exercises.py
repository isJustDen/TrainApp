# exercises.py file
import json
import os

EXERCISE_FILE = 'data/exercises.json'

#	Возвращает список всех упражнений
def load_exercise_list():
    """Загружает список упражнений из файла"""
    if os.path.exists(EXERCISE_FILE):
        with open(EXERCISE_FILE, 'r', encoding='UTF-8') as f:
            return json.load(f)
    return []

#Добавляет упражнение в справочник, если его нет
def save_exercise(name: str):
    """Сохраняет новое упражнение, если его ещё нет"""
    name = name.strip().capitalize()
    if not name:
        return

    exercises = load_exercise_list()
    if name not in exercises:
        exercises.append(name)
        with open(EXERCISE_FILE, 'w', encoding="UTF-8") as f:
            json.dump(exercises, f, ensure_ascii=False, indent=4)
        print(f"✅ Упражнение '{name}' добавлено в справочник.")

