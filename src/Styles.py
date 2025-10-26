# ==================== COLOR DEFINITIONS ====================
COLORS = {
    'bg_keyboard': (28/255, 28/255, 30/255, 1),      # #1C1C1E
    'bg_panel': (30/255, 31/255, 35/255, 1),         # #1E1F23

    'key_normal': (58/255, 58/255, 58/255, 1),       # #2C2C2E - для служебных клавиш
    'key_pressed': (72/255, 72/255, 72/255, 1),      # #3A3A3C

    'key_normal_light': (142/255, 142/255, 147/255, 1),     # #8E8E93 - светлые буквенные клавиши\
    'key_pressed_light': (170/255, 170/255, 175/255, 1),  # Светлый pressed для обычных клавиш

    'key_normal_dark': (44/255, 44/255, 44/255, 1),     # #8E8E93 - светлые буквенные клавиши\
    'key_pressed_dark': (58/255, 58/255, 58/255, 1),  # Светлый pressed для обычных клавиш

    'text_normal_light': (142/255, 142/255, 147/255, 1), # Светлый текст для обычных клавиш
    'text_pressed_light': (1, 1, 1, 1), # Светлый текст для pressed обычных клавиш

    'text_normal': (242/255, 242/255, 247/255, 1),   # #F2F2F7
    'text_pressed': (1, 1, 1, 1), # Темный текст для светлых клавиш

    'text_normal_dark': (1, 1, 1, 1),                    # #FFFFFF
    'text_pressed_dark': (10/255, 10/255, 12/255, 1), # Темный текст для pressed светлых клавиш

    'accent_purple': (123/255, 97/255, 255/255, 1),  # #7B61FF
    'accent_cyan': (0, 209/255, 255/255, 1),         # #00D1FF
}

# # ==================== GRADIENT HELPER ====================
# def create_gradient_texture(color1, color2, width=256, height=1):
#     """
#     Create a horizontal gradient texture from color1 to color2
#     Args:
#         color1: (r, g, b, a) - left color (purple)
#         color2: (r, g, b, a) - right color (cyan)
#         width: texture width in pixels
#         height: texture height in pixels
#     """
#     texture = Texture.create(size=(width, height), colorfmt='rgba')
#     pixels = []
    
#     for x in range(width):
#         # Linear interpolation between colors
#         t = x / (width - 1)
#         r = int((color1[0] * (1 - t) + color2[0] * t) * 255)
#         g = int((color1[1] * (1 - t) + color2[1] * t) * 255)
#         b = int((color1[2] * (1 - t) + color2[2] * t) * 255)
#         a = int((color1[3] * (1 - t) + color2[3] * t) * 255)
        
#         for y in range(height):
#             pixels.extend([r, g, b, a])
    
#     texture.blit_buffer(bytes(pixels), colorfmt='rgba', bufferfmt='ubyte')
#     return texture

class ButtonIcon:
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
    def __init__(self, icon: str = "", background: ButtonColor = ButtonColor(), text: str = None, font_size: int = 0, font_color: ButtonColor = ButtonColor()):
        self.icon               = icon # todo ButtonIcon
        self.background         = background
        self.text               = text
        self.font_size          = font_size
        self.font_color         = font_color


def make_key_button_style(icon = "", text = ""):
    return StyleMap(
        icon=icon,
        background=ButtonColor(color_normal=COLORS['key_normal'], color_checked=COLORS['key_pressed']),
        text=text,
        font_size=18,  # Увеличен размер шрифта для лучшей читаемости
        font_color=ButtonColor(color_normal=COLORS['text_normal'], color_checked=COLORS['text_pressed'])
    )

def make_dark_key_button_style(icon = "", text = ""):
    return StyleMap(
        icon=icon,
        background=ButtonColor(color_normal=COLORS['key_normal_dark'], color_checked=COLORS['key_pressed_dark']),
        text=text,
        font_size=16,  # Увеличен размер шрифта
        font_color=ButtonColor(color_normal=COLORS['text_normal_dark'], color_checked=COLORS['text_normal_dark'])
    )

def make_accent_button_style(icon = "", text = ""):
    return StyleMap(
        icon=icon,
        background=ButtonColor(color_normal=COLORS['accent_purple'], color_checked=COLORS['accent_cyan']),
        text=text,
        font_size=16,  # Увеличен размер шрифта
        font_color=ButtonColor(color_normal=COLORS['text_normal'], color_checked=COLORS['text_pressed'])
    )

def make_float_button_style(icon = "", text = ""):
    return StyleMap(
        icon=icon,
        background=ButtonColor(color_normal=COLORS['bg_keyboard'], color_checked=COLORS['bg_keyboard']),
        text=text,
        font_size=12,
        font_color=ButtonColor(color_normal=COLORS['text_normal'], color_checked=COLORS['text_normal'])
    )

def make_circle_button_style(icon = "", text = ""):
    return StyleMap(
        icon=icon,
        background=ButtonColor(color_normal=(18/255, 18/255, 20/255, 1), color_checked=(25/255, 25/255, 27/255, 1)),  # Темнее фона приложения
        text=text,
        font_size=14,
        font_color=ButtonColor(color_normal=COLORS['text_normal_dark'], color_checked=COLORS['text_normal_dark'])
    )

def make_tablet_button_style(icon = "", text = ""):
    return StyleMap(
        icon=icon,
        background=ButtonColor(color_normal=(18/255, 18/255, 20/255, 1), color_checked=(25/255, 25/255, 27/255, 1)),  # Темнее фона приложения
        text=text,
        font_size=14,
        font_color=ButtonColor(color_normal=COLORS['text_normal_dark'], color_checked=COLORS['text_normal_dark'])
    )
