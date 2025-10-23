from kivy.uix.boxlayout import BoxLayout

from src.KeyboardPanel import KeyboardPanel
from src.SuggestionsPanel import SuggestionsPanel
from src.FeaturesMiniPanel import FeaturesMiniPanel
from src.FeaturesPanel import FeaturesPanel
from src.FeatureToolPanel import FeatureToolPanel

# keyboard state: "keys + suggestions", "keys + features", "features", "keys + feature tool", "feature tool"
# set_state(state: str):
# 1. clear childer - self.clear_children()
# 2. add new widgets - self.add_widget(self.make_smth_widget())
# 
# make_smth_widget():
# 1. make new widget
# 2. subscribe on next state
# 3. subscribe on request (type: str, text: str): type: "text (key, suggestion)", "feature", "instruction" (maybe)

#feature tool widget:
# 1. cache inside to redo, undo
# 2. send current text on switches (close, reopen, smth else) and accept request


class KeyboardMain(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 6  # Убран spacing для плотного прилегания HeaderBar к KeyboardPanel
        self.padding = [0, 0, 0, 0]  # Убраны отступы для плотного прилегания
        
        self.keyboard_panel = None
        self.suggestions_panel = None
        self.features_mini_panel = None
        self.features_panel = None
        self.feature_tool_panel = None
        
        # keyboard state: "keys + suggestions", "keys + features", "features", "keys + feature tool", "feature tool"
        self.set_state("keys + suggestions")

    def set_state(self, state: str, clarification: str = ""):
        self.clear_widgets()

        if state == "keys + suggestions":
            self.keyboard_panel = self.make_keyboard_panel()
            self.suggestions_panel = self.make_suggestions_panel()
            self.features_mini_panel = None
            self.features_panel = None
            self.feature_tool_panel = None
        elif state == "keys + features":
            self.keyboard_panel = self.make_keyboard_panel()
            self.suggestions_panel = None
            self.features_mini_panel = self.make_features_mini_panel()
            self.features_panel = None
            self.feature_tool_panel = None
        elif state == "features":
            self.keyboard_panel = None
            self.suggestions_panel = None
            self.features_mini_panel = None
            self.features_panel = self.make_features_panel()
            self.feature_tool_panel = None
        elif state == "keys + feature tool":
            self.keyboard_panel = self.make_keyboard_panel()
            self.suggestions_panel = None
            self.features_mini_panel = None
            self.features_panel = None
            self.feature_tool_panel = self.make_feature_tool_panel(clarification)
        elif state == "feature tool":
            self.keyboard_panel = None
            self.suggestions_panel = None
            self.features_mini_panel = None
            self.features_panel = None
            self.feature_tool_panel = self.make_feature_tool_panel()

        if self.suggestions_panel is not None:
            self.add_widget(self.suggestions_panel)

        if self.features_mini_panel is not None:
            self.add_widget(self.features_mini_panel)

        if self.features_panel is not None:
            self.add_widget(self.features_panel)

        if self.feature_tool_panel is not None:
            self.add_widget(self.feature_tool_panel)

        if self.keyboard_panel is not None:
            self.add_widget(self.keyboard_panel)

    def make_keyboard_panel(self):
        if self.keyboard_panel is not None:
            return self.keyboard_panel
        
        self.keyboard_panel = self.make_smth_panel(KeyboardPanel)
        return self.keyboard_panel

    def make_suggestions_panel(self):
        if self.suggestions_panel is not None:
            return self.suggestions_panel
        
        self.suggestions_panel = self.make_smth_panel(SuggestionsPanel)
        return self.suggestions_panel

    def make_features_mini_panel(self):
        if self.features_mini_panel is not None:
            return self.features_mini_panel
        
        self.features_mini_panel = self.make_smth_panel(FeaturesMiniPanel)
        return self.features_mini_panel

    def make_features_panel(self):
        if self.features_panel is not None:
            return self.features_panel
        
        self.features_panel = self.make_smth_panel(FeaturesPanel)
        return self.features_panel

    def make_feature_tool_panel(self, clarification: str = ""):
        if self.feature_tool_panel is not None:
            return self.feature_tool_panel
        
        if clarification == "":
            return None

        self.feature_tool_panel = self.make_smth_panel(FeatureToolPanel)
        return self.feature_tool_panel

    def make_smth_panel(self, panel_type: type):
        panel = panel_type()
        panel.subscribe_on_state(self.set_state)
        panel.subscribe_on_request(self.proc_request)
        return panel

    def proc_request(self, type: str, text: str):
        print(f"request: type={type}, text={text}")
        #todo: add processor