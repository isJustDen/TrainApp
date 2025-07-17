# ФАЙЛ data.py
from datetime import datetime

#**********************************************************************************************************************#

class TrainingSession:
    def __init__(self):
        self.type = None
        self.exercises = []
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            'type': self.type,
            'exercises': [ex for ex in self.exercises],
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        session = cls()
        session.type = data.get('type')
        session.exercises = data.get('exercises', [])
        session.timestamp = data.get('timestamp')
        return session

    def set_type(self, training_type):
        self.type = training_type

    def add_exercise(self, name: str, reps, sets:int):
        """Добавляет упражнение в тренировку
        - reps: строка вида "15,12,8"
        - преобразуется в список: [15,12,8]
        """

        # Проверяем и нормализуем reps
        if isinstance(reps, (int, float)):
            reps_list = [int(reps)]
        # Если reps - строка, пытаемся разбить по запятым
        elif isinstance(reps, str):
            reps_list = [int(r.strip()) for r in reps.split(',') if r.strip().isdigit()]
        # Если reps уже список - оставляем как есть
        elif isinstance(reps, (list, tuple)):
            reps_list = [int(r) for r in reps]
        else:
            reps_list = [0]  # Значение по умолчанию

        # Проверяем sets
        try:
            sets_num = int(sets)
        except(ValueError, TypeError):
            sets_num = 1 # Значение по умолчанию

        self.exercises.append({
            'name': name,
            'reps': reps_list,
            'sets': sets_num
        })

    def reset(self):
        self.type = None
        self.exercises = []

    def __repr__(self):
        return f'<Тренировка: {self.type}, {len(self.exercises)} упражнений>'

session = TrainingSession()
print("Загруженные тренировки:", session)