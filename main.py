# ФАЙЛ main.py

from kivymd.app import MDApp
from controller.screen_manager import create_screen_manager
#----------------------------------------------------------------------------------------------------------------------#
#Класс для запуска приложения
class TrainApp(MDApp):
    def build(self):
        self.title = 'Тренировки'
        self.theme_cls.primary_palette = 'BlueGray'
        return create_screen_manager()

if __name__ == "__main__":
    TrainApp().run()
