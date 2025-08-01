# ФАЙЛ training_program.py
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.button.button import theme_text_color_options
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivy.utils import platform
from pygame.examples.scroll import scroll_view

from model.data import session
from model.exercises import load_exercise_list, save_exercise
from model.storage import save_session_to_file
from model.templates import save_template, load_templates, get_template_by_name
from view.timer_widget import TimerWidget

#**********************************************************************************************************************#
class TrainingProgramScreen(MDScreen):
    def __init__ (self, **kwargs):
        super().__init__(**kwargs)

        # Проверяем мобильную платформу
        if platform in ('android', 'ios'):
            self.mobile_adjustments()

        # Главный макет с прокруткой
        self.main_layout = MDBoxLayout(
            orientation = 'vertical',
            spacing = dp(5),
            padding = [dp(10), dp(10), dp(10), dp(10)]
        )

        # 1. Основной ScrollView для всего содержимого
        self.scroll = MDScrollView()
        self.content_layout = MDBoxLayout(
            orientation = 'vertical',
            spacing = dp(0),
            size_hint_y = None,
            padding = [dp(10), dp(10), dp(10), dp(10)]) # Отступ снизу для нижней панели
        self.content_layout.bind(minimum_height = self.content_layout.setter('height'))


        # 2. Заголовок
        self.header = MDLabel(
            text = f'Тренировка: {session.type}',
            halign = 'center',
            font_style = 'H5',
            size_hint_y = None,
            height = dp(30)
        )
        self.main_layout.add_widget(self.header)


        # 3. Поля для ввода упражнения
        self.input_layout = MDBoxLayout(
            orientation = 'vertical',
            spacing = dp(5),
            size_hint_y = None,
            height =  dp(0)
        )
        self.name_input = MDTextField(hint_text = "Название упражнения")
        self.reps_input = MDTextField(
            hint_text = 'Повторение',
            input_filter = lambda text, from_undo: text if text in "0123456789," else "",
            helper_text = 'Введите повторения через запятую (Например: 12-10-8)',
            helper_text_mode = 'on_focus',)
        self.sets_input = MDTextField(hint_text ='Подходы (sets)', input_filter = 'int')

        self.main_layout.add_widget(self.name_input)
        self.main_layout.add_widget(self.reps_input)
        self.main_layout.add_widget(self.sets_input)
        self.content_layout.add_widget(self.input_layout)


        #4. Кнопки действий
        self.action_buttons_layout = MDBoxLayout(
            orientation = 'horizontal',
            spacing = dp(25),
            size_hint_y = None,
            height=dp(48), # Фиксированная высота для 3 кнопок
            padding = [dp(5), 0, dp(5), 0]  #Небольшие отступы по бокам
        )
        # Кнопка добавления
        self.add_btn = MDRaisedButton(
            text = 'Добавить',
            size_hint=(None, 1),
            width=dp(60),
            height=dp(48)
        )
        self.add_btn.bind(on_release = self.add_exercise)


        # Кнопка быстрого добавления
        self.quick_add_btn = MDRaisedButton(
            text = 'Быстрое добавление',
            size_hint = (None, 1),
            width=dp(60),
            height=dp(48)
        )
        self.quick_add_btn.bind(on_release = self.show_quick_add_options)

        self.action_buttons_layout.add_widget(self.add_btn)
        self.action_buttons_layout.add_widget(self.quick_add_btn)

        self.main_layout.add_widget(self.action_buttons_layout) # Добавляем layout с кнопками в основной макет

        # 5. Список упражнений
        self.exercise_list = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(1),
            adaptive_height = True
        )
        self.exercise_list.bind(minimum_height=self.exercise_list.setter('height'))
        self.content_layout.add_widget(self.exercise_list)

        # 6. Нижняя фиксированная панель
        self.bottom_panel = MDBoxLayout(
            orientation = 'horizontal',
            size_hint_y = None,
            height = dp(70),
            padding = [dp(10), dp(5), dp(10), dp(5)],
            spacing = dp(5)
        )
        # Таймер
        self.timer = TimerWidget(duration=60, size_hint_x=0.7)

        #контейнер для кнопок сохранить/назад
        self.save_back_layout = MDBoxLayout(
            orientation = 'horizontal',
            size_hint_x = 0.25,
            padding=[10, 0, 0, 10],
            spacing=dp(25),
            height=dp(10),
        )
        # Кнопки сохранения/назад
        self.save_btn = MDRaisedButton(
            text='Сохранить',
            size_hint_y = None,
            height=dp(28),
            font_size = '15sp'
        )
        self.save_btn.bind(on_release=self.save_session)

        self.back_btn = MDRaisedButton(
            text='Назад',
            size_hint_y=None,
            height=dp(28),
            font_size = '15sp'
        )
        self.back_btn.bind(on_release=self.go_back)

        self.save_back_layout.add_widget(self.save_btn)
        self.save_back_layout.add_widget(self.back_btn)


        self.bottom_panel.add_widget(self.timer)
        self.main_layout.add_widget(self.save_back_layout)

        # Собираем все вместе
        self.scroll.add_widget(self.content_layout)
        self.main_layout.add_widget(self.scroll)
        self.main_layout.add_widget(self.bottom_panel)
        self.add_widget(self.main_layout)

        # Инициализация меню
        self.init_template_menu()
        self.init_exercise_dropdown()


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
        """Полностью обновляет список упражнений"""
        self.exercise_list.clear_widgets() # Очищаем виджет
        for ex in session.exercises:
            # Форматируем повторения для отображения
            reps_str = ', '.join(map(str, ex['reps']))  # Изменил запятые на дефисы для лучшего вида
            ex_label = MDLabel(
                text = f"{ex['name']} - {ex['sets']}×{reps_str}",
                halign = 'left',
                size_hint_y = None,
                height = dp(40)
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

        # Создаем кнопку, которая будет вызывать меню
        self.template_btn = MDRaisedButton(
            text = 'Добавить из шаблона',
            pos_hint = {'center_x': 0.5},
            on_release = self.open_template_menu
        )
        # Создаем само меню
        self.template_menu = MDDropdownMenu(
            caller = self.template_btn,
            items = menu_items,
            width_mult = 4
        )

        # Добавляем кнопку в интерфейс
        if not hasattr(self, 'template_btn_added'):
            self.main_layout.add_widget(self.template_btn)
            self.template_btn_added = True

    def open_template_menu(self, instance):
        """Открывает меню с шаблонами"""
        if hasattr(self, 'template_menu') and self.template_menu:
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
        if hasattr(self, 'dialog'):
            self.dialog.dismiss()

#--------------------------------------------------------------------------------------------------------------#
    def add_template_exercises(self , template):
        """Добавляет упражнения из выбранного шаблона в текущую тренировку"""
        # Проверяем, что шаблон содержит упражнения
        if 'exercises' not in template:
            print("Шаблон не содержит упражнений")
            return
        session.exercises = []
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

    def mobile_adjustments(self):
        """Настройки для мобильных устройств"""
        app = MDApp.get_running_app()
        padding = app.mobile_styles['padding']
        spacing = app.mobile_styles['spacing']

        self.main_layout.padding = [padding, padding]
        self.main_layout.spacing = spacing

        # Уменьшаем размер шрифтов для мобильных устройств
        self.header.font_style = 'H6'
        for child in self.exercise_list.children:
            if isinstance(child, MDLabel):
                child.font_style = 'Body1'

#--------------------------------------------------------------------------------------------------------------#
    def calculate_action_height(self):
        '''Задаёт высоту кнопок'''
        button_height = dp(48)# Высота одной кнопк
        spacing = dp(10)# Отступ между кнопками
        padding = dp(10)*2# Внутренние отступы контейнер
        num_buttons = 3 # Количество кнопок (например: Добавить, Шаблоны, Таймер)
        return (button_height*num_buttons)+(spacing * (num_buttons-1)+padding)

#--------------------------------------------------------------------------------------------------------------#
    def show_quick_add_options(self, instance):
        # Список быстрых упражнений
        quick_exercises = [
            {'name': 'Приседания', 'reps': '12,10,8', 'sets': '3'},
            {'name': 'Отжимания', 'reps': '15,12,10', 'sets': '3'},
            {'name': 'Подтягивания', 'reps': '8,6,5', 'sets': '3'},
            {'name': 'Жим лежа', 'reps': '10,8,6', 'sets': '3'},
            {'name': 'Становая тяга', 'reps': '8,6,4', 'sets': '3'}
        ]

        # Главный контейнер
        content = MDBoxLayout(
            orientation='vertical',
            spacing='12dp',
            size_hint_y=None,
            height='400dp'  # Увеличиваем высоту для списка
        )

        # ScrollView для списка упражнений
        scroll = MDScrollView()
        exercise_list = MDBoxLayout(
            orientation='vertical',
            spacing='10dp',
            size_hint_y=None,
            adaptive_height=True
        )
        scroll.add_widget(exercise_list)
        content.add_widget(scroll)

        # Добавляем упражнения в список
        for ex in quick_exercises:
            item = MDBoxLayout(
                orientation='horizontal',
                spacing='10dp',
                size_hint_y=None,
                height='48dp'
            )

            # Кнопка добавления
            add_btn = MDFlatButton(
                text=md_icons['plus'],
                font_style="Icon",
                theme_text_color='Custom',
                text_color=(0, 0.5, 0, 1),  # Зеленый цвет
                on_release=lambda x, ex=ex: self._add_quick_exercise(ex)
            )

            # Название упражнения
            name_label = MDLabel(
                text=ex['name'],
                halign='left',
                size_hint_x=0.6
            )

            # Кнопка удаления
            del_btn = MDFlatButton(
                text=md_icons['delete'],
                font_style="Icon",
                theme_text_color='Custom',
                text_color=(0.8, 0, 0, 1),  # Красный цвет
                on_release=lambda x, ex=ex: self._remove_quick_exercise(ex)
            )

            item.add_widget(add_btn)
            item.add_widget(name_label)
            item.add_widget(del_btn)
            exercise_list.add_widget(item)

        # Кнопки диалога
        buttons = [
            MDFlatButton(
                text='Закрыть',
                on_release=lambda x: self.dialog.dismiss()
            )
        ]

        # Создаем диалог
        self.dialog = MDDialog(
            title="Быстрое добавление упражнений",
            type="custom",
            content_cls=content,
            buttons=buttons,
            size_hint=(0.9, None),
            height='500dp'
        )

        # Добавляем кнопку закрытия в заголовок
        close_btn = MDFlatButton(
            text=md_icons['close'],
            font_style="Icon",
            theme_text_color='Custom',
            text_color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=('48dp', '48dp'),
            pos_hint={'top': 1, 'right': 1},
            on_release=lambda x: self.dialog.dismiss()
        )

        if hasattr(self.dialog, 'ids') and 'container' in self.dialog.ids:
            self.dialog.ids.container.add_widget(close_btn)

        self.dialog.open()

    def _add_quick_exercise(self, exercise):
        """Добавляет выбранное упражнение в тренировку"""
        self.name_input.text = exercise['name']
        self.reps_input.text = exercise['reps']
        self.sets_input.text = exercise['sets']
        if hasattr(self, 'dialog'):
            self.dialog.dismiss()

    def _remove_quick_exercise(self, exercise):
        """Удаляет упражнение из списка быстрых (можно реализовать сохранение в настройках)"""
        # Здесь можно добавить логику удаления из сохраненного списка
        print(f"Упражнение {exercise['name']} удалено из быстрых")
        # Создаем кнопки выбора упражнений
        buttons = [
            MDFlatButton(
                text='Приседания',
                padding="12sp",

                on_release=lambda x: self.add_quick_exercise('Приседания')
            ),
            MDFlatButton(
                text='Отжимания',
                on_release=lambda x: self.add_quick_exercise('Отжимания')
            ),
            MDFlatButton(
                text='Подтягивания',
                on_release=lambda x: self.add_quick_exercise('Подтягивания')
            )
        ]

        # Добавляем кнопку закрытия (крестик)
        self.dialog = MDDialog(
            title="Быстрое добавление",
            type="custom",
            content_cls=content,
            buttons=buttons,
            size_hint=(0.8, None),


        )
        self.dialog.ids.button_close = MDFlatButton(
            text = md_icons['close'],
            font_style = "Icon",
            theme_text_color = 'Custom',
            text_color = (0, 0, 0, 1),
            size_hint = (None, None),
            size =('48dp', '48dp'),
            pos_hint = {'top': 1, 'right': 1},
            on_release = lambda x: self.dialog.dismiss()
        )

        self.dialog.ids.container.add_widget(self.dialog.ids.button_close)

        self.dialog.open()
# --------------------------------------------------------------------------------------------------------------#
    def clear_exercises(self):
        """Очищает список упражнений в текущей сессии"""
        self.exercises = []
#--------------------------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------------------------#
