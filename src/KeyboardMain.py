from kivy.uix.boxlayout import BoxLayout
from src.HeaderBar import HeaderBar
from src.KeyboardPanel import KeyboardPanel
from src.FeaturesPanel import FeaturesPanel

class KeyboardMain(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 0  # Убран spacing для плотного прилегания HeaderBar к KeyboardPanel
        self.padding = [0, 0, 0, 0]  # Убраны отступы для плотного прилегания
        
        self.header_bar = HeaderBar()
        self.active_panel = KeyboardPanel()
        self.header_bar.set_suggestions(['the', 'and', 'for'])

        self.header_bar.subscribe_on_mode_change(self.proc_mode_change)

        # Добавлено: добавляем header_bar в layout
        self.add_widget(self.header_bar)

        self.proc_mode_change('suggestions')
        # self.active_panel.subscribe_on_buttons(self.proc_button)

    def proc_mode_change(self, mode: str):
        # Добавлено: проверяем, что виджет существует в layout перед удалением
        if self.active_panel in self.children:
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