#view/timer_widget.py
from kivy.metrics import dp
from kivy.properties import NumericProperty, BooleanProperty, StringProperty
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu


# Таймер обратного отсчета с интерфейсом
class TimerWidget(BoxLayout):
    time_left = NumericProperty(0) # Оставшееся время в секундах. Автоматически обновляет UI при изменении.
    is_running = BooleanProperty(False) # Флаг состояния таймера
    duration_options = StringProperty('30,60,90,120,180,300') # Варианты длительности через запятую

    def __init__(self, duration = 60, **kwargs):
        super().__init__(orientation = 'vertical', **kwargs)
        self.total_time = duration
        self.time_left = self.total_time

        self._create_ui()         # Создаем интерфейс

        self._init_time_menu()    # Инициализируем меню выбора времени

    def _create_ui(self):
        """Создает элементы интерфейса таймера"""
        # Главный контейнер таймера
        self.orientation = 'horizontal'
        self.spacing = dp(5)
        self.size_hint = (1, None)
        self.height = dp(48)
        self.padding = [dp(5), dp(5)]

        # Кнопка выбора времени
        self.time_select_btn = MDRaisedButton(
            text=f'{self._format_time(self.total_time)}',
            size_hint=(1, None),
            width = dp(70),
            height=dp(80),
            theme_text_color = 'Custom',
            #text_color = (1, 1, 1, 1)
        )
        self.time_select_btn.bind(on_release = self.open_time_menu)
        self.add_widget(self.time_select_btn)

        # Отображение оставшегося времени
        self.label = MDLabel(
            text = self._format_time(self.time_left),
            halign='center',
            font_style='Subtitle2',
            size_hint=(0.5, 1),
            theme_text_color='Custom',
           # text_color=(1, 1, 1, 1)
        )
        self.add_widget(self.label)

        # Панель управления (старт/сброс)
        self.btn_layout = MDBoxLayout(
            orientation = 'horizontal',
            size_hint=(None, 1),
            width=dp(120),
            spacing=5
        )

        self.start_button = MDRaisedButton(
            text = 'Старт',
            size_hint = (1, None),
            theme_text_color = 'Custom',
            width=dp(70),
            height=dp(80),
            #text_color = (1, 1, 1, 1)
        )
        self.start_button.bind(on_release=self.toggle_timer)

        self.reset_button = MDFlatButton(
            text = 'Сброс',
            size_hint=(1, 1),
            # theme_text_color='Custom',
            #text_color=(1, 1, 1, 1)
        )
        self.reset_button.bind(on_release=self.reset_timer)

        self.btn_layout.add_widget(self.start_button)
        self.btn_layout.add_widget(self.reset_button)
        self.add_widget(self.btn_layout)

        # self.add_widget(self.start_button)
        # self.add_widget(self.reset_button)


    def _init_time_menu(self):
        """Инициализирует меню выбора времени"""
        time_options = [int(t) for t in self.duration_options.split(',')]

        menu_items = [{
            'text': self._format_time(t),
            'viewclass': 'OneLineListItem',
            'on_release': lambda x=t: self.set_duration(x)
        } for t in time_options]
        self.time_menu = MDDropdownMenu(
            caller = self.time_select_btn,
            items = menu_items,
            width_mult = 4,
            max_height = 300
        )

    def _format_time(self, seconds = None):
        """Форматирует время в формат MM:SS"""
        if seconds is None:
            seconds = self.time_left
        minutes = int(seconds) // 60
        seconds = int(seconds) % 60
        return f'{minutes:02}:{seconds:02}'

    def set_duration(self, seconds):
        """Устанавливает новую длительность таймера"""
        self.total_time = seconds
        self.reset_timer()
        self.time_select_btn.text = f'Таймер: {self._format_time(self.total_time)}'
        self.time_menu.dismiss()

    def open_time_menu(self, *args):
        """Открывает меню выбора времени"""
        self.time_menu.open()

    def toggle_timer(self, instance):
        """Переключает состояние таймера (старт/стоп)"""
        if not self.is_running:
            self.start_timer()
        else:
            self.stop_timer()

    def start_timer(self, *args):
        """Запускает таймер"""
        if not self.is_running:
            self.is_running = True
            self.start_button.text = 'Стоп'
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def stop_timer(self):
        """Останавливает таймер"""
        if self.is_running:
            self.is_running = False
            self.start_button.text = 'Старт'
            if hasattr(self, 'timer_event'):
                self.timer_event.cancel()

    def reset_timer(self, *args):
        """Сбрасывает таймер в начальное состояние"""
        self.stop_timer()
        self.time_left = self.total_time
        self.label.text = self._format_time(self.time_left)
        self.start_button.text = "Старт"

    def update_timer(self, dt):
        """Обновляет состояние таймера каждую секунду"""
        if self.time_left > 0:
            self.time_left -= 1
            self.label.text = self._format_time(self.time_left)
        else:
            self.stop_timer()
            self.label.text = 'Время вышло!'


