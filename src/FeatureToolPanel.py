from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from src.ButtonWithIcon import make_round_icon_button, make_square_icon_part_button, make_tablet_icon_button, make_tablet_icon_part_button
from src.Styles import COLORS, make_accent_button_style, make_dark_key_button_style

class FeatureToolPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 6
        self.padding = [3, 0, 3, 6]

        self.top_layout = BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44)
        self.back_button = make_round_icon_button(make_dark_key_button_style(text='<--'))
        self.back_button.bind(on_release=lambda instance: self.state_subscriber('keys + features')) #todo: back state
        self.top_layout.add_widget(self.back_button)
        self.top_layout.add_widget(self.make_splitter())
        self.top_layout.add_widget(Label(text='Feature Tool', font_size=16, color=COLORS['text_normal']))
        self.add_widget(self.top_layout)

        self.text_input = TextInput(multiline=True, font_size=16, foreground_color=COLORS['text_normal'], size_hint_y=1.0)
        self.add_widget(self.text_input)
        
        self.bottom_layout = BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44)

        self.generate_button = make_round_icon_button(make_dark_key_button_style(text='R'))
        self.generate_button.bind(on_release=lambda instance: self.request_subscriber('generate', self.text_input.text))

        self.undo_button = make_round_icon_button(make_dark_key_button_style(text='Undo'))
        self.redo_button = make_round_icon_button(make_dark_key_button_style(text='Redo'))

        self.space_widget = BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None)

        self.apply_button = make_tablet_icon_button(make_accent_button_style(text='Apply'))
        self.apply_button.bind(on_release=lambda instance: self.state_subscriber('keys + features', self.text_input.text)) #todo: back state
        
        self.bottom_layout.add_widget(self.generate_button)
        self.bottom_layout.add_widget(self.undo_button)
        self.bottom_layout.add_widget(self.redo_button)
        self.bottom_layout.add_widget(self.space_widget)
        self.bottom_layout.add_widget(self.apply_button)

        self.add_widget(self.bottom_layout)

        self.back_button.size_hint_x = None
        self.generate_button.size_hint_x = None
        self.undo_button.size_hint_x = None
        self.redo_button.size_hint_x = None
        self.apply_button.size_hint_x = None

        self.bind(size=self.update_geometry)
        self.update_geometry()

    def update_geometry(self, *args):
        avaliable_height = self.bottom_layout.height - self.bottom_layout.padding[1] - self.bottom_layout.padding[3]

        self.back_button.size = (avaliable_height, avaliable_height)
        self.generate_button.size = (avaliable_height, avaliable_height)
        self.undo_button.size = (avaliable_height, avaliable_height)
        self.redo_button.size = (avaliable_height, avaliable_height)
        self.apply_button.size = (80, avaliable_height)

    def make_splitter(self):
        """Helper method to create a separator"""
        return Label(
            text="|",
            font_size=10,
            color=(242/255, 242/255, 247/255, 0.3),
            size_hint_x=0.2
        )

    def make_feature_button(self, text: str):
        feature_button = make_tablet_icon_part_button(make_dark_key_button_style(icon=f'icons/{text.lower()}.png', text=text))
        feature_button.bind(on_release=lambda instance: self.state_subscriber('keys + feature tool', text))
        return feature_button

    def subscribe_on_state(self, callback: callable):
        self.state_subscriber = callback

    def subscribe_on_request(self, callback: callable):
        self.request_subscriber = callback