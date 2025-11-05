from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp

from src.ButtonWithIcon import make_square_icon_part_button
from src.Styles import make_accent_button_style, make_float_button_style

class SuggestionsPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 6
        self.padding = [6, 0, 6, 0]
        self.size_hint_y = None
        self.height = dp(32)

        self.suggestion_layout = BoxLayout(orientation='horizontal', spacing=6, padding=[0, 0, 0, 0])

        # Создаем кнопку "AI" с обработчиком
        ai_button = make_square_icon_part_button(make_accent_button_style(text='L'))
        ai_button.set_gradient_background(True)
        ai_button.size_hint = (0.1, 1.0)
        ai_button.size = (dp(45), dp(32))
        ai_button.bind(on_release=lambda instance: self.state_subscriber('keys + features'))
        self.add_widget(ai_button)
        self.add_widget(self.suggestion_layout)
        
    def set_suggestions(self, suggestions: list[str]):
        self.suggestion_layout.clear_widgets()

        if len(suggestions) == 0:
            return
        
        for suggestion in suggestions[:-1]:
            self.suggestion_layout.add_widget(self.make_suggestion_button(suggestion))
            self.suggestion_layout.add_widget(self.make_splitter())

        self.suggestion_layout.add_widget(self.make_suggestion_button(suggestions[-1]))

    def make_suggestion_button(self, text: str):
        suggestion_button = make_square_icon_part_button(make_float_button_style(text=text))
        suggestion_button.bind(on_release=lambda instance: self.request_subscriber('suggestion', text))
        return suggestion_button

    def make_splitter(self):
        """Helper method to create a separator"""
        return Label(
            text="|",
            font_size=10,
            color=(242/255, 242/255, 247/255, 0.3),
            size_hint_x=0.2
        )

    def subscribe_on_state(self, callback: callable):
        self.state_subscriber = callback

    def subscribe_on_request(self, callback: callable):
        self.request_subscriber = callback