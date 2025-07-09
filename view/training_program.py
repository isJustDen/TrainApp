# ФАЙЛ training_program.py

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField

from model.data import session
from model.storage import save_session_to_file


class TrainingProgramScreen(MDScreen):
    def __init__ (self, **kwargs):
        super().__init__(**kwargs)

        self.main_layout = MDBoxLayout(orientation = 'vertical', spacing = 10, padding = 20)

        self.header = MDLabel(
            text = f'Тренировка: {session.type}',
            halign = 'center',
            font_style = 'H5'
        )
        self.main_layout.add_widget(self.header)
        # Поля для ввода упражнения
        self.name_input = MDTextField(hint_text = "Название упражнения")
        self.reps_input = MDTextField(hint_text = 'Повторения (reps)', input_filter = 'int')
        self.sets_input = MDTextField(hint_text = 'Подходы (sets)', input_filter = 'int')

        self.main_layout.add_widget(self.name_input)
        self.main_layout.add_widget(self.reps_input)
        self.main_layout.add_widget(self.sets_input)

        # Кнопка добавить
        add_btn = MDRaisedButton(text = 'Добавить упражнения', pos_hint = {'center_x': 0.5})
        add_btn.bind(on_release = self.add_exercise)
        self.main_layout.add_widget(add_btn)

        # Список добавленных упражнений
        self.exercise_list = MDBoxLayout(orientation = 'vertical', size_hint_y =None)
        self.exercise_list.bind(minimum_height = self.exercise_list.setter('height'))

        scroll = MDScrollView()
        scroll.add_widget(self.exercise_list)
        self.main_layout.add_widget(scroll)

        # Кнопка сохранить (пока просто лог)
        save_btn = MDRaisedButton(text = 'Сохранить тренировку', pos_hint = {'center_x' :0.5})
        save_btn.bind(on_release = self.save_session)
        self.main_layout.add_widget(save_btn)

        back_btn = MDRaisedButton (text = 'Назад к истории', pos_hint = {'center_x': 0.5})
        back_btn.bind(on_release = self.go_back)
        self.main_layout.add_widget(back_btn)

        self.add_widget(self.main_layout)

    def on_pre_enter(self, *args):
        if not session.type:
            self.manager.current = 'training_type'
            return
        # Обновим заголовок и список при входе
        self.header.text = f'Тренировка: {session.type}'
        self.refresh_list()

    def add_exercise(self, instance):
            name = self.name_input.text.strip()
            reps = self.reps_input.text.strip()
            sets = self.sets_input.text.strip()

            if name and reps and sets:
                print(f"Добавляем упражнение: {name}, {reps} повторений, {sets} подходов")
                session.add_exercise(name, int(reps), int(sets))
                self.name_input.text = ''
                self.reps_input.text = ''
                self.sets_input.text = ''
                self.refresh_list()

    def refresh_list(self):
            self.exercise_list.clear_widgets()
            for ex in session.exercises:
                ex_label = MDLabel(
                    text = f"{ex['name']} - {ex['sets']}×{ex['reps']}",
                    halign = 'left'
                )
                self.exercise_list.add_widget(ex_label)

    def save_session(self, instance):
        print(f'Тренировка сохранена: {session}')
        save_session_to_file()
        self.refresh_list()

    def go_back(self, instance):
        self.manager.current  = 'training_history'