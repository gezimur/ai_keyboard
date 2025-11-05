"""
iOS Keyboard Visual Prototype
Kivy-based UI mockup with dark theme, animations, and layout switching
Python 3.11 + Kivy
"""

from kivy.app import App
from kivy.core.window import Window

from src.KeyboardMain import KeyboardMain
from src.Styles import COLORS

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

        MainWidget = KeyboardMain()

        Window.bind(on_request_close=MainWidget.prepare_to_close)
        
        # AI INTEGRATION HOOK: App initialization
        # Future: initialize ChatGPT API connection, load user preferences
        
        return MainWidget


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

