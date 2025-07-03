# ФАЙЛ screen_manager.py
from kivymd.uix.screenmanager import MDScreenManager

from view.main_menu import MainMenuScreen
from view.training_program import TrainingProgramScreen
from view.training_type import TrainingTypeScreen


def create_screen_manager():
    sm = MDScreenManager()
    sm.add_widget(MainMenuScreen(name = "main_menu"))
    sm.add_widget(TrainingTypeScreen(name = 'training_type'))
    sm.add_widget(TrainingProgramScreen(name = 'training_program'))
    return sm
