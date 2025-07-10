# training_stats.py файл
from collections import defaultdict

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView

from model.data import session
from model.storage import load_all_sessions


class TrainingStatsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 🔲 Основной вертикальный макет
        self.layout = MDBoxLayout(orientation = 'vertical', padding = 20, spacing = 10)

        # 🏷 Заголовок
        self.title = MDLabel(text = '📊Статистика тренировок', halign = 'center', font_style = 'H5')
        self.layout.add_widget(self.title)

        # 🔃 Область с прокруткой
        self.scroll = MDScrollView()
        self.stats_box = MDBoxLayout(orientation = 'vertical', size_hint_y = None)
        self.stats_box.bind(minimum_height = self.stats_box.setter('height'))
        self.scroll.add_widget(self.stats_box)

        self.layout.add_widget(self.scroll)

        # 🔙 Кнопка возврат
        back_btn = MDRaisedButton(text = 'Назад', pos_hint = {'center_x': 0.5})
        back_btn.bind(on_release = self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        """Перед входом обновляем статистику"""
        self.refresh_stats()

    def refresh_stats(self):
        """Читает файл истории и подсчитывает количество подходов по датам"""
        self.stats_box.clear_widgets()

        sessions = load_all_sessions()

        if not sessions:
            self.stats_box.add_widget(MDLabel(text = 'Нет данных для анализа', halign = 'center', theme_text_color = 'Secondary'))
            return

        # Используем словарь: дата -> общее количество подходов
        stats = defaultdict(int)

        for session in sessions:
            date_str = session.get('timestamp', '').split(' ')[0]
            for ex in session.get('exercises', []):
                sets = int(ex.get('sets', '0'))
                stats[date_str] += sets

            # Сортировка по дате (свежие сверху)
            for data in sorted(stats.keys(), reverse = True):
                total_sets = stats[data]
                self.stats_box.add_widget(MDLabel(text = f'{data}: {total_sets} подходов',
                                                  halign = 'left',
                                                  theme_text_color = 'Primary'
                ))

    def go_back(self, instance):
        '''Возврат на главное меню'''
        self.manager.current = 'main_menu'


