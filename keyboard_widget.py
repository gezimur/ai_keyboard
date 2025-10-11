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
from kivy.graphics import Color, RoundedRectangle, Line, Rectangle
from kivy.graphics.texture import Texture
from kivy.graphics.stencil_instructions import StencilPush, StencilUse, StencilUnUse, StencilPop
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty, ListProperty, BooleanProperty
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior


# ==================== COLOR DEFINITIONS ====================
COLORS = {
    'bg_keyboard': (28/255, 28/255, 30/255, 1),      # #1C1C1E
    'bg_panel': (30/255, 31/255, 35/255, 1),         # #1E1F23
    'key_normal': (44/255, 44/255, 46/255, 1),       # #2C2C2E - для служебных клавиш
    'key_light': (142/255, 142/255, 147/255, 1),     # #8E8E93 - светлые буквенные клавиши
    'key_pressed': (58/255, 58/255, 60/255, 1),      # #3A3A3C
    'key_pressed_light': (170/255, 170/255, 175/255, 1),  # Светлый pressed для обычных клавиш
    'key_disabled': (31/255, 31/255, 33/255, 1),     # #1F1F21
    'text_normal': (242/255, 242/255, 247/255, 1),   # #F2F2F7
    'text_normal_dark': (28/255, 28/255, 30/255, 1), # Темный текст для светлых клавиш
    'text_pressed': (1, 1, 1, 1),                    # #FFFFFF
    'text_pressed_dark': (10/255, 10/255, 12/255, 1), # Темный текст для pressed светлых клавиш
    'text_disabled': (142/255, 142/255, 147/255, 1), # #8E8E93
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


# ==================== KEY BUTTON COMPONENT ====================
class KeyButton(ButtonBehavior, Widget):
    """
    Custom keyboard key with rounded rectangle, state management, and press animation.
    Supports normal/pressed/disabled states with 0.97 scale animation (70ms).
    """
    text = StringProperty('')
    state_color = ListProperty(COLORS['key_normal'])
    text_color = ListProperty(COLORS['text_normal'])
    is_accent = BooleanProperty(False)
    is_accent_bg = BooleanProperty(False)
    is_disabled = BooleanProperty(False)
    key_type = StringProperty('char')  # char, special, space, enter
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set initial colors based on key type
        # Light keys: char, space
        # Accent keys: enter (purple background)
        # Dark keys: shift, del, lang, 123/ABC, #+= (special)
        if self.key_type == 'enter':
            self.state_color = COLORS['accent_purple']
            self.is_light_key = False
            self.is_accent_bg = True  # Акцентный фон для Enter
        elif self.key_type in ('char', 'space'):
            self.state_color = COLORS['key_light']
            self.is_light_key = True
            self.is_accent_bg = False
        else:
            self.state_color = COLORS['key_normal']
            self.is_light_key = False
            self.is_accent_bg = False
        
        self.text_color = COLORS['text_normal']  # Светло-серый текст для всех

        #subscribe on widget params changes
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.bind(state_color=self.update_canvas)
        self.bind(is_accent=self.update_canvas)
        
        #set drawing instructions for background and save it to change after 
        with self.canvas:
            if self.is_accent_bg:
                # Gradient background with rounded corners using stencil
                # Create stencil mask for rounded corners
                StencilPush()
                self.stencil_rect = RoundedRectangle(
                    pos=self.pos,
                    size=self.size,
                    radius=[5]
                )
                StencilUse()
                
                # Draw gradient inside the stencil
                self.bg_color = Color(1, 1, 1, 1)  # White color for texture
                gradient_texture = create_gradient_texture(
                    COLORS['accent_purple'],
                    COLORS['accent_cyan']
                )
                self.bg_rect = Rectangle(
                    pos=self.pos,
                    size=self.size,
                    texture=gradient_texture
                )
                
                StencilUnUse()
                # Redraw the stencil shape (optional, for better edge quality)
                RoundedRectangle(
                    pos=self.pos,
                    size=self.size,
                    radius=[5]
                )
                StencilPop()
            else:
                # Solid color background
                self.bg_color = Color(*self.state_color)
                self.bg_rect = RoundedRectangle(
                    pos=self.pos,
                    size=self.size,
                    radius=[5]
                )
            
            # Accent border for Enter/active keys
            self.border_color = Color(0, 0, 0, 0)
            self.border_line = Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, 5),
                width=1.5
            )
        
        # Add text label
        self.label = Label(
            text=self.text,
            font_size='18sp',
            color=self.text_color,
            bold=False,
            halign='center',
            valign='middle'
        )
        self.add_widget(self.label)
    
    def update_canvas(self, *args):
        # Don't update color for gradient buttons
        if not self.is_accent_bg:
            self.bg_color.rgba = self.state_color
        
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        
        # Update stencil rect for gradient buttons
        if self.is_accent_bg and hasattr(self, 'stencil_rect'):
            self.stencil_rect.pos = self.pos
            self.stencil_rect.size = self.size
        
        # Update border for accent keys (disable for Enter with accent background)
        if self.is_accent and not self.is_accent_bg:
            self.border_color.rgba = COLORS['accent_purple']
        else:
            self.border_color.rgba = (0, 0, 0, 0)
        
        self.border_line.rounded_rectangle = (
            self.x, self.y, self.width, self.height, 5
        )
        
        self.label.pos = self.pos
        self.label.size = self.size
        self.label.text_size = self.size
    
    def on_press(self):
        """Handle press with visual feedback and animation"""

        if self.is_disabled:
            return
        
        # Update colors based on key type
        if self.is_accent_bg:
            # Enter button with gradient: just reduce opacity slightly
            # Don't change state_color to preserve gradient
            pass
        elif self.is_light_key:
            self.state_color = COLORS['key_pressed_light']
            self.text_color = COLORS['text_normal']  # Остается светло-серым
        else:
            self.state_color = COLORS['key_pressed']
            self.text_color = COLORS['text_normal']  # Остается светло-серым
        
        # # Scale animation
        # anim = Animation(
        #     opacity=0.96,
        #     duration=0.07
        # )
        # anim.start(self)
        
        # # Simulate scale with size change
        # self.original_size = (self.width, self.height)
        # scale_anim = Animation(
        #     width=self.width * 0.97,
        #     height=self.height * 0.97,
        #     duration=0.07
        # )
        # scale_anim.start(self)
    
    def on_release(self):
        """Restore normal state after release"""
        if self.is_disabled:
            return
        
        # Restore colors based on key type
        if self.is_accent_bg:
            # Enter button with gradient: gradient is preserved automatically
            # No need to restore state_color
            pass
        elif self.is_light_key:
            self.state_color = COLORS['key_light']
            self.text_color = COLORS['text_normal']  # Светло-серый
        else:
            self.state_color = COLORS['key_normal']
            self.text_color = COLORS['text_normal']  # Светло-серый
        
        # # Restore opacity and size
        # anim = Animation(
        #     opacity=1.0,
        #     duration=0.09
        # )
        # anim.start(self)
        
        # if hasattr(self, 'original_size'):
        #     scale_anim = Animation(
        #         width=self.original_size[0],
        #         height=self.original_size[1],
        #         duration=0.09
        #     )
        #     scale_anim.start(self)
        
        # AI INTEGRATION HOOK: Post-release processing
        # Future: update context, trigger autocomplete

#Нах нада? Удалить
# ==================== CHIP BUTTON ====================
class ChipButton(Label):
    """
    Clickable chip button for suggestions
    Combines ButtonBehavior with Label for interactive text chips
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.halign = 'center'
        self.valign = 'middle'
        self.bind(size=self.update_text_size)
    
    def update_text_size(self):
        """Update text_size to match widget size for proper text alignment"""
        self.text_size = self.size


# ==================== SUGGEST BAR ====================
class SuggestBar(BoxLayout):
    """
    Suggestion bar (40px height - slightly taller than letters)
    Contains: AI button (purple, left) + 3 suggestion chips (no background, equal width)
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 40
        self.spacing = 8
        self.padding = [12, 4, 12, 0]  # Нижний padding = 0 для примыкания к клавиатуре
        
        with self.canvas:
            Color(*COLORS['bg_keyboard'])  # Тот же цвет что у клавиатуры для бесшовности
            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[0]
            )
        
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        # AI button (left side, purple like Enter)
        # AI INTEGRATION HOOK: Trigger ChatGPT suggestions
        ai_button = self.create_ai_button()
        self.add_widget(ai_button)
        
        # Demo suggestion chips (no background, equal width)
        # AI INTEGRATION HOOK: ChatGPT autocomplete suggestions
        # Future: populate from AI model predictions
        suggestions = ['the', 'and', 'for']
        for i, suggestion in enumerate(suggestions):
            chip = self.create_chip(suggestion)
            self.add_widget(chip)
            
            # Add vertical separator between chips (but not after the last one)
            if i < len(suggestions) - 1:
                separator = self.create_separator()
                self.add_widget(separator)
    
    def create_ai_button(self):
        """Create AI button with gradient purple-to-cyan background like Enter"""
        ai_btn = KeyButton(
            is_accent=True,
            key_type="enter",
            text = 'AI'
        )
        
        return ai_btn
    
    def create_chip(self, text):
        """Create a suggestion chip without background, equal width"""
        chip = ChipButton(
            text=text,
            size_hint_x=1,  # Равная ширина для всех
            color=COLORS['text_normal'],
            font_size='16sp'
        )
        
        # Нет фона - только текст
        
        return chip
    
    def create_separator(self):
        """Create vertical separator between suggestion chips"""
        separator = Label(
            text='|',
            size_hint_x=None,
            width=10,
            color=(COLORS['text_normal'][0], COLORS['text_normal'][1], COLORS['text_normal'][2], 0.3),  # Полупрозрачный
            font_size='16sp'
        )
        return separator
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


# ==================== EMOJI PANEL ====================
class EmojiPanel(BoxLayout):
    """
    Emoji panel placeholder (single row of demo emojis)
    Hidden by default, shown when emoji mode activated
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 60
        self.spacing = 12
        self.padding = [16, 8, 16, 8]
        
        with self.canvas.before:
            Color(*COLORS['bg_panel'])
            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[0]
            )
        
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        # Demo emojis
        emojis = ['😀', '😂', '❤️', '👍', '🎉', '🔥', '✨', '🌟']
        for emoji in emojis:
            emoji_btn = Label(
                text=emoji,
                size_hint=(None, 1),
                width=40,
                font_size='24sp'
            )
            self.add_widget(emoji_btn)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


# ==================== KEYBOARD ROWS ====================
class KeyboardRows(BoxLayout):
    """
    Main keyboard layout with 3 letter rows + bottom utility row
    Supports ABC (QWERTY), 123 (numbers/symbols), and Emoji modes
    """
    current_mode = StringProperty('ABC')  # ABC, abc, 123, SYM, Emoji
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 6
        self.padding = [3, 0, 3, 6]
        self.is_shifted = False  # Track shift state (False = lowercase, True = uppercase)
        
        # Layout definitions
        self.layouts = {
            'ABC': [
                ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
                ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
                ['shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'del']
            ],
            'abc': [
                ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
                ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
                ['shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'del']
            ],
            '123': [
                ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
                ['-', '/', ':', ';', '(', ')', '$', '&', '@', '"'],
                ['#+=', '.', ',', '?', '!', "'", 'del']
            ],
            'SYM': [
                ['[', ']', '{', '}', '#', '%', '^', '*', '+', '='],
                ['_', '\\', '|', '~', '<', '>', '€', '£', '¥', '•'],
                ['123', '.', ',', '?', '!', "'", 'del']
            ]
        }
        
        self.build_layout()
    
    def build_layout(self):
        """Build the current keyboard layout"""
        self.clear_widgets()
        
        mode = self.current_mode
        
        # Determine which layout to use based on mode and shift state
        if mode == 'ABC':
            layout_key = 'ABC' if self.is_shifted else 'abc'
        else:
            layout_key = mode
        
        if layout_key in self.layouts:
            rows = self.layouts[layout_key]
            for row_index, row_chars in enumerate(rows):
                row = self.create_row(row_chars, row_index)
                self.add_widget(row)
        
        # Add bottom utility row
        bottom_row = self.create_bottom_row()
        self.add_widget(bottom_row)
    
    def create_row(self, chars, row_index=0):
        """Create a single keyboard row"""
        row = BoxLayout(
            orientation='horizontal',
            spacing=6,
            size_hint_y=None,
            height=44
        )
        
        # Add left padding for second row (index 1) - half key width
        if row_index == 1:
            left_spacer = Widget(size_hint_x=0.5)
            row.add_widget(left_spacer)
        
        for char in chars:
            if char == 'shift':
                # Shift key (wider)
                key = KeyButton(
                    text='shift',
                    size_hint_x=1.3,
                    key_type='special',
                    is_accent=self.is_shifted  # Highlight when active
                )
                key.bind(on_release=self.toggle_shift)
            elif char == 'del':
                # Delete key (wider)
                key = KeyButton(
                    text='Del',
                    size_hint_x=1.3,
                    key_type='special'
                )
            elif char == '#+=':
                # Symbol switch key (123 -> SYM)
                key = KeyButton(
                    text='#+=',
                    size_hint_x=1.3,
                    key_type='special'
                )
                key.bind(on_release=self.switch_to_symbols)
            elif char == '123':
                # Number switch key (SYM -> 123)
                key = KeyButton(
                    text='123',
                    size_hint_x=1.3,
                    key_type='special'
                )
                key.bind(on_release=self.switch_to_numbers)
            else:
                # Regular character key
                key = KeyButton(
                    text=char,
                    size_hint_x=1,
                    key_type='char'
                )
            
            row.add_widget(key)
        
        # Add right padding for second row (index 1) - half key width
        if row_index == 1:
            right_spacer = Widget(size_hint_x=0.5)
            row.add_widget(right_spacer)
        
        return row
    
    def create_bottom_row(self):
        """
        Create bottom utility row with 123, Lang, Space, Enter
        Sizes: 123=58x54, Lang=54x54, Space=min180x54(flex), Enter=76x54
        """
        row = BoxLayout(
            orientation='horizontal',
            spacing=6,
            size_hint_y=None,
            height=44
        )
        
        # 123 / ABC switch button (58px width)
        if self.current_mode == 'ABC':
            switch_text = '123'
        else:  # 123 or SYM mode
            switch_text = 'ABC'
        
        switch_btn = KeyButton(
            text=switch_text,
            size_hint_x=None,
            width=58,
            key_type='special'
        )
        switch_btn.bind(on_release=self.toggle_layout)
        row.add_widget(switch_btn)
        
        # Language/Emoji button (54px width)
        lang_btn = KeyButton(
            text='🌐',
            size_hint_x=None,
            width=54,
            key_type='special'
        )
        lang_btn.bind(on_release=self.toggle_emoji)
        row.add_widget(lang_btn)
        
        # Space bar (flexible, min 180px)
        # AI INTEGRATION HOOK: Space bar long-press for voice/AI input
        space_btn = KeyButton(
            text='space',
            size_hint_x=3,
            key_type='space'
        )
        row.add_widget(space_btn)
        
        # Enter button (76px width, accent style)
        enter_btn = KeyButton(
            text='⏎',
            size_hint_x=None,
            width=76,
            key_type='enter',
            is_accent=True
        )
        # AI INTEGRATION HOOK: Enter key sends message to AI
        row.add_widget(enter_btn)
        
        return row
    
    def toggle_layout(self, instance):
        """Switch between ABC and 123/SYM layouts"""
        # AI INTEGRATION HOOK: Layout switch event
        if self.current_mode == 'ABC':
            self.current_mode = '123'
            self.is_shifted = False  # Reset shift when leaving ABC mode
        elif self.current_mode in ('123', 'SYM'):
            self.current_mode = 'ABC'
            self.is_shifted = False  # Start with lowercase
        self.build_layout()
    
    def switch_to_symbols(self, instance):
        """Switch from 123 to SYM layout"""
        # AI INTEGRATION HOOK: Symbol layout activation
        self.current_mode = 'SYM'
        self.build_layout()
    
    def switch_to_numbers(self, instance):
        """Switch from SYM to 123 layout"""
        # AI INTEGRATION HOOK: Number layout activation
        self.current_mode = '123'
        self.build_layout()
    
    def toggle_shift(self, instance):
        """Toggle shift state for uppercase/lowercase letters"""
        # AI INTEGRATION HOOK: Shift state change
        if self.current_mode == 'ABC':
            self.is_shifted = not self.is_shifted
            self.build_layout()
    
    def toggle_emoji(self, instance):
        """Toggle emoji panel (placeholder)"""
        # AI INTEGRATION HOOK: Emoji/language selector
        # Future: integrate emoji picker with AI sentiment
        pass


# ==================== KEYBOARD CONTAINER ====================
class KeyboardContainer(FloatLayout):
    """
    Root keyboard container with dark background (#1C1C1E)
    Includes safe-area bottom padding (34px)
    Total size: 390x(280+34)=314px
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)
        
        with self.canvas.before:
            Color(*COLORS['bg_keyboard'])
            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[0]
            )
        
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        # Main layout container
        main_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=284,  # Keyboard (244) + suggest bar (40) + safe area (34)
            pos_hint={'center_x': 0.5, 'top': 0.8},
            spacing=0  # No spacing between suggest bar and keyboard
        )
        
        # Suggest bar
        # AI INTEGRATION HOOK: Real-time ChatGPT suggestions
        suggest_bar = SuggestBar()
        main_layout.add_widget(suggest_bar)
        
        # Keyboard rows
        keyboard_rows = KeyboardRows()
        main_layout.add_widget(keyboard_rows)
        
        # Emoji panel (hidden by default)
        # emoji_panel = EmojiPanel()
        # main_layout.add_widget(emoji_panel)
        
        # Safe area bottom padding (34px)
        safe_area = Widget(size_hint_y=None, height=34)
        with safe_area.canvas.before:
            Color(*COLORS['bg_keyboard'])
            safe_bg = RoundedRectangle(pos=safe_area.pos, size=safe_area.size)
            safe_area.bind(pos=lambda i, v: setattr(safe_bg, 'pos', v))
            safe_area.bind(size=lambda i, v: setattr(safe_bg, 'size', v))
        main_layout.add_widget(safe_area)
        
        self.add_widget(main_layout)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


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
        
        return KeyboardContainer()


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

