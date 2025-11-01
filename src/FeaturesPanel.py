import copy

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from src.ButtonWithIcon import make_round_icon_part_button, make_tablet_icon_part_button
from src.Styles import COLORS, make_dark_key_button_style

class FeaturesPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 6
        self.padding = [3, 0, 3, 6]

        self.features_info = [
            ['Translate', 'Correct', 'Emoji'],
            ['Expand', 'Reply', 'Goal'],
            ['Compress', 'Paraphrase', 'Format'],
            ['Scan', 'Tone', 'Settings']
        ]

        self.back_button = make_round_icon_part_button(make_dark_key_button_style(icon='icons/back.png'))
        self.back_button.bind(on_release=lambda instance: self.state_subscriber('keys + features')) #todo: back state
        
        self.top_layout = BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44)
        self.top_layout.add_widget(Label(text='Features', font_size=16, color=COLORS['text_normal']))
        self.top_layout.add_widget(self.back_button)
        self.add_widget(self.top_layout)

        for row in self.features_info:
            row_layout = BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44)
            for feature in row:
                row_layout.add_widget(self.make_feature_button(feature))
            self.add_widget(row_layout)

        self.back_button.size_hint_x = None

        self.bind(size=self.update_geometry)
        self.update_geometry()

    def update_geometry(self, *args):
        avaliable_height = self.top_layout.height - self.top_layout.padding[1] - self.top_layout.padding[3]
        self.back_button.size = (avaliable_height, avaliable_height)

    def make_feature_button(self, text: str):
        feature_button = make_tablet_icon_part_button(make_dark_key_button_style(icon=f'icons/{text.lower()}.png', text=text))
        feature_button.set_gradient_background(True)
        feature_button.bind(on_release=lambda instance, button_text = copy.deepcopy(text): self.state_subscriber('keys + feature tool', clarification=button_text))
        return feature_button

    def subscribe_on_state(self, callback: callable):
        self.state_subscriber = callback

    def subscribe_on_request(self, callback: callable):
        self.request_subscriber = callback

