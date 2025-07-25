# ФАЙЛ main.py
from kivy import Config
from kivymd.app import MDApp
from kivy.utils import platform

#----------------------------------------------------------------------------------------------------------------------#
# Установка конфигурации ДО создания приложения
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', '0')
Config.set('kivy', 'keyboard_mode', 'systemanddock')

from kivy.core.window import Window
Window.size = (360, 640)

class TrainApp(MDApp):
    def build(self):
        self.title = 'Тренировки - Мобильная версия'

        # Настройки темы
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.theme_style = 'Light'

        # Размер шрифта
        from kivy.metrics import dp
        Config.set('graphics', 'font_size', str(dp(14)))

        # Мобильные стили (только для Android/iOS)
        if platform in ('android', 'ios'):
            from utils.mobile_styles import setup_mobile_styles
            self.mobile_styles = setup_mobile_styles()

        # Импорт здесь, чтобы Config успел примениться
        from controller.screen_manager import create_screen_manager
        return create_screen_manager()

if __name__ == "__main__":
    TrainApp().run()