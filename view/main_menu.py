# ФАЙЛ main_menu.py

from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

class MainMenuScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # область кнопок и названия
        layout = MDBoxLayout(orientation = 'vertical', spacing = 20, padding =20)

        # Название основного приложения в главном меню
        layout.add_widget(MDLabel(text = 'Добро пожаловать на тренировку!', halign = 'center', font_style = 'H5'))

        # Кнопка "Начать тренировку"
        start_button = MDRaisedButton(text = 'Начать тренировку', pos_hint={'center_x' : 0.5})
        start_button.bind(on_release=self.go_to_training_type)
        layout.add_widget(start_button)

        # Кнопка "История"
        history_btn = MDRaisedButton(text='История', pos_hint ={'center_x': 0.5})
        history_btn.bind(on_release = self.go_to_history)
        layout.add_widget(history_btn)

        # Кнопка "Настройки"
        layout.add_widget(MDRaisedButton(text = 'Настройки', pos_hint = {'center_x':0.5}))

        #Кнопка "Статистика"
        stats_button = MDRaisedButton(text = 'Статистика', pos_hint = {'center_x': 0.5})
        stats_button.bind(on_release = self.go_to_stats)
        layout.add_widget(stats_button)

        self.add_widget(layout)

    def go_to_training_type(self, instance):
        self.manager.current = 'training_type'

    def go_to_history(self, instance):
        self.manager.current = 'training_history'

    def go_to_stats(self, instance):
        self.manager.current = 'training_stats'
