from kivy.uix.screenmanager import ScreenManager
from view.main_menu import MainMenuScreeen

def create_screen_manager():
    sm = ScreenManager()
    sm.add_widget(MainMenuScreeen(name = "main_menu"))
    return sm
