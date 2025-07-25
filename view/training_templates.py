# 📁 view/training_templates.py
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView

from model.templates import load_templates
from model.data import session

class TrainingTemplatesScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = MDBoxLayout(orientation = 'vertical', padding = 20, spacing = 10)# Главный вертикальный контейнер

        # Заголовок
        self.title = MDLabel(text = 'Шаблоны тренировок', halign = 'center', font_style = 'H5')
        self.layout.add_widget(self.title)

        # Область прокрутки
        self.scroll = MDScrollView()
        self.templates_box = MDBoxLayout(orientation = 'vertical', size_hint_y = None)
        self.templates_box.bind(minimum_height=self.templates_box.setter('height'))
        self.scroll.add_widget(self.templates_box)

        self.layout.add_widget(self.scroll)

        # Кнопка назад
        back_btn = MDRaisedButton(text = 'НАЗАД', pos_hint={'center_x': 0.5})
        back_btn.bind(on_release = self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        """Обновление шаблонов перед показом"""
        self.refresh_templates()

    def refresh_templates(self):
        """Обновляет список шаблонов"""
        self.templates_box.clear_widgets()

        templates = load_templates()
        if not templates:
            self.templates_box.add_widget(MDLabel(
                text = 'Нет сохраненных шаблонов',
                halign = 'center',
                theme_text_color = 'Secondary'
            ))
            return

        for template in templates:
            name = template.get('name', 'Без названия')
            created = template.get('created', "Дата неизвестна")
            display = f'{name}, ({created})'

            label = MDLabel(text = display, halign = 'left', theme_text_color = 'Primary')
            btn = MDFlatButton(text = 'Загрузить', pos_hint = {'right': 1})
            btn.bind(on_release = lambda btn, tpl = template: self.load_template(tpl))

            box = MDBoxLayout(orientation = 'vertical')
            box.add_widget(label)
            box.add_widget(btn)

            self.templates_box.add_widget(box)

    def load_template(self, template_data):
        """Загружает шаблон и сразу переходит к редактированию"""
        session.reset()
        session.set_type(template_data.get('type', 'дом'))

        for ex in template_data.get('exercises',[]):
            session.add_exercise(ex['name'], ex['reps'], ex['sets'])

        self.manager.current = 'training_program'
        # Автоматически открываем меню шаблонов
        screen = self.manager.get_screen('training_program')
        screen.refresh_list()
        if hasattr(screen, 'template_menu') and screen.template_menu:
            screen.template_menu.open()

    def go_back(self, instance):
        self.manager.current = 'main_menu'
