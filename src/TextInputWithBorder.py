from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Line
from src.Styles import COLORS, make_circle_button_style
from src.ButtonWithIcon import make_round_icon_part_button

class TextInputWithBorder(BoxLayout):
    """
    Wrapper class for TextInput with rounded purple border and clear button
    """
    def __init__(self, border_color=None, border_width=2, border_radius=10, **kwargs):
        super().__init__()
        
        self.padding = (5, 5)
        
        # Extract TextInput specific kwargs
        text_input_kwargs = {}
        for key in ['multiline', 'font_size', 'foreground_color', 'background_color', 'hint_text', 'text']:
            if key in kwargs:
                text_input_kwargs[key] = kwargs.pop(key)
        
        # Set border properties
        self.border_color = border_color if border_color else COLORS['accent_purple']
        self.border_width = border_width
        self.border_radius = border_radius
        
        # Create TextInput with padding to avoid overlap with clear button
        self.text_input = TextInput(
            **text_input_kwargs
        )
        self.text_input.size_hint = (1, 1)
        
        # Create clear button
        clear_button_style = make_circle_button_style(icon="icons/close.png")
        self.clear_button = make_round_icon_part_button(clear_button_style)
        self.clear_button.size_hint = (None, None)
        self.clear_button.size = (30, 30)
        self.clear_button.pos_hint = {'right': 0.98, 'y': 0.05}
        self.clear_button.bind(on_release=self.clear_text)
        
        # Bind events for canvas updates
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        
        # Initialize canvas
        self.init_canvas()
        
        # Add widgets to layout
        self.add_widget(self.text_input)
        self.add_widget(self.clear_button)
    
    def init_canvas(self):
        """Initialize the canvas with border"""
        with self.canvas.before:
            self.border_color_obj = Color(*self.border_color)
            self.border_line = Line(
                rounded_rectangle=(
                    self.x, self.y,
                    self.width, self.height,
                    self.border_radius
                ),
                width=self.border_width
            )
    
    def update_canvas(self, *args):
        """Update canvas when position or size changes"""
        self.border_line.rounded_rectangle = (
            self.x, self.y,
            self.width, self.height,
            self.border_radius
        )
    
    def clear_text(self, *args):
        """Clear the text input"""
        self.text_input.text = ""