from kivy.app import App
from kivy.uix.widget import Widget


def activate_inspector():
    from kivy.config import Config
    from kivy.modules import Modules
    from kivy.core.window import Window
    Config.set('modules', 'inspector', '')
    Modules.activate_module('inspector', Window)


def deactivate_inspector():
    from kivy.modules import Modules
    from kivy.core.window import Window
    Modules.deactivate_module('inspector', Window)


class SampleApp(App):
    def on_start(self):
        activate_inspector()
    def on_stop(self):
        deactivate_inspector()
    def build(self):
        return Widget()


if __name__ == '__main__':
    SampleApp().run()