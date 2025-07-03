import json
import os
from datetime import datetime
from model.data import session

# 📁 Папка для хранения данны
DATA_FILE = 'data/training_history.json'

# ✅ Сохранение текущей тренировки
def save_session_to_file():
    os.makedirs('data', exist_ok = True)

    session_data = {
        'type': session.type,
        'exercises': session.exercises,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding= 'UTF-8') as f:
                all_sessions = json.load(f)
        else:
            all_sessions = []

        all_sessions.append(session_data)

        with open(DATA_FILE, 'w', encoding = 'utf-8') as f:
            json.dump(all_sessions, f, ensure_ascii=False, indent = 4)

        print("✅ Тренировка сохранена в файл.")
        session.reset()

    except Exception as e:
        print(f"❌ Ошибка при сохранении: {e}")
