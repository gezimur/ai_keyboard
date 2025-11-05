from kivy.uix.boxlayout import BoxLayout

from src.KeyboardPanel import KeyboardPanel
from src.SuggestionsPanel import SuggestionsPanel
from src.FeaturesMiniPanel import FeaturesMiniPanel
from src.FeaturesPanel import FeaturesPanel
from src.FeatureToolPanel import FeatureToolPanel
from src.SelectLanguagePanel import SelectLanguagePanel
from src.AIProcessor import AIProcessor

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
        self.select_language_panel = None

        self.ai_processor = AIProcessor()
        self.ai_processor.subscribe_on_answer(self.proc_request)
        self.ai_processor.start()
        
        # keyboard state: "keys + suggestions", "keys + features", "features", "keys + feature tool", "feature tool"
        self.set_state("keys + suggestions")

    def prepare_to_close(self, *args):
        self.ai_processor.prepare_to_close()

    def set_state(self, state: str, **args):
        self.clear_widgets()

        if state == "keys + suggestions":
            self.keyboard_panel = self.make_keyboard_panel()
            self.suggestions_panel = self.make_suggestions_panel()
            self.features_mini_panel = None
            self.features_panel = None
            self.feature_tool_panel = None
            self.select_language_panel = None
        elif state == "keys + features":
            self.keyboard_panel = self.make_keyboard_panel()
            self.suggestions_panel = None
            self.features_mini_panel = self.make_features_mini_panel()
            self.features_panel = None
            self.feature_tool_panel = None
            self.select_language_panel = None
        elif state == "features":
            self.keyboard_panel = None
            self.suggestions_panel = None
            self.features_mini_panel = None
            self.features_panel = self.make_features_panel()
            self.feature_tool_panel = None
            self.select_language_panel = None
        elif state == "keys + feature tool":
            self.keyboard_panel = self.make_keyboard_panel()
            self.suggestions_panel = None
            self.features_mini_panel = None
            self.features_panel = None
            self.feature_tool_panel = self.make_feature_tool_panel(**args)
            self.select_language_panel = None
        elif state == "feature tool":
            self.keyboard_panel = None
            self.suggestions_panel = None
            self.features_mini_panel = None
            self.features_panel = None
            self.feature_tool_panel = self.make_feature_tool_panel(**args)
            self.select_language_panel = None
        elif state == "select translate language":
            self.keyboard_panel = None
            self.suggestions_panel = None
            self.features_mini_panel = None
            self.features_panel = None
            self.feature_tool_panel = None
            self.select_language_panel = self.make_select_language_panel(**args)
        else:
            raise ValueError(f"Invalid state: {state}")

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

        if self.select_language_panel is not None:
            self.add_widget(self.select_language_panel)

    def make_keyboard_panel(self):
        if self.keyboard_panel is not None:
            return self.keyboard_panel
        
        self.keyboard_panel = self.make_smth_panel(KeyboardPanel)
        return self.keyboard_panel

    def make_suggestions_panel(self):
        if self.suggestions_panel is not None:
            return self.suggestions_panel
        
        self.suggestions_panel = self.make_smth_panel(SuggestionsPanel)
        self.suggestions_panel.set_suggestions(['Hello', 'World', 'Python'])
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

    def make_feature_tool_panel(self, clarification: str = "", **args):
        if self.feature_tool_panel is not None:
            return self.feature_tool_panel
        
        if clarification == "":
            return None

        self.feature_tool_panel = self.make_smth_panel(FeatureToolPanel, clarification=clarification, **args)
        return self.feature_tool_panel

    def make_select_language_panel(self, **args):
        if self.select_language_panel is not None:
            return self.select_language_panel
        
        self.select_language_panel = self.make_smth_panel(SelectLanguagePanel, **args)
        return self.select_language_panel

    def make_smth_panel(self, panel_type: type, **args):
        panel = panel_type(**args)
        panel.subscribe_on_state(self.set_state)
        panel.subscribe_on_request(self.proc_request)
        return panel

    def proc_request(self, type: str, text: str):
        print(f"request: type={type}, text={text}")
        if self.feature_tool_panel is None:
            return

        if type == 'key' or type == 'suggestion' or type == 'error' or type == 'result':
            self.feature_tool_panel.proc_request(type, text)

        elif type == 'generate':
            self.ai_processor.proc_request(type, text)
            self.feature_tool_panel.proc_request('wait', '')
