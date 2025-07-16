#файл training_history,py
import json
import os.path
from types import NoneType

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.button.button import theme_text_color_options
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.tab.tab import MDTabsScrollView

from model.data import session
from model.storage import load_all_sessions

#**********************************************************************************************************************#
class TrainingHistoryScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # -------------------------------------------------------------------------------------------------------------№
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

            ##Отображает основную информацию: дату, тип тренировки и список упражнений для повтора тренировки или удаления
            height = 80 +len(exercises) * 30 ## Динамический расчет высоты

            card = MDCard(orientation = 'vertical', padding = 10, size_hint_y = None, height = height if exercises  else 60 )
            label = MDLabel(text = text.strip(), halign = 'left', theme_text_color = 'Primary')

            repeat_btn = MDFlatButton(text = 'Повторить', pos_hint = {'right': 1})
            repeat_btn.bind(on_release = lambda btn , data = session_data: self.repeat_session(data))

            delete_btn = MDFlatButton(text = 'Удалить', pos_hint = {'right': 1})
            delete_btn.bind(on_release = lambda btn, data = session_data: self.delete_session(data))

            btn_box = MDBoxLayout(orientation = 'horizontal', size_hint_y = None, height = 40, spacing = 10, padding = 10)
            btn_box.add_widget(repeat_btn)
            btn_box.add_widget(delete_btn)

            card.add_widget(label)
            card.add_widget(btn_box)

            self.history_list.add_widget(card)

    #Логика для повторения уже существующей тренировки
    def repeat_session(self, data):
        """Загружает старую тренировку и переходит на экран повторения"""
        session.reset()
        session.set_type(data.get("type"))

        for ex in data.get('exercises', []):
            name = ex.get('name', 'Без названия')
            sets = ex.get('sets', 0)
            reps = ex.get('reps', 0)
            session.add_exercise(name, reps, sets)

        print(f"🔁 Повторяем тренировку: {session}")
        self.manager.current = 'training_program'

    # Логика для возврата домой(главное меню)
    def go_back(self, instance):
        """Возврат в главное меню"""
        self.manager.current = 'main_menu'

    def delete_session(self, data_to_delete):
        """Удаляет тренировку из истории и обновляет экран"""
        path = 'data/training_history.json'
        if not os.path.exists(path):
            print("❌ Файл истории не найден.")
            return

        try:
            # Читаем файл один раз
            with open(path, 'r', encoding='utf-8') as f:
                # Удаляем по полному совпадению структуры
                all_sessions = json.load(f)

            # Фильтруем тренировки
            updated_sessions = [s for s in all_sessions if s != data_to_delete]

            # Записываем обратно
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(updated_sessions, f, ensure_ascii=False, indent=4)

            print("✅Тренировка удалена")
            self.refresh_history()

        except Exception as e:
            print(f"❌Ошибка при удалении: {e}")

