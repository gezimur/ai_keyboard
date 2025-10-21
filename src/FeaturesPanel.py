from kivy.uix.boxlayout import BoxLayout
# from src.ButtonWithIcon import ButtonWithIcon
from src.Styles import make_tablet_button_style

class FeaturesPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 6
        self.padding = [3, 0, 3, 6]

        # self.translate_button = ButtonWithIcon(style=make_tablet_button_style(icon="icons/translate.svg", text="Translate"))

