from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp

from src.ButtonWithIcon import make_square_icon_part_button, make_round_icon_part_button
from src.Styles import make_dark_key_button_style, make_float_button_style

class FeaturesMiniPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 6
        self.padding = [6, 0, 6, 0]
        self.size_hint_y = None
        self.height = dp(32)

        # Создаем кнопку "<--" с обработчиком возврата к suggestions
        back_button = make_round_icon_part_button(make_dark_key_button_style(text='<--'))
        back_button.bind(on_release=lambda instance: self.state_subscriber('keys + suggestions'))
        self.add_widget(back_button)
        
        self.add_widget(self.make_splitter())

        self.add_widget(self.make_feature_button('Tr'))
        self.add_widget(self.make_feature_button('Aa'))
        self.add_widget(self.make_feature_button('O'))
        self.add_widget(self.make_feature_button('T'))

        self.add_widget(self.make_splitter())

        # Создаем кнопку "***" с обработчиком перехода к feature_full
        more_button = make_round_icon_part_button(make_dark_key_button_style(text='***'))
        more_button.bind(on_release=lambda instance: self.state_subscriber('features'))
        self.add_widget(more_button)
    
    def make_splitter(self):
        """Helper method to create a separator"""
        return Label(
            text="|",
            font_size=10,
            color=(242/255, 242/255, 247/255, 0.3),
            size_hint_x=0.2
        )

    def make_feature_button(self, text: str):
        feature_button = make_square_icon_part_button(make_float_button_style(text=text))
        feature_button.bind(on_release=lambda instance: self.state_subscriber('keys + feature tool', text))
        return feature_button

    def subscribe_on_state(self, callback: callable):
        self.state_subscriber = callback

    def subscribe_on_request(self, callback: callable):
        self.request_subscriber = callback