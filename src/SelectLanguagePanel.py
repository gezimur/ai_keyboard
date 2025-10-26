import copy

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label

from src.ButtonWithIcon import make_round_icon_part_button, make_tablet_icon_part_button, make_square_icon_part_button
from src.Styles import COLORS, make_dark_key_button_style, make_accent_button_style, make_float_button_style

class SelectLanguagePanel(BoxLayout):
    def __init__(self, lhs_language="Auto", rhs_language="English", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 6
        self.padding = [6, 0, 6, 6]

        # Список языков
        self.languages = [
            "Auto", "Afrikaans", "Albanian", "Arabic", "Armenian", "Azerbaijani",
            "Basque", "Belarusian", "Bengali", "Bosnian", "Bulgarian", "Catalan",
            "Cebuano", "Chichewa", "Chinese (Simplified)", "Chinese (Traditional)",
            "Corsican", "Croatian", "Czech", "Danish", "Dutch", "English",
            "Esperanto", "Estonian", "Filipino", "Finnish", "French", "Frisian",
            "Galician", "Georgian", "German", "Greek", "Gujarati", "Haitian Creole",
            "Hausa", "Hawaiian", "Hebrew", "Hindi", "Hmong", "Hungarian",
            "Icelandic", "Igbo", "Indonesian", "Irish", "Italian", "Japanese",
            "Javanese", "Kannada", "Kazakh", "Khmer", "Kinyarwanda", "Korean",
            "Kurdish", "Kyrgyz", "Lao", "Latin", "Latvian", "Lithuanian",
            "Luxembourgish", "Macedonian", "Malagasy", "Malay", "Malayalam", "Maltese",
            "Maori", "Marathi", "Mongolian", "Myanmar (Burmese)", "Nepali", "Norwegian",
            "Odia (Oriya)", "Pashto", "Persian", "Polish", "Portuguese", "Punjabi",
            "Romanian", "Russian", "Samoan", "Scots Gaelic", "Serbian", "Sesotho",
            "Shona", "Sindhi", "Sinhala", "Slovak", "Slovenian", "Somali",
            "Spanish", "Sundanese", "Swahili", "Swedish", "Tajik", "Tamil",
            "Tatar", "Telugu", "Thai", "Turkish", "Turkmen", "Ukrainian",
            "Urdu", "Uyghur", "Uzbek", "Vietnamese", "Welsh", "Xhosa",
            "Yiddish", "Yoruba", "Zulu"
        ]

        # Верхняя панель
        self.top_layout = BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44)
        self.back_button = make_round_icon_part_button(make_dark_key_button_style(icon='icons/back.png'))
        self.back_button.bind(on_release=lambda instance: self.state_subscriber('keys + feature tool', clarification="Translate"))
        self.top_layout.add_widget(self.back_button)
        self.top_layout.add_widget(self.make_splitter())
        self.top_layout.add_widget(Label(text='Select Language', font_size=16, color=COLORS['text_normal']))
        self.top_layout.add_widget(BoxLayout(orientation='horizontal', size_hint_x=1.0))
        self.add_widget(self.top_layout)

        # Основное поле с двумя колонками
        self.main_layout = BoxLayout(orientation='horizontal', spacing=6, size_hint_y=1.0)
        
        # Левая колонка (исходный язык)
        self.lhs_column = self.create_language_column("lhs", lhs_language)
        self.main_layout.add_widget(self.lhs_column)
        
        # Правая колонка (целевой язык)
        self.rhs_column = self.create_language_column("rhs", rhs_language)
        self.main_layout.add_widget(self.rhs_column)
        
        self.add_widget(self.main_layout)

        # Нижняя панель с кнопкой Apply
        self.bottom_layout = BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44)
        self.bottom_layout.add_widget(BoxLayout(size_hint_x=0.25))  # Пустое пространство слева
        self.apply_button = make_tablet_icon_part_button(make_accent_button_style(text='Apply'))
        self.apply_button.bind(on_release=self.proc_apply)
        self.apply_button.size_hint_x = 0.5
        self.bottom_layout.add_widget(self.apply_button)
        self.bottom_layout.add_widget(BoxLayout(size_hint_x=0.25))  # Пустое пространство справа
        self.add_widget(self.bottom_layout)

        self.back_button.size_hint_x = None

        self.selected_lhs_language = self.get_centered_language(self.lhs_column)
        self.selected_lhs_language.button_view.text.color = COLORS['accent_purple']

        self.selected_rhs_language = self.get_centered_language(self.rhs_column)
        self.selected_rhs_language.button_view.text.color = COLORS['accent_purple']

        self.bind(size=self.update_geometry)
        self.update_geometry()

    def create_language_column(self, side, current_language):
        languages = self.languages if side == "lhs" else self.languages[1:]
        scroll_y = 1.0 - languages.index(current_language) / float(len(languages))

        scroll_view = ScrollView(size_hint=(1, 1), scroll_y=copy.deepcopy(scroll_y))
        languages_layout = BoxLayout(orientation='vertical', spacing=3, size_hint_y=None)
        
        for language in languages:
            lang_button = make_square_icon_part_button(make_float_button_style(text=language))
            lang_button.button_view.text.font_size = 16
            lang_button.size_hint_y = None
            lang_button.height = 40
            if lang_button.button_view.text.text == current_language:
                lang_button.button_view.text.color = COLORS['accent_purple']
            languages_layout.add_widget(lang_button)
            languages_layout.height += 40 + 3
        
        scroll_view.add_widget(languages_layout)
        scroll_view.bind(scroll_y=self.select_language)
        
        return scroll_view

    def select_language(self, *args):
        self.selected_lhs_language.button_view.text.color = COLORS['text_normal']
        self.selected_lhs_language = self.get_centered_language(self.lhs_column)
        self.selected_lhs_language.button_view.text.color = COLORS['accent_purple']

        self.selected_rhs_language.button_view.text.color = COLORS['text_normal']
        self.selected_rhs_language = self.get_centered_language(self.rhs_column)
        self.selected_rhs_language.button_view.text.color = COLORS['accent_purple']
    
    def get_centered_language(self, scroll_view: ScrollView):
        if not scroll_view.children:
            return None

        languages_layout = scroll_view.children[0]
        
        if not languages_layout.children:
            return None
        
        scroll_y = min(1.0, max(0.0, scroll_view.scroll_y))
        current_button_index = int(scroll_y * (len(languages_layout.children) - 1))
        return languages_layout.children[current_button_index]

    def proc_apply(self, *args):
        """Применить выбранные языки"""
        self.state_subscriber(
            'keys + feature tool', 
            clarification="Translate",
            lhs_language=self.selected_lhs_language.button_view.text.text,
            rhs_language=self.selected_rhs_language.button_view.text.text
        )

    def make_splitter(self):
        """Helper method to create a separator"""
        return Label(
            text="|",
            font_size=10,
            color=(242/255, 242/255, 247/255, 0.3),
            size_hint_x=0.2
        )

    def update_geometry(self, *args):
        avaliable_height = self.top_layout.height - self.top_layout.padding[1] - self.top_layout.padding[3]
        self.back_button.size = (avaliable_height, avaliable_height)

    def subscribe_on_state(self, callback: callable):
        self.state_subscriber = callback

    def subscribe_on_request(self, callback: callable):
        self.request_subscriber = callback