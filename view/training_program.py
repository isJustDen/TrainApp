# ФАЙЛ training_program.py
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField

from model.data import session
from model.exercises import load_exercise_list, save_exercise
from model.storage import save_session_to_file
from model.templates import save_template


#**********************************************************************************************************************#
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
        self.main_layout.add_widget(self.name_input)

        self.reps_input = MDTextField(hint_text = 'Повторения (reps)', input_filter = 'int')
        self.main_layout.add_widget(self.reps_input)

        self.sets_input = MDTextField(hint_text = 'Подходы (sets)', input_filter = 'int')
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

        #Кнопка сохранения в шаблон
        template_btn = MDRaisedButton(text = '💾 Сохранить как шаблон', pos_hint={'center_x':0.5})
        template_btn.bind(on_release = self.ask_template_name)
        self.main_layout.add_widget(template_btn)

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

        # Текстовое поле
        exercise_name_input = MDTextField(
            hint_text='Название упражнения',
            mode='rectangle'
        )
        # Загружаем список упражнений
        exercise_names = load_exercise_list()

        # Создаём выпадающее меню
        menu_items = [{
            'text': name,
            'viewclass': 'OneLineListItem',
            'on_release': lambda x=name: set_exercise_name(x)
        }
            for name in exercise_names
        ]

        menu = MDDropdownMenu(
            caller=exercise_name_input,
            items=menu_items,
            width_mult=4
        )

        exercise_name_input.bind(on_focus=lambda instance, value: menu.open() if value else None)
        if name:
            save_exercise(name) # Сохраняем в справочник упражнений

        self.init_exercise_dropdown()

    def init_exercise_dropdown(self):
        """Инициализирует выпадающий список упражнений"""
        exercise_names = load_exercise_list()

        menu_items = [{
            'text':name,
            'viewclass': 'OneLineListItem',
            'on_release': lambda x=name: self.set_exercise_name(x)
        } for name in exercise_names]

        self.menu = MDDropdownMenu(
            caller = self.name_input,
            items = menu_items,
            width_mult = 4
        )
        self.name_input.bind(on_focus = self.open_menu)

    def set_exercise_name(self, name):
        """Устанавливает выбранное упражнение в поле ввода"""
        self.name_input.text = name
        self.menu.dismiss()

    def open_menu(self, instance, value):
        """Открывает меню при фокусе на поле ввода"""
        if value:
            self.menu.open()

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

    def ask_template_name(self, instance):
        """Запрашивает у пользователя имя шаблона и сохраняет его"""
        content = MDBoxLayout(orientation = 'vertical', spacing = 10, size_hint_y=None, height=60)
        text_field = MDTextField(hint_text = 'Название шаблона')
        content.add_widget(text_field)

        dialog = MDDialog(
            title = 'Сохранить как шаблон',
            type = 'custom',
            content_cls = content,
            buttons = [
                MDFlatButton(text = 'ОТМЕНА', on_release = lambda x: dialog.dismiss()),
                MDRaisedButton(text = 'Сохранить', on_release = lambda x: self._save_template_name(text_field, dialog))
            ]
                          )
        dialog.open()

    def _save_template_name(self, text_field, dialog):
        """Обрабатывает сохранение шаблона"""
        name = text_field.text.strip()
        if name:
            save_template(name)
            dialog.dismiss()
        else:
            text_field.error = True
            text_field.helper_text = 'Введите имя шаблона'

#--------------------------------------------------------------------------------------------------------------#
