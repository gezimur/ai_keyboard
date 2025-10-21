from kivy.uix.boxlayout import BoxLayout

from src.ButtonWithIcon import make_square_icon_button, make_square_icon_part_button
from src.Styles import make_key_button_style, make_float_button_style, make_dark_key_button_style

class KeyboardPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 6
        self.padding = [6, 2, 6, 6]  # Минимальный верхний отступ для плотного прилегания к HeaderBar

        self.central_rows_info = {'ABC': [
                ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
                ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
                ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
            ],
            'abc': [
                ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
                ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
                ['z', 'x', 'c', 'v', 'b', 'n', 'm']
            ],
            '123': [
                ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
                ['-', '/', ':', ';', '(', ')', '$', '&', '@', '"'],
                ['.', ',', '?', '!', "'"]
            ],
            'SYM': [
                ['[', ']', '{', '}', '#', '%', '^', '*', '+', '='],
                ['_', '\\', '|', '~', '<', '>', '€', '£', '¥', '•'],
                ['.', ',', '?', '!', "'"]
            ]}

        self.central_rows = []
        self.central_rows.append(BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44))
        self.central_rows.append(BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44, padding=[15, 0, 15, 0]))  # Отступы для визуального смещения
        self.central_rows.append(BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44))

        self.rows = []
        self.rows.append(BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44))
        self.rows[0].add_widget(self.central_rows[0])
        
        self.rows.append(BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44))
        self.rows[1].add_widget(self.central_rows[1])

        self.shift_button = make_square_icon_part_button(make_dark_key_button_style(text='Shift'))
        self.shift_button.size_hint_x = None  # Уменьшенный размер для Shift
        self.shift_button.size = (57, 52)
        self.shift_button.bind(on_release=self.proc_shift)

        self.delete_button = make_square_icon_part_button(make_dark_key_button_style(icon='icons/del.png'))
        self.delete_button.size_hint_x = None  # Уменьшенный размер для Del
        self.delete_button.size = (57, 52)

        self.rows.append(BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44))
        self.rows[2].add_widget(self.shift_button)
        self.rows[2].add_widget(self.central_rows[2])
        self.rows[2].add_widget(self.delete_button)

        self.mode_switch_button = make_square_icon_part_button(make_key_button_style(text='123'))
        self.mode_switch_button.size_hint_x = 1.0  # Компактный размер
        self.mode_switch_button.bind(on_release=self.proc_switch)

        self.lang_button = make_square_icon_part_button(make_key_button_style(text='Lang'))
        self.lang_button.size_hint_x = 1.0  # Компактный размер

        self.space_button = make_square_icon_part_button(make_key_button_style(text='Space'))
        self.space_button.size_hint_x = 5.0  # Широкая кнопка Space

        self.enter_button = make_square_icon_button(make_dark_key_button_style(icon='icons/enter.png', text='Enter'))
        self.enter_button.size_hint_x = 1.1  # Средний размер

        self.rows.append(BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44))
        self.rows[3].add_widget(self.mode_switch_button)
        self.rows[3].add_widget(self.lang_button)
        self.rows[3].add_widget(self.space_button)
        self.rows[3].add_widget(self.enter_button)

        # Добавлено: инициализируем клавиши при создании панели
        self.fill_central_row('ABC')

        for row in self.rows:
            self.add_widget(row)

    def proc_shift(self, *args):
        if (self.shift_button.style.text == 'Shift'):
            self.fill_central_row('abc')
            self.shift_button.set_text('SHIFT')
        elif (self.shift_button.style.text == 'SHIFT'):
            self.fill_central_row('ABC')
            self.shift_button.set_text('Shift')
        elif (self.shift_button.style.text == '1/2'):
            self.fill_central_row('SYM')
            self.shift_button.set_text('2/2')
        elif (self.shift_button.style.text == '2/2'):
            self.fill_central_row('123')
            self.shift_button.set_text('1/2')

    def proc_switch(self, *args):
        if (self.mode_switch_button.style.text == '123'):
            self.shift_button.set_text('1/2')
            self.mode_switch_button.set_text('ABC')
            self.fill_central_row('123')
        elif (self.mode_switch_button.style.text == 'ABC'):
            self.shift_button.set_text('Shift')
            self.mode_switch_button.set_text('123')
            self.fill_central_row('ABC')

    def fill_central_row(self,mode: str):
        for row_index, row in enumerate(self.central_rows):
            row.clear_widgets()
            for button in self.central_rows_info[mode][row_index]:
                button = make_square_icon_part_button(make_key_button_style(text=button))
                button.size_hint_x = 1.0
                row.add_widget(button)
        # make buttons depends on KeyboardPanel mode (ABC, abc, 123, #+=)