# ФАЙЛ training_type
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel

class TrainingTypeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation = 'vertical', spacing = 20, padding = 20)

        layout.add_widget(MDLabel(text = 'Choose the type of training', halign = 'center', font_style = 'H5'))

        layout.add_widget(MDRaisedButton(text = 'House', pos_hint = {'center_x':0.5}))
        layout.add_widget(MDRaisedButton(text='GYM', pos_hint={'center_x': 0.5}))
        layout.add_widget(MDRaisedButton(text='My Train', pos_hint={'center_x': 0.5}))

        back_btn = MDRaisedButton(text = 'Back', pos_hint = {'center_x': 0.5})
        back_btn.bind(on_release = self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current  = 'main_menu'