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

    def add_exercise(self, name, reps, sets):
        self.exercises.append({
            'name': name,
            'reps': reps,
            'sets': sets
        })

    def reset(self):
        self.type = None
        self.exercises = []

    def __repr__(self):
        return f'<Тренировка: {self.type}, {len(self.exercises)} упражнений>'

session = TrainingSession()
print("Загруженные тренировки:", session)