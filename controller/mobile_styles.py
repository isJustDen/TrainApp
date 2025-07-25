#controller/mobile_styles.py
from kivy.metrics import dp
from kivymd.app import MDApp


def setup_mobile_styles():
    app = MDApp.get_running_app()

    MOBILE_SIZES = {
        'button_height': dp(48),
        'input_height': dp(60),
        'section_spacing': dp(15),
        'timer_height': dp(100)
    }
    # Мобильные размеры
    app.theme_cls.material_style = 'M3'
    app.theme_cls.primary_palette = 'Blue'
    app.theme_cls.theme_style = 'Light'

    # Размеры для мобильных устройств
    return{
        'button_height': dp(48),
        'text_size': dp(16),
        'title_size': dp(20),
        'padding': dp(15),
        'spacing': dp(10)
    }