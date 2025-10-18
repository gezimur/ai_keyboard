"""
iOS Keyboard Visual Prototype
Kivy-based UI mockup with dark theme, animations, and layout switching
Python 3.11 + Kivy
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle, Line, Rectangle
from kivy.graphics.texture import Texture
from kivy.graphics.stencil_instructions import StencilPush, StencilUse, StencilUnUse, StencilPop
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty, ListProperty, BooleanProperty
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior

# Import FeaturesPanel from features_panel.py
from features_panel import FeaturesPanel


# ==================== COLOR DEFINITIONS ====================
COLORS = {
    'bg_keyboard': (28/255, 28/255, 30/255, 1),      # #1C1C1E
    'bg_panel': (30/255, 31/255, 35/255, 1),         # #1E1F23

    'key_normal': (44/255, 44/255, 46/255, 1),       # #2C2C2E - для служебных клавиш
    'key_pressed': (58/255, 58/255, 60/255, 1),      # #3A3A3C

    'key_normal_light': (142/255, 142/255, 147/255, 1),     # #8E8E93 - светлые буквенные клавиши\
    'key_pressed_light': (170/255, 170/255, 175/255, 1),  # Светлый pressed для обычных клавиш

    'key_normal_dark': (28/255, 28/255, 30/255, 1),     # #8E8E93 - светлые буквенные клавиши\
    'key_pressed_dark': (44/255, 44/255, 44/255, 1),  # Светлый pressed для обычных клавиш

    'text_normal_light': (142/255, 142/255, 147/255, 1), # Светлый текст для обычных клавиш
    'text_pressed_light': (1, 1, 1, 1), # Светлый текст для pressed обычных клавиш

    'text_normal': (242/255, 242/255, 247/255, 1),   # #F2F2F7
    'text_pressed': (1, 1, 1, 1), # Темный текст для светлых клавиш

    'text_normal_dark': (1, 1, 1, 1),                    # #FFFFFF
    'text_pressed_dark': (10/255, 10/255, 12/255, 1), # Темный текст для pressed светлых клавиш

    'accent_purple': (123/255, 97/255, 255/255, 1),  # #7B61FF
    'accent_cyan': (0, 209/255, 255/255, 1),         # #00D1FF
}

# ==================== GRADIENT HELPER ====================
def create_gradient_texture(color1, color2, width=256, height=1):
    """
    Create a horizontal gradient texture from color1 to color2
    Args:
        color1: (r, g, b, a) - left color (purple)
        color2: (r, g, b, a) - right color (cyan)
        width: texture width in pixels
        height: texture height in pixels
    """
    texture = Texture.create(size=(width, height), colorfmt='rgba')
    pixels = []
    
    for x in range(width):
        # Linear interpolation between colors
        t = x / (width - 1)
        r = int((color1[0] * (1 - t) + color2[0] * t) * 255)
        g = int((color1[1] * (1 - t) + color2[1] * t) * 255)
        b = int((color1[2] * (1 - t) + color2[2] * t) * 255)
        a = int((color1[3] * (1 - t) + color2[3] * t) * 255)
        
        for y in range(height):
            pixels.extend([r, g, b, a])
    
    texture.blit_buffer(bytes(pixels), colorfmt='rgba', bufferfmt='ubyte')
    return texture

class ButtoIcon:
    def __init__(self, icon_normal = None, icon_checked = None):
        self.icon_normal = icon_normal
        self.icon_checked = icon_checked

    def hasIcon(self, is_checked: bool):
        if is_checked and self.icon_checked is not None:
            return True
        elif self.icon_normal is not None:
            return True
        else:
            return False

    def getIcon(self, is_checked: bool):
        if is_checked and self.icon_checked is not None:
            return self.icon_checked
        elif self.icon_normal is not None:
            return self.icon_normal
        else:
            return None

class ButtonColor:
    def __init__(self, color_normal = tuple([0,0,0,0]), color_checked = tuple([0,0,0,0])):
        self.color_normal = color_normal
        self.color_checked = color_checked

    def hasColor(self, is_checked: bool):
        if is_checked:
            return self.color_checked is not None
        else:
            return self.color_normal is not None

    def getColor(self, is_checked: bool):
        if is_checked:
            return self.color_checked
        else:
            return self.color_normal

class StyleMap:
    def __init__(self, icon: ButtoIcon = None, background: ButtonColor = ButtonColor(), border_color: ButtonColor = ButtonColor(), border_radius: int = 0, border_width: int = 0, text: str = None, font_size: int = 0, font_color: ButtonColor = ButtonColor()):
        self.icon               = ButtoIcon()
        self.background         = background
        self.border_color       = border_color
        self.border_radius      = border_radius
        self.border_width       = border_width
        self.text               = text
        self.font_size          = font_size
        self.font_color         = font_color

class ButtonWithIcon(ButtonBehavior, Widget):
    def __init__(self, style: StyleMap, **kwargs):
        super().__init__(**kwargs)
        self.width = 20
        self.height = 20
        self.size_hint=(1,1)
        
        self.style = style
        self.is_checked = False

        self.icon = None
        self.text = None

        self.bind(pos=self.change_view)
        self.bind(size=self.change_view)

        self.init_canvas()
        self.change_view()

    def change_view(self, *args):
        self.main_rect.pos = self.pos
        self.main_rect.size = self.size

        if self.border_line is not None:
            self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, self.style.border_radius)
        
        if self.style.background.hasColor(self.is_checked):
            self.background_color.rgba = self.style.background.getColor(self.is_checked)

        if self.style.border_color is not None and self.style.border_color.hasColor(self.is_checked):
            self.border_color.rgba = self.style.border_color.getColor(self.is_checked)
        
        if self.style.icon.hasIcon(self.is_checked):
            if self.icon is not None:
                self.icon.texture_update(self.style.icon.getIcon(self.is_checked))
                self.icon.pos = (self.x + self.width / 2 - self.icon.width / 2, self.y + self.height / 2 - self.icon.height / 2)
            else:
                self.icon = Image(self.style.icon.getIcon(self.is_checked))
                self.icon.pos = (self.x + self.width / 2 - self.icon.width / 2, self.y + self.height / 2 - self.icon.height / 2)
                self.add_widget(self.icon)
        else:
            if self.icon is not None:
                self.remove_widget(self.icon)
                self.icon = None
        
        if self.style.text is not None:
            if self.text is not None:
                self.text.text = self.style.text
                self.text.color = self.style.font_color.getColor(self.is_checked)
                self.text.pos = (self.x + self.width / 2 - self.text.width / 2, self.y + self.height / 2 - self.text.height / 2)
            else:
                self.text = Label(text=self.style.text, font_size=self.style.font_size, color=self.style.font_color.getColor(self.is_checked))
                self.add_widget(self.text)
                self.text.pos = (self.x + self.width / 2 - self.text.width / 2, self.y + self.height / 2 - self.text.height / 2)
        else:
            if self.text is not None:
                self.remove_widget(self.text)
                self.text = None

    def init_canvas(self):
        with self.canvas:
            self.background_color = Color(*self.style.background.getColor(self.is_checked))
            self.main_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[self.style.border_radius])
            
            self.border_line = None
            if self.style.border_color is not None and self.style.border_color.hasColor(self.is_checked):
                self.border_color = Color(*self.style.border_color.getColor(self.is_checked))
                self.border_line = Line(
                    rounded_rectangle=(self.x, self.y, self.width, self.height, self.style.border_radius),
                    width=self.style.border_width
                )

    def set_text(self, text: str):
        self.style.text = text
        self.change_view()
    
    def set_icon(self, icon: Image):
        self.style.icon = icon
        self.change_view()

    def on_press(self):
        self.is_checked = True
        self.change_view()
    
    def on_release(self):
        self.is_checked = False
        self.change_view()

def make_key_button_style(text: str):
    return StyleMap(
        icon=None,
        background=ButtonColor(color_normal=COLORS['key_normal'], color_checked=COLORS['key_pressed']),
        border_color=None,
        border_radius=4,
        border_width=0,
        text=text,
        font_size=12,
        font_color=ButtonColor(color_normal=COLORS['text_normal'], color_checked=COLORS['text_pressed'])
    )

def make_dark_key_button_style(text: str):
    return StyleMap(
        icon=None,
        background=ButtonColor(color_normal=COLORS['key_normal_dark'], color_checked=COLORS['key_pressed_dark']),
        border_color=None,
        border_radius=4,
        border_width=0,
        text=text,
        font_size=12,
        font_color=ButtonColor(color_normal=COLORS['text_normal_dark'], color_checked=COLORS['text_normal_dark'])
    )

def make_accent_button_style(text: str):
    return StyleMap(
        icon=None,
        background=ButtonColor(color_normal=COLORS['accent_purple'], color_checked=COLORS['accent_cyan']),
        border_color=None,
        border_radius=4,
        border_width=0,
        text=text,
        font_size=12,
        font_color=ButtonColor(color_normal=COLORS['text_normal'], color_checked=COLORS['text_pressed'])
    )

def make_float_button_style(icon = "", text = ""):
    return StyleMap(
        icon=icon,
        background=ButtonColor(color_normal=COLORS['bg_keyboard'], color_checked=COLORS['bg_keyboard']),
        border_color=None,
        border_radius=0,
        border_width=0,
        text=text,
        font_size=12,
        font_color=ButtonColor(color_normal=COLORS['text_normal'], color_checked=COLORS['text_normal'])
    )

def make_circle_button_style(icon: str, text: str):
    return StyleMap(
        icon=icon,
        background=ButtonColor(color_normal=COLORS['key_normal_dark'], color_checked=COLORS['key_normal_dark']),
        border_color=None,
        border_radius=20,
        border_width=0,
        text=text,
        font_size=12,
        font_color=ButtonColor(color_normal=COLORS['text_normal_dark'], color_checked=COLORS['text_normal_dark'])
    )

class HeaderBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.height = 40
        self.width = 390
        self.spacing = 8
        self.padding = [12, 4, 12, 0]  # Нижний padding = 0 для примыкания к клавиатуре
        self.subscriber = None

        self.bind(size=self.change_view)
        self.bind(pos=self.change_view)

        self.build_layout('suggestions')

        # make buttons depends on HeadeBar mode (suggestions, feature_mini, feature_full)

    def change_view(self, *args):
        self.main_layout.pos = self.pos
        self.main_layout.size = self.size

    def build_layout(self, mode: str):
        """Build the current keyboard layout"""
        self.clear_widgets()

        if mode == 'suggestions':
            self.main_layout = BoxLayout(orientation='horizontal', spacing=8, padding=[12, 4, 12, 0])

            self.add_widget(ButtonWithIcon(make_accent_button_style(text='AI')))
            self.add_widget(self.main_layout)

            if self.subscriber is not None:
                self.subscriber('suggestions')

        elif mode == 'feature_mini':
            
            self.add_widget(ButtonWithIcon(make_circle_button_style(text='<--')))
            
            self.add_widget(make_splitter())

            self.add_widget(ButtonWithIcon(make_float_button_style(text='Tr')))
            self.add_widget(ButtonWithIcon(make_float_button_style(text='Aa')))
            self.add_widget(ButtonWithIcon(make_float_button_style(text='O')))
            self.add_widget(ButtonWithIcon(make_float_button_style(text='T')))

            self.add_widget(make_splitter())

            self.add_widget(ButtonWithIcon(make_circle_button_style(text='***')))

            if self.subscriber is not None:
                self.subscriber('feature_mini')

        elif mode == 'feature_full':
            self.add_widget(Label(
                text="All features",
                font_size=12,
                color=COLORS['text_normal']
            ))
            self.add_widget(ButtonWithIcon(make_float_button_style(text='X')))

            if self.subscriber is not None:
                self.subscriber('feature_full')

        else:
            raise ValueError(f"Invalid mode: {mode}")

        def make_splitter(self):
            return Label(
                text="|",
                font_size=12,
                color=COLORS['text_normal']
            )
        
    def set_suggestions(self, suggestions: list[str]):
        self.main_layout.clear_widgets()
        for suggestion in suggestions:
            self.main_layout.add_widget(ButtonWithIcon(make_float_button_style(text=suggestion)))

    def subscribe_on_mode_change(self, callback: callable):
        self.subscriber = callback

class KeyboardPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 6
        self.padding = [3, 0, 3, 6]

        self.central_rows_info = {'ABC': [
                ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
                ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
                ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
            ],
            'abc': [
                ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
                ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
                ['z', 'x', 'c', 'v', 'b', 'n', 'm']
            ],
            '123': [
                ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
                ['-', '/', ':', ';', '(', ')', '$', '&', '@', '"'],
                ['.', ',', '?', '!', "'"]
            ],
            'SYM': [
                ['[', ']', '{', '}', '#', '%', '^', '*', '+', '='],
                ['_', '\\', '|', '~', '<', '>', '€', '£', '¥', '•'],
                ['.', ',', '?', '!', "'"]
            ]}

        self.central_rows = []
        self.central_rows.append(BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44))
        self.central_rows.append(BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44))
        self.central_rows.append(BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44))

        self.rows = []
        self.rows.append(BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44))
        self.rows[0].add_widget(self.central_rows[0])
        
        self.rows.append(BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44))
        self.rows[1].add_widget(self.central_rows[1])

        self.shift_button = ButtonWithIcon(make_dark_key_button_style(text='Shift'))
        self.shift_button.bind(on_release=self.proc_shift)

        self.rows.append(BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44))
        self.rows[2].add_widget(self.shift_button)
        self.rows[2].add_widget(self.central_rows[2])
        self.rows[2].add_widget(ButtonWithIcon(make_dark_key_button_style(text='Del')))

        self.mode_switch_button = ButtonWithIcon(make_key_button_style(text='123'))
        self.mode_switch_button.bind(on_release=self.proc_switch)

        self.rows.append(BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44))
        self.rows[3].add_widget(self.mode_switch_button)
        self.rows[3].add_widget(ButtonWithIcon(make_key_button_style(text='Lang')))
        self.rows[3].add_widget(ButtonWithIcon(make_key_button_style(text='Space')))
        self.rows[3].add_widget(ButtonWithIcon(make_accent_button_style(text='Enter')))

        for row in self.rows:
            self.add_widget(row)

    def proc_shift(self, *args):
        if (self.shift_button.style.text == 'Shift'):
            self.fill_central_row('abc')
            self.shift_button.style.text = 'SHIFT'
        elif (self.shift_button.style.text == 'SHIFT'):
            self.fill_central_row('ABC')
            self.shift_button.style.text = 'Shift'
        elif (self.shift_button.style.text == '1/2'):
            self.fill_central_row('SYM')
            self.shift_button.style.text = '2/2'
        elif (self.shift_button.style.text == '2/2'):
            self.fill_central_row('123')
            self.shift_button.style.text = '1/2'

    def proc_switch(self, *args):
        if (self.mode_switch_button.style.text == '123'):
            self.fill_central_row('123')
            self.shift_button.style.text = '1/2'
            self.mode_switch_button.style.text = 'ABC'
        elif (self.mode_switch_button.style.text == 'ABC'):
            self.fill_central_row('ABC')
            self.shift_button.style.text = 'Shift'
            self.mode_switch_button.style.text = '123'

    def fill_central_row(self,mode: str):
        for row_index, row in enumerate(self.central_rows):
            row.clear_widgets()
            for button in self.central_rows_info[mode][row_index]:
                row.add_widget(ButtonWithIcon(make_key_button_style(text=button)))
        # make buttons depends on KeyboardPanel mode (ABC, abc, 123, #+=)

class FeaturesPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 6
        self.padding = [3, 0, 3, 6]
        
        # make buttons depends on FeaturesPanel mode

# class EmojiPanel(BoxLayout): # maybe widget?
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.orientation = 'horizontal'
#         self.height = 60
#         self.spacing = 12
#         self.padding = [16, 8, 16, 8]
        
        # make buttons depends on EmojiPanel mode

class KeyboardMain(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 6
        self.padding = [3, 0, 3, 6]
        
        self.header_bar = HeaderBar()
        self.active_panel = KeyboardPanel()
        self.header_bar.set_suggestions(['the', 'and', 'for'])

        self.header_bar.subscribe_on_mode_change(self.proc_mode_change)

        self.proc_mode_change('suggestions')
        # self.active_panel.subscribe_on_buttons(self.proc_button)

    def proc_mode_change(self, mode: str):
        self.remove_widget(self.active_panel)

        if mode == 'suggestions':
            self.active_panel = KeyboardPanel()
        elif mode == 'feature_mini':
            self.active_panel = KeyboardPanel()
        elif mode == 'feature_full':
            self.active_panel = FeaturesPanel()

        self.add_widget(self.active_panel)

    # def proc_button(self, type: str, text: str):
        # if type == 'symbol':
        #     print(f"Symbol: {text}")
        # elif type == 'mode_switch':
        #     print(f"Mode switch: {text}")
        #     # switch between panels (KeyboardPanel, FeaturesPanel, EmojiPanel)
        # elif type == 'feature':
        #     print(f"Feature: {text}")
            # process feature button

# split all to different files

# ==================== MAIN APP ====================
class KeyboardApp(App):
    """
    Main Kivy application
    Displays iOS keyboard visual prototype in a 390x320 window
    """
    def build(self):
        # Set window size (390x384: 244 keyboard rows + 40 suggest bar + 34 safe area + margin)
        Window.size = (390, 384)
        Window.clearcolor = COLORS['bg_keyboard']
        
        # AI INTEGRATION HOOK: App initialization
        # Future: initialize ChatGPT API connection, load user preferences
        
        return KeyboardMain()


# ==================== ENTRY POINT ====================
if __name__ == '__main__':
    """
    Launch the keyboard widget
    Run: python keyboard_widget.py
    
    AI INTEGRATION ROADMAP:
    - Connect to ChatGPT API for suggestions
    - Implement context-aware autocomplete
    - Add voice input transcription
    - Smart emoji recommendations
    - Multi-language support with AI translation
    """
    KeyboardApp().run()

