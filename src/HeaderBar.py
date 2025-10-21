from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp

from src.ButtonWithIcon import make_square_icon_button, make_square_icon_part_button, make_round_icon_part_button
from src.Styles import COLORS, make_accent_button_style, make_circle_button_style, make_float_button_style

class HeaderBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.height = 36  # Уменьшена высота для более компактного вида
        self.size_hint_y = None  # Добавлено: используем фиксированную высоту
        self.width = 390
        self.spacing = 6  # Уменьшен spacing для более плотного размещения
        self.padding = [6, 0, 6, 0]  # Убраны вертикальные отступы для плотного прилегания
        self.subscriber = None

        self.bind(size=self.change_view)
        self.bind(pos=self.change_view)

        self.build_layout('suggestions')

    def change_view(self, *args):
        self.main_layout.pos = self.pos
        self.main_layout.size = self.size

    def make_splitter(self):
        """Helper method to create a separator"""
        return Label(
            text="|",
            font_size=10,  # Уменьшен размер для тоньше разделителя
            color=(242/255, 242/255, 247/255, 0.3),  # Менее яркий цвет (opacity 0.3 вместо 1.0)
            size_hint_x=0.2  # Компактный размер разделителя
        )
    
    def build_layout(self, mode: str):
        """Build the current keyboard layout"""
        self.clear_widgets()

        if mode == 'suggestions':
            self.main_layout = BoxLayout(orientation='horizontal', spacing=6, padding=[0, 0, 0, 0])

            # Создаем кнопку "AI" с обработчиком
            ai_button = make_square_icon_button(make_accent_button_style(text='AI'))
            ai_button.size_hint = (None, None)  # Фиксированный размер
            ai_button.size = (dp(45), dp(32))  # Небольшой компактный размер
            ai_button.bind(on_release=lambda instance: self.build_layout('feature_mini'))
            self.add_widget(ai_button)
            self.add_widget(self.main_layout)

            self.set_suggestions(['', '', ''])

            if self.subscriber is not None:
                self.subscriber('suggestions')

        elif mode == 'feature_mini':
            
            # Создаем кнопку "<--" с обработчиком возврата к suggestions
            back_button = make_round_icon_part_button(make_circle_button_style(text='<--'))
            back_button.size_hint = (None, None)  # Фиксированный размер
            back_button.size = (36, 36)  # Круглая кнопка 36x36
            back_button.bind(on_release=lambda instance: self.build_layout('suggestions'))
            self.add_widget(back_button)
            
            self.add_widget(self.make_splitter())

            self.add_widget(make_square_icon_part_button(make_float_button_style(text='Tr')))
            self.add_widget(make_square_icon_part_button(make_float_button_style(text='Aa')))
            self.add_widget(make_square_icon_part_button(make_float_button_style(text='O')))
            self.add_widget(make_square_icon_part_button(make_float_button_style(text='T')))

            self.add_widget(self.make_splitter())

            # Создаем кнопку "***" с обработчиком перехода к feature_full
            more_button = make_round_icon_part_button(make_circle_button_style(text='***'))
            more_button.size_hint = (None, None)  # Фиксированный размер
            more_button.size = (36, 36)  # Круглая кнопка 36x36
            more_button.bind(on_release=lambda instance: self.build_layout('feature_full'))
            self.add_widget(more_button)

            if self.subscriber is not None:
                self.subscriber('feature_mini')

        elif mode == 'feature_full':
            self.add_widget(Label(
                text="All features",
                font_size=12,
                color=COLORS['text_normal']
            ))
            
            # Создаем кнопку "X" с обработчиком возврата к suggestions
            close_button = make_round_icon_part_button(make_circle_button_style(text='X'))
            close_button.size_hint_x = 0.6  # Компактный размер
            close_button.bind(on_release=lambda instance: self.build_layout('feature_mini'))
            self.add_widget(close_button)

            if self.subscriber is not None:
                self.subscriber('feature_full')

        else:
            raise ValueError(f"Invalid mode: {mode}")
        
    def set_suggestions(self, suggestions: list[str]):
        self.main_layout.clear_widgets()
        for suggestion in suggestions:
            self.main_layout.add_widget(make_square_icon_part_button(make_float_button_style(text=suggestion)))

    def subscribe_on_mode_change(self, callback: callable):
        self.subscriber = callback