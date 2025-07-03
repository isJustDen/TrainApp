# ФАЙЛ training_type

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel

from model.data import session


class TrainingTypeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation = 'vertical', spacing = 20, padding = 20)

        layout.add_widget(MDLabel(text = 'Выберите тип тренировки', halign = 'center', font_style = 'H5'))

        # Кнопки выбора типа тренировки
        house_btn = MDRaisedButton(text = 'ДОМ', pos_hint = {'center_x':0.5})
        house_btn.bind(on_release = lambda x: self.select_type('домашняя'))

        gym_btn = MDRaisedButton(text='ЗАЛ', pos_hint={'center_x': 0.5})
        gym_btn.bind(on_release = lambda x: self.select_type('зал'))

        custom_btn = MDRaisedButton(text='СВОЯ', pos_hint={'center_x': 0.5})
        custom_btn.bind(on_release = lambda  x: self.select_type('своя'))

        back_btn = MDRaisedButton(text = 'НАЗАД', pos_hint = {'center_x': 0.5})
        back_btn.bind(on_release = self.go_back)

        layout.add_widget(house_btn)
        layout.add_widget(gym_btn)
        layout.add_widget(custom_btn)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current  = 'main_menu'

    def select_type(self, training_type):
        session.set_type(training_type)
        print(f'Тип тренировки выбран: {session.type}')
        self.manager.current = 'training_program'