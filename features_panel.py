"""
All Features Panel - UI экран для виджета клавиатуры
Тёмная тема с неоновой фиолетово-синей подсветкой
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Ellipse, Line
from kivy.animation import Animation
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from kivy.core.window import Window

# ============================================================================
# КОНСТАНТЫ ЦВЕТОВ И РАЗМЕРОВ
# ============================================================================

# Цвета фона
COLOR_BG_DARK = (0.067, 0.067, 0.067, 1)  # #111111
COLOR_BG_CARD = (0.102, 0.102, 0.102, 1)  # #1A1A1A
COLOR_BG_CHIP = (0.13, 0.13, 0.15, 1)     # #212123

# Неоновые цвета
COLOR_NEON_PRIMARY = (0.6, 0.4, 1.0, 1)    # Фиолетовый
COLOR_NEON_SECONDARY = (0.4, 0.6, 1.0, 1)  # Синий
COLOR_NEON_GLOW = (0.5, 0.5, 1.0, 0.3)     # Свечение

# Цвета текста
COLOR_TEXT_PRIMARY = (1, 1, 1, 1)
COLOR_TEXT_SECONDARY = (0.8, 0.8, 0.85, 1)

# Размеры
CHIP_HEIGHT = 52
CHIP_RADIUS = 26
ICON_SIZE = 24
ICON_CIRCLE_SIZE = 32
GRID_SPACING = 12
PADDING_HORIZONTAL = 20
PADDING_TOP = 60
PADDING_BOTTOM = 40

# Анимация
ANIM_DURATION = 0.25
PRESS_SCALE = 0.98


# ============================================================================
# КОМПОНЕНТ КАПСУЛЬ-КНОПКИ
# ============================================================================

class FeatureChip(BoxLayout):
    """Капсуль-кнопка с иконкой и текстом"""
    
    icon_name = StringProperty('')
    label_text = StringProperty('')
    active = BooleanProperty(False)
    press_opacity = NumericProperty(1.0)
    
    # Эмодзи-иконки для каждой функции
    ICON_EMOJI_MAP = {
        'translate': '🌐',
        'correct': '✓',
        'emojify': '😊',
        'expand': '↔',
        'reply': '💬',
        'dialog_goal': '🎯',
        'compress': '⇄',
        'paraphrase': '♻',
        'format': '📝',
        'scan': '🔍',
        'tone': '🎵',
        'settings': '⚙',
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 12
        self.padding = [16, 0, 16, 0]
        self.size_hint = (1, None)
        self.height = CHIP_HEIGHT
        
        # Инициализация графики
        with self.canvas.before:
            # Фон капсули
            self.bg_color = Color(*COLOR_BG_CHIP)
            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[CHIP_RADIUS]
            )
            
            # Свечение (изначально прозрачное)
            self.glow_color = Color(0.5, 0.5, 1.0, 0)
            self.glow_rect = RoundedRectangle(
                pos=(self.x - 2, self.y - 2),
                size=(self.width + 4, self.height + 4),
                radius=[CHIP_RADIUS + 2]
            )
        
        # Иконка (круглая плашка с эмодзи)
        icon_layout = FloatLayout(size_hint=(None, 1), width=ICON_CIRCLE_SIZE)
        
        # Рисуем градиентный круг для иконки
        with icon_layout.canvas.before:
            self.icon_color = Color(*COLOR_NEON_PRIMARY)
            self.icon_circle = Ellipse(
                pos=(self.x + 16, self.y + (CHIP_HEIGHT - ICON_CIRCLE_SIZE) / 2),
                size=(ICON_CIRCLE_SIZE, ICON_CIRCLE_SIZE)
            )
        
        # Эмодзи или символ поверх круга
        emoji = self.ICON_EMOJI_MAP.get(self.icon_name, '•')
        self.icon_label = Label(
            text=emoji,
            font_size='16sp',
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        icon_layout.add_widget(self.icon_label)
        
        self.add_widget(icon_layout)
        
        # Текст кнопки
        self.text_label = Label(
            text=self.label_text,
            font_size='16sp',
            color=COLOR_TEXT_PRIMARY,
            size_hint=(1, 1)
        )
        self.add_widget(self.text_label)
        
        # Привязка событий
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.bind(active=self.on_active_change)
        self.bind(press_opacity=self.on_opacity_change)
        
    def update_graphics(self, *args):
        """Обновление графических элементов при изменении размера/позиции"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.glow_rect.pos = (self.x - 2, self.y - 2)
        self.glow_rect.size = (self.width + 4, self.height + 4)
        
        # Обновляем позицию круга иконки
        if hasattr(self, 'icon_circle'):
            self.icon_circle.pos = (
                self.x + 16,
                self.y + (CHIP_HEIGHT - ICON_CIRCLE_SIZE) / 2
            )
    
    def on_active_change(self, instance, value):
        """Анимация свечения при активации"""
        if value:
            # Включаем свечение
            anim = Animation(a=0.4, duration=ANIM_DURATION)
            anim.start(self.glow_color)
        else:
            # Выключаем свечение
            anim = Animation(a=0, duration=ANIM_DURATION)
            anim.start(self.glow_color)
    
    def on_opacity_change(self, instance, value):
        """Изменение прозрачности при нажатии"""
        self.bg_color.a = value
        self.icon_color.a = value
        self.text_label.opacity = value
        self.icon_label.opacity = value
    
    def on_touch_down(self, touch):
        """Обработка нажатия"""
        if self.collide_point(*touch.pos):
            self.active = True
            # Анимация нажатия
            anim_down = Animation(
                press_opacity=0.7,
                duration=ANIM_DURATION / 2
            )
            anim_down.start(self)
            return True
        return super().on_touch_down(touch)
    
    def on_touch_up(self, touch):
        """Обработка отпускания"""
        if self.active:
            # Анимация возврата
            anim_up = Animation(
                press_opacity=1.0,
                duration=ANIM_DURATION
            )
            anim_up.start(self)
            
            # Выключаем свечение через небольшую задержку
            def deactivate(*args):
                self.active = False
            
            anim_up.bind(on_complete=deactivate)
            return True
        return super().on_touch_up(touch)


# ============================================================================
# КНОПКА ЗАКРЫТИЯ
# ============================================================================

class CloseButton(Widget):
    """Кнопка X для закрытия"""
    
    press_opacity = NumericProperty(1.0)
    
    def __init__(self, on_close=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (40, 40)
        self.on_close_callback = on_close  # Store close callback
        
        with self.canvas:
            # Фон круглой кнопки
            self.bg_color = Color(*COLOR_BG_CHIP)
            self.bg_circle = Ellipse(pos=self.pos, size=self.size)
            
            # Крестик
            self.x_color = Color(*COLOR_TEXT_SECONDARY)
            # Линия 1: \
            self.line1 = Line(
                points=[
                    self.x + 12, self.y + 12,
                    self.x + 28, self.y + 28
                ],
                width=2
            )
            # Линия 2: /
            self.line2 = Line(
                points=[
                    self.x + 28, self.y + 12,
                    self.x + 12, self.y + 28
                ],
                width=2
            )
        
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.bind(press_opacity=self.on_opacity_change)
    
    def update_graphics(self, *args):
        """Обновление графики"""
        self.bg_circle.pos = self.pos
        self.bg_circle.size = self.size
        self.line1.points = [
            self.x + 12, self.y + 12,
            self.x + 28, self.y + 28
        ]
        self.line2.points = [
            self.x + 28, self.y + 12,
            self.x + 12, self.y + 28
        ]
    
    def on_opacity_change(self, instance, value):
        """Изменение прозрачности"""
        self.bg_color.a = value
        self.x_color.a = value
    
    def on_touch_down(self, touch):
        """Нажатие"""
        if self.collide_point(*touch.pos):
            self.touch_down_pos = touch.pos
            anim = Animation(press_opacity=0.5, duration=ANIM_DURATION / 2)
            anim.start(self)
            return True
        return super().on_touch_down(touch)
    
    def on_touch_up(self, touch):
        """Отпускание"""
        if hasattr(self, 'touch_down_pos') and self.collide_point(*touch.pos):
            # Вызываем колбэк закрытия
            if self.on_close_callback:
                self.on_close_callback()
            
            anim = Animation(press_opacity=1.0, duration=ANIM_DURATION)
            anim.start(self)
            return True
        
        anim = Animation(press_opacity=1.0, duration=ANIM_DURATION)
        anim.start(self)
        return super().on_touch_up(touch)


# ============================================================================
# ГЛАВНАЯ ПАНЕЛЬ
# ============================================================================

class FeaturesPanel(FloatLayout):
    """Экран All Features"""
    
    # Список всех функций
    FEATURES = [
        ('translate', 'Translate'),
        ('correct', 'Correct'),
        ('emojify', 'Emojify'),
        ('expand', 'Expand'),
        ('reply', 'Reply'),
        ('dialog_goal', 'Dialog Goal'),
        ('compress', 'Compress'),
        ('paraphrase', 'Paraphrase'),
        ('format', 'Format'),
        ('scan', 'Scan'),
        ('tone', 'Tone'),
        ('settings', 'Settings'),
    ]
    
    def __init__(self, on_close=None, **kwargs):
        super().__init__(**kwargs)
        
        # Store close callback
        self.on_close_callback = on_close
        
        # Фон
        with self.canvas.before:
            Color(*COLOR_BG_DARK)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        # Основной контейнер
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[PADDING_HORIZONTAL, PADDING_TOP, PADDING_HORIZONTAL, PADDING_BOTTOM],
            spacing=24
        )
        
        # Шапка с заголовком и кнопкой закрытия
        header = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=40,
            spacing=16
        )
        
        # Заголовок
        title = Label(
            text='All Features',
            font_size='28sp',
            bold=True,
            color=COLOR_TEXT_PRIMARY,
            size_hint=(1, 1)
        )
        header.add_widget(title)
        
        # Кнопка закрытия (передаём колбэк)
        close_btn = CloseButton(on_close=self.on_close_callback)
        header.add_widget(close_btn)
        
        main_layout.add_widget(header)
        
        # Сетка кнопок (3 колонки)
        grid = GridLayout(
            cols=3,
            spacing=GRID_SPACING,
            size_hint=(1, 1),
            row_default_height=CHIP_HEIGHT,
            row_force_default=True
        )
        
        # Добавляем все кнопки
        for icon_name, label in self.FEATURES:
            chip = FeatureChip(
                icon_name=icon_name,
                label_text=label
            )
            grid.add_widget(chip)
        
        main_layout.add_widget(grid)
        
        self.add_widget(main_layout)
    
    def update_bg(self, *args):
        """Обновление фона"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


# ============================================================================
# ДЕМО-ПРИЛОЖЕНИЕ
# ============================================================================

class FeaturesApp(App):
    """Демо-приложение для экрана All Features"""
    
    def build(self):
        # Устанавливаем размер окна под iPhone
        Window.size = (390, 844)
        Window.clearcolor = COLOR_BG_DARK
        
        return FeaturesPanel()


if __name__ == '__main__':
    FeaturesApp().run()

