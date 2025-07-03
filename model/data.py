# ФАЙЛ data.py

class TrainingSession:
    def __init__(self):
        self.type = None
        self.exercises = []

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
