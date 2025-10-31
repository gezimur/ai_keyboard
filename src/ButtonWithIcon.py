from kivy.uix.button import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle, Line

from src.Styles import StyleMap, COLORS

class ButtonViewStrategy:
    def __init__(self):
        self.icon = None
        self.text = None

    def set_icon(self, icon: str):
        pass
    def set_text(self, text: str):
        pass
    def set_font_size(self, font_size: int):
        pass

class IconBackgroundButton(Widget, ButtonViewStrategy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)

    def update_canvas(self, *args):
        if self.icon is not None:
            self.icon.size = self.size
            self.icon.pos = self.pos

        if self.text is not None:
            self.text.pos = self.pos
            self.text.size = self.size

    def set_icon(self, icon: str):
        if not icon:
            return

        if self.icon is None:
            self.icon = Image(source=icon, allow_stretch=True, keep_ratio=True, size_hint=(None, None))
            self.add_widget(self.icon)
        else:
            self.icon.source = icon

        self.update_canvas()
        
    def set_text(self, text: str):
        if not text:
            return

        if self.text is None:
            self.text = Label(text=text, size_hint=(None, None))
            self.add_widget(self.text)
        else:
            self.text.text = text
        
        self.update_canvas()

    def set_font_size(self, font_size: int):
        if self.text is not None:
            self.text.font_size = font_size

class IconPartButton(BoxLayout, ButtonViewStrategy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'

    def set_icon(self, icon: str):
        if not icon:
            return
        
        if self.icon is None:
            self.icon = Image(source=icon, allow_stretch=True, keep_ratio=True, size_hint=(0.5, 0.5))
            self.icon.pos_hint = {'center_x': 0.9, 'center_y': 0.5}
            self.add_widget(self.icon)
        else:
            self.icon.source = icon

    def set_text(self, text: str):
        if not text:
            return
        
        if self.text is None:
            self.text = Label(text=text, size_hint=(1, 1))
            self.add_widget(self.text)
        else:
            self.text.text = text

    def set_font_size(self, font_size: int):
        if self.text is not None:
            self.text.font_size = font_size

class BaseButton(ButtonBehavior, Widget):
    def __init__(self, style: StyleMap, button_view: ButtonViewStrategy, **kwargs):
        super().__init__(**kwargs)
        self.style = style # background for presed / background for normal, text color, text size
        self.button_view = button_view

        # self.width = 20
        # self.height = 20
        # self.size_hint=(1,1)

        self.is_checked = False

        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.bind(disabled=self.update_canvas)

        self.add_widget(self.button_view)

        if self.button_view.text is not None:
            self.button_view.set_font_size(self.style.font_size)
            self.button_view.text.color = self.style.font_color.getColor(self.is_checked)

    def update_canvas(self, *args):
        if self.style.background.hasColor(self.is_checked):
            self.background_color.rgba = self.style.background.getColor(self.is_checked)

        icon_opacity = 1.0
        if self.disabled:
            icon_opacity = 0.5
        
        if self.button_view.icon is not None:
            self.button_view.icon.opacity = icon_opacity

        self.button_view.pos = self.pos
        self.button_view.size = self.size

    def set_text(self, text: str):
        self.style.text = text
        self.button_view.set_text(text)
    
    def set_icon(self, icon: str):
        self.style.icon = icon
        self.button_view.set_icon(icon)

    def on_press(self):
        self.is_checked = True
        self.update_canvas()
    
    def on_release(self):
        self.is_checked = False
        self.update_canvas()

    #def subsctibe_on_click(): -> callbck on (type: str, text: str)

class SquareButton(BaseButton):
    def __init__(self, style: StyleMap, button_view: ButtonViewStrategy, **kwargs):
        super().__init__(style, button_view, **kwargs)

        self.init_canvas()

    def update_canvas(self, *args):
        self.main_rect.pos = self.pos
        self.main_rect.size = self.size
        self.main_rect.radius = [self.height / 10]

        super().update_canvas() # update background color

    def init_canvas(self):
        
        with self.canvas.before:
            self.background_color = Color(*self.style.background.getColor(self.is_checked))
            self.main_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[self.height / 10])

class RoundButton(BaseButton):
    def __init__(self, style: StyleMap, button_view: ButtonViewStrategy, **kwargs):
        super().__init__(style, button_view, **kwargs)
        self.size_hint = (1.0, 1.0)

        self.init_canvas()

    def update_canvas(self, *args):
        main_rect_size = min(self.width, self.height)

        self.main_rect.pos = self.pos
        self.main_rect.size = (main_rect_size, main_rect_size)
        self.main_rect.radius = [main_rect_size / 2]

        super().update_canvas() # update background color

    def init_canvas(self):
        main_rect_size = min(self.width, self.height)
        
        with self.canvas.before:
            self.background_color = Color(*self.style.background.getColor(self.is_checked))
            self.main_rect = RoundedRectangle(
                pos=self.pos,
                size=(main_rect_size, main_rect_size),
                radius=[main_rect_size / 2])

class TabletButton(BaseButton):
    def __init__(self, style: StyleMap, button_view: ButtonViewStrategy, **kwargs):
        super().__init__(style, button_view, **kwargs)

        self.init_canvas()

    def update_canvas(self, *args):
        self.main_rect.pos = self.pos
        self.main_rect.size = self.size
        self.main_rect.radius = [self.height / 2]

        super().update_canvas() # update background color

    def init_canvas(self):
        with self.canvas.before:
            self.background_color = Color(*self.style.background.getColor(self.is_checked))
            self.main_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[self.height / 2])

def make_square_icon_button(style: StyleMap):
    button_view = IconBackgroundButton()
    button_view.set_icon(style.icon)
    button_view.set_text(style.text)
    return SquareButton(style, button_view)

def make_square_icon_part_button(style: StyleMap):
    button_view = IconPartButton()
    button_view.set_icon(style.icon)
    button_view.set_text(style.text)
    return SquareButton(style, button_view)

def make_round_icon_button(style: StyleMap):
    button_view = IconBackgroundButton()
    button_view.set_icon(style.icon)
    button_view.set_text(style.text)
    return RoundButton(style, button_view)

def make_round_icon_part_button(style: StyleMap):
    button_view = IconPartButton()
    button_view.set_icon(style.icon)
    button_view.set_text(style.text)
    return RoundButton(style, button_view)

def make_tablet_icon_button(style: StyleMap):
    button_view = IconBackgroundButton()
    button_view.set_icon(style.icon)
    button_view.set_text(style.text)
    return TabletButton(style, button_view)

def make_tablet_icon_part_button(style: StyleMap):
    button_view = IconPartButton()
    button_view.set_icon(style.icon)
    button_view.set_text(style.text)
    return TabletButton(style, button_view)
