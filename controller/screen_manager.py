# ФАЙЛ screen_manager.py
from kivymd.uix.screenmanager import MDScreenManager
from kivy.metrics import dp
from kivy.utils import platform
from view.main_menu import MainMenuScreen
from view.training_history import TrainingHistoryScreen
from view.training_program import TrainingProgramScreen
from view.training_stats import TrainingStatsScreen
from view.training_templates import TrainingTemplatesScreen
from view.training_type import TrainingTypeScreen


def create_screen_manager():
    sm = MDScreenManager()

    # Настройки для мобильных устройств
    if platform in ('android', 'ios'):
        if platform  == 'android':
            try:
                from android.permissions import request_permissions, Permission
                request_permissions([Permission.READ_EXTERNAL_STORAGE,
                                     Permission.WRITE_EXTERNAL_STORAGE])
            except:
                pass

        # Мобильные стили
        from kivymd.app import MDApp
        MDApp.get_running_app().theme_cls.primary_palette = 'Blue'
        MDApp.get_running_app().theme_cls.theme_style = 'Light'

    sm.add_widget(MainMenuScreen(name = "main_menu"))
    sm.add_widget(TrainingTypeScreen(name = 'training_type'))
    sm.add_widget(TrainingProgramScreen(name = 'training_program'))
    sm.add_widget(TrainingHistoryScreen(name = 'training_history'))
    sm.add_widget(TrainingStatsScreen(name = 'training_stats'))
    sm.add_widget(TrainingTemplatesScreen(name = 'training_templates'))
    return sm


