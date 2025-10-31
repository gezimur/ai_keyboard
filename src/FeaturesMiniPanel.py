import copy

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

        self.back_button = make_round_icon_part_button(make_dark_key_button_style(icon='icons/back.png'))
        self.back_button.bind(on_release=lambda instance: self.state_subscriber('keys + suggestions'))
        self.add_widget(self.back_button)
        
        self.add_widget(self.make_splitter())

        self.add_widget(self.make_feature_button('Translate'))
        self.add_widget(self.make_feature_button('Correct'))
        self.add_widget(self.make_feature_button('Emoji'))
        self.add_widget(self.make_feature_button('Expand'))

        self.add_widget(self.make_splitter())

        # Создаем кнопку "***" с обработчиком перехода к feature_full
        self.more_button = make_round_icon_part_button(make_dark_key_button_style(icon='icons/more.png'))
        self.more_button.bind(on_release=lambda instance: self.state_subscriber('features'))
        self.add_widget(self.more_button)
    
        self.back_button.size_hint_x = None
        self.more_button.size_hint_x = None

        self.bind(size=self.update_geometry)
        self.update_geometry()

    def update_geometry(self, *args):
        avaliable_height = self.height - self.padding[1] - self.padding[3]

        self.back_button.size = (avaliable_height, avaliable_height)
        self.more_button.size = (avaliable_height, avaliable_height)

    def make_splitter(self):
        """Helper method to create a separator"""
        return Label(
            text="|",
            font_size=10,
            color=(242/255, 242/255, 247/255, 0.3),
            size_hint_x=0.2
        )

    def make_feature_button(self, text: str):
        feature_button = make_square_icon_part_button(make_float_button_style(icon=f'icons/{text.lower()}.png'))
        feature_button.bind(on_release=lambda instance, button_text = copy.deepcopy(text): self.state_subscriber('keys + feature tool', clarification=button_text))
        return feature_button

    def subscribe_on_state(self, callback: callable):
        self.state_subscriber = callback

    def subscribe_on_request(self, callback: callable):
        self.request_subscriber = callback