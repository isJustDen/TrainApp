#файл training_history,py
from types import NoneType

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button.button import theme_text_color_options
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.tab.tab import MDTabsScrollView

from model.data import session
from model.storage import load_all_sessions


class TrainingHistoryScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Основной контейнер для всех элементов экрана
        self.layout = MDBoxLayout(orientation = 'vertical', spacing = 10, padding = 20)

        # Заголовок экрана
        self.title = MDLabel(text = 'История тренировок', halign = 'center', font_style = 'H5')
        self.layout.add_widget(self.title)

        # Область для прокрутки списка тренировок
        self.scroll = MDTabsScrollView()

        # Контейнер для элементов истории тренировок
        self.history_list = MDBoxLayout(orientation = 'vertical', size_hint_y = None)
        self.history_list.bind(minimum_height = self.history_list.setter('height'))
        self.scroll.add_widget(self.history_list)
        self.layout.add_widget(self.scroll)

        # Кнопка возврата в главное меню
        back_btn = MDRaisedButton(text = 'Назад', pos_hint ={'center_x': 0.5})
        back_btn.bind(on_release = self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        """Вызывается перед открытием экрана"""
        self.refresh_history()

    def refresh_history(self):
        """Обновляет список тренировок"""
        self.history_list.clear_widgets()

        # Загружаем все сохраненные тренировки
        sessions = load_all_sessions()

        # Если тренировок нет - показываем сообщение
        if not sessions:
            no_data_label = MDLabel(text = 'Нет сохраненных тренировок', halign = 'center', theme_text_color = 'Secondary')
            self.history_list.add_widget(no_data_label)
            return

        # Показываем тренировки в обратном порядке (свежие сверху)
        for session_data in reversed(sessions):
            # Формируем текст для отображения
            session_type = session_data.get('type', 'Неизвестный тип')
            timestamp = session_data.get('timestamp', 'Без даты')

            display_type = str(session_type).capitalize() if session_type else 'Неизвестный тип'
            text = f'[{timestamp}] {display_type}\n'

            # Добавляем список упражнений
            exercises = session_data.get('exercises', [])
            if  exercises:
                for ex in exercises:
                    name = ex.get('name', 'Без названия')
                    sets = ex.get('sets', '?')
                    reps = ex.get('reps', '?')
                    text += f" - {name} ({sets}×{reps})\n"
            else:
                 text += '- Нет упражнений\n'

                # Создаем элемент списка

            item_label = MDLabel(text = text.strip(),halign = 'left',theme_text_color = 'Primary',size_hint_y = None,height = 100 if exercises else 40)
            self.history_list.add_widget(item_label)

    def go_back(self, instance):
        """Возврат в главное меню"""
        self.manager.current = 'main_menu'