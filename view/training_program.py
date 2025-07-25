# ФАЙЛ training_program.py
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from requests.compat import has_simplejson

from model.data import session
from model.exercises import load_exercise_list, save_exercise
from model.storage import save_session_to_file
from model.templates import save_template, load_templates, get_template_by_name
from view.timer_widget import TimerWidget


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

        self.reps_input = MDTextField(hint_text = 'Повторения', input_filter = lambda text, from_undo: text if text in '0123456789,' else "")
        self.reps_input.helper_text = "Введите повторения через запятую (например: 12,10,8)"
        self.reps_input.helper_text_mode = "on_focus"
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
        template_btn = MDRaisedButton(text = 'Сохранить как шаблон', pos_hint={'center_x':0.5})
        template_btn.bind(on_release = self.ask_template_name)
        self.main_layout.add_widget(template_btn)

        # Добавляем таймер
        self.timer = TimerWidget(duration = 60)
        self.main_layout.add_widget(self.timer)

        # Добавляем кнопку для выбора из шаблонов
        self.template_btn = MDRaisedButton(text = 'Добавить из шаблона', pos_hint={'center_x':0.5}, on_release = self.open_template_menu)
        # Инициализируем меню шаблонов
        self.template_menu = None
        self.init_template_menu()

        # Область для кнопок быстрого добавления популярных упражнений
        self.quick_add_layout = MDBoxLayout(orientation = 'horizontal', size_hint_y = None, height = 50)
        self.main_layout.add_widget(self.quick_add_layout)

        # Кнопки быстрого добавления популярных упражнений
        popular_exercises = ["Приседания", "Отжимания", "Подтягивания"]
        for ex in popular_exercises:
            btn = MDFlatButton(text = ex, on_release = lambda x, e = ex: self.add_quick_exercise(e))
            self.quick_add_layout.add_widget(btn)

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
        reps_input = self.reps_input.text.strip() # Получаем строку с повторениями
        sets_input = self.sets_input.text.strip()

        if not all([name, reps_input, sets_input]):
            print("Заполните все поля")
            return

        try:
            # Обрабатываем повторения (может быть одно число или несколько через запятую)
            reps_list = []
            for r in reps_input.split(','):
                r_clean = r.strip()
                if r_clean.isdigit():
                    reps_list.append(int(r_clean))

            if not reps_list:
                print("Введите хотя бы одно корректное число повторений")
                return

            # Обрабатываем подходы (должно быть одно число)
            sets = int(sets_input)

            print(f"Добавляем упражнение: {name}, {reps_list} повторений, {sets} подходов")

            # Сохраняем в сессию (передаем список повторений и число подходов)
            session.add_exercise(name, reps_list, sets)

            # Очищаем поля ввода
            self.name_input.text = ''
            self.reps_input.text = ''
            self.sets_input.text = ''

            self.refresh_list()
        except ValueError as e:
            print(f'Ошибка ввода: {e}')

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
            'on_release': lambda x=name: self.set_exercise_name(x)
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
        self.menu.dismiss()

    def open_menu(self, instance, value):
        """Открывает меню при фокусе на поле ввода"""
        if value:
            self.menu.open()

    def refresh_list(self):
            self.exercise_list.clear_widgets()
            for ex in session.exercises:
                # Форматируем повторения для отображения
                reps_str = ', '.join(map(str, ex['reps']))
                ex_label = MDLabel(
                    text = f"{ex['name']} - {ex['sets']}×{reps_str}",
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
    def init_template_menu(self):
        """Инициализирует меню с шаблонами упражнений"""
        templates = load_templates()
        menu_items = []

        for template in templates:
            menu_items.append({
                'text':template['name'],
                'viewclass': 'OneLineListItem',
                'on_release': lambda x=template: self.add_template_exercises(x)
            })

        self.template_menu = MDDropdownMenu(caller = self.template_btn, items = menu_items, width_mult = 4)
        menu_items.append({
            'text': template['name'],
            'viewclass': 'OneLineIconListItem',
            'icon': 'dumbbell',
            'on_release': lambda x=template: self.add_template_exercises(x)
        })
    def open_template_menu(self, instance):
        """Открывает меню с шаблонами"""
        self.template_menu.open()

    def add_template_menu(self, template):
        """Добавляет упражнения из выбранного шаблона"""
        for ex in template('exercises'):
            session.add_exercise(ex['name'], ex['reps'], ex['sets'])
            self.refresh_list()
            self.template_menu.dismiss()

    def edit_template(self, template_name):
        """Редактирование шаблона"""
        template = get_template_by_name(template_name)
        if template:
            self.load_template(template)
            # Переходим в режим редактирования
            self.edit_mode = True
            self.current_template = template_name
    #--------------------------------------------------------------------------------------------------------------#
    def add_quick_exercise(self, name):
        """Быстрое добавление популярного упражнения"""
        self.name_input.text = name
        self.reps_input.text = '12, 10, 8'
        self.sets_input.text = '3'
#--------------------------------------------------------------------------------------------------------------#
    def add_template_exercises(self , template):
        """Добавляет упражнения из выбранного шаблона в текущую тренировку"""
        # Проверяем, что шаблон содержит упражнения
        if 'exercises' not in template:
            print("Шаблон не содержит упражнений")
            return

        # Добавляем каждое упражнение из шаблона
        for exercise in template['exercises']:
            name = exercise.get('name', '')
            reps = exercise.get('reps', [])
            sets = exercise.get('sets', 1)

            session.add_exercise(name, reps, sets) # Добавляем упражнение в текущую сессию

            self.refresh_list()     # Обновляем список упражнений на экране

            # Закрываем меню шаблонов
            if hasattr(self, 'template_menu'):
                self.template_menu.dismiss()
#--------------------------------------------------------------------------------------------------------------#

