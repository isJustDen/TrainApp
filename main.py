from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

class MainMenuScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation = 'vertical', spacing = 20, padding = 20)
        layout.add_widget(MDLabel(text = 'Welcome to train!', halign = 'center', font_style = 'H5'))

        layout.add_widget(MDRaisedButton(text = 'Start training', pos_hint = {'center_x':0.5}))
        layout.add_widget(MDRaisedButton(text = 'History', pos_hint = {'center_x':0.5}))
        layout.add_widget(MDRaisedButton(text = 'Settings', pos_hint={'center_x':0.5}))

        self.add_widget(layout)

class TrainApp(MDApp):
    def build(self):
        return MainMenuScreen()

if __name__ == "__main__":
    TrainApp().run()