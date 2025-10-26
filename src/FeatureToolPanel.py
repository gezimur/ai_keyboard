from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from src.ButtonWithIcon import make_round_icon_button, make_tablet_icon_button, make_tablet_icon_part_button, TextInputWithBorder
from src.Styles import COLORS, make_accent_button_style, make_dark_key_button_style

#todo maybe base feature tool panel class
class FeatureToolPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = [6, 0, 6, 6]

        self.top_layout = BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44)
        self.back_button = make_round_icon_button(make_dark_key_button_style(text='<--'))
        self.back_button.bind(on_release=lambda instance: self.state_subscriber('keys + features')) #todo: back state
        self.top_layout.add_widget(self.back_button)
        self.top_layout.add_widget(self.make_splitter())
        self.top_layout.add_widget(Label(text='Feature Tool', font_size=16, color=COLORS['text_normal']))
        self.top_layout.add_widget(BoxLayout(orientation='horizontal', size_hint_x=1.0))
        self.add_widget(self.top_layout)

        self.text_input_wrapper = TextInputWithBorder(
            border_color=COLORS['accent_purple'],
            border_width=1,
            border_radius=10,
            multiline=True, 
            font_size=16, 
            foreground_color=COLORS['key_normal_light'], 
            background_color=COLORS['bg_panel'],
            size_hint_y=1.0
        )
        self.text_input = self.text_input_wrapper.text_input
        self.add_widget(self.text_input_wrapper)
        
        self.bottom_layout = BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44)

        self.generate_button = make_round_icon_button(make_dark_key_button_style(text='R'))
        self.generate_button.bind(on_release=self.proc_generate)

        self.undo_button = make_round_icon_button(make_dark_key_button_style(text='Undo'))
        self.undo_button.bind(on_release=self.proc_undo)
        self.redo_button = make_round_icon_button(make_dark_key_button_style(text='Redo'))
        self.redo_button.bind(on_release=self.proc_redo)

        self.space_widget = BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None)

        self.apply_button = make_tablet_icon_button(make_accent_button_style(text='Apply'))
        self.apply_button.bind(on_release=self.proc_generate) #todo: back state
        
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

        self.redo_button.disabled = True
        self.undo_button.disabled = True

        self.bind(size=self.update_geometry)
        self.update_geometry()

        self.undo_cache = []
        self.redo_cache = []

        self.rewrite_last_in_cache = False

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

    def proc_request(self, type: str, text: str):
        self.rewrite_last_in_cache |= self.cache_text()
        
        if type == "key":
            if text == "Del":
                if self.text_input.text:
                    self.text_input.text = self.text_input.text[:-1]
            elif text == "Enter":
                self.text_input.text.insert_text("\n")
            elif text == "Space":
                self.text_input.text.insert_text(" ")
            else:
                self.text_input.insert_text(text)
        elif type == "suggestion":
            self.text_input.insert_text(text)

        self.rewrite_last_in_cache |= self.cache_text()

    def proc_undo(self, *args):
        self.proc_cache_containers(self.undo_cache, self.redo_cache)

    def proc_redo(self, *args):
        self.proc_cache_containers(self.redo_cache, self.undo_cache)

    def proc_cache_containers(self, src: list, dst: list):
        if src:
            cached = src.pop()
            if cached == self.text_input.text and src:
                cached = src.pop()

            dst.append(self.text_input.text)
            self.text_input.text = cached
        
        self.undo_button.disabled = not self.undo_cache
        self.redo_button.disabled = not self.redo_cache

    def proc_generate(self, *args):
        self.rewrite_last_in_cache = False
        self.cache_text()
        self.request_subscriber('generate', self.text_input.text)

    def cache_text(self):
        cache_changed = False
        
        if not self.undo_cache:
            self.undo_cache.append("")

        if self.text_input.text != self.undo_cache[-1]:
            if self.rewrite_last_in_cache:
                self.undo_cache[-1] = self.text_input.text
            else:
                self.undo_cache.append(self.text_input.text)
            self.redo_cache.clear()
            cache_changed = True
        
        self.undo_button.disabled = not self.undo_cache
        self.redo_button.disabled = not self.redo_cache
        return cache_changed

    def subscribe_on_state(self, callback: callable):
        self.state_subscriber = callback

    def subscribe_on_request(self, callback: callable):
        self.request_subscriber = callback