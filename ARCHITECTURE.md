# Архитектура iOS Keyboard Prototype

## 📦 Структура компонентов

```
KeyboardApp (Kivy App)
└── KeyboardContainer (FloatLayout)
    └── BoxLayout (vertical)
        ├── SuggestBar (BoxLayout)
        │   ├── ChipButton ("the")
        │   ├── ChipButton ("and")
        │   └── ChipButton ("for")
        ├── KeyboardRows (BoxLayout)
        │   ├── Row 1: Q W E R T Y U I O P
        │   ├── Row 2: A S D F G H J K L
        │   ├── Row 3: ⇧ Z X C V B N M ⌫
        │   └── Row 4: [123] [🌐] [space] [⏎]
        └── SafeArea (Widget, 34px)
```

## 🎨 Визуальная иерархия

### KeyboardContainer
- **Тип**: FloatLayout
- **Фон**: #1C1C1E (темно-серый)
- **Размер**: 390 x 380 px
- **Функция**: Корневой контейнер, обеспечивает dark-тему

### SuggestBar
- **Тип**: BoxLayout (horizontal)
- **Высота**: 36 px
- **Фон**: #1E1F23 (темная панель)
- **Содержимое**: 3 чипа-подсказки
- **Отступы**: padding=[12,6,12,6], spacing=8
- **AI Hook**: Сюда будут приходить предложения от ChatGPT

### KeyboardRows
- **Тип**: BoxLayout (vertical)
- **Ориентация**: вертикальная
- **Spacing**: 6 px между рядами
- **Padding**: [3,0,3,6]
- **Режимы**: ABC, 123
- **Функция**: Управляет раскладками и переключением

### KeyButton
- **Базовый класс**: ButtonBehavior + Widget
- **Размер**: 44 x 52 px (минимум)
- **Радиус**: 12 px
- **Состояния**:
  - `normal`: #2C2C2E, текст #F2F2F7
  - `pressed`: #3A3A3C, текст #FFFFFF, scale 0.97
  - `disabled`: #1F1F21, текст #8E8E93
- **Анимация**: 70 ms, opacity 0.96

#### Специальные кнопки:
1. **Shift (⇧)**: ширина x1.3
2. **Delete (⌫)**: ширина x1.3
3. **123/ABC**: 58 x 54 px
4. **Lang (🌐)**: 54 x 54 px
5. **Space**: гибкая ширина (min 180 px)
6. **Enter (⏎)**: 76 x 54 px, акцентная рамка #7B61FF

### EmojiPanel
- **Тип**: BoxLayout (horizontal)
- **Высота**: 60 px
- **Содержимое**: 8 демо-эмоджи
- **Статус**: скрыта по умолчанию
- **Функция**: Заглушка для будущей панели эмоджи

### SafeArea
- **Тип**: Widget
- **Высота**: 34 px
- **Фон**: #1C1C1E
- **Функция**: Отступ для iOS safe area (нижняя панель)

## 🔄 Потоки данных

### Переключение раскладок
```
User tap [123] button
    ↓
KeyButton.on_release()
    ↓
KeyboardRows.toggle_layout()
    ↓
current_mode: ABC → 123
    ↓
KeyboardRows.build_layout()
    ↓
UI updates with new layout
```

### Нажатие клавиши
```
User press key
    ↓
KeyButton.on_press()
    ↓
[AI HOOK] Send to ChatGPT
    ↓
Visual feedback:
  - scale → 0.97
  - opacity → 0.96
  - color → pressed
    ↓
User release
    ↓
KeyButton.on_release()
    ↓
[AI HOOK] Update context
    ↓
Restore normal state (90ms animation)
```

## 🎯 AI Integration Points

### 1. SuggestBar
```python
# AI INTEGRATION HOOK: ChatGPT autocomplete suggestions
# Future implementation:
# - API call to GPT with current context
# - Display top 3 predictions
# - Update on each keystroke
```

### 2. KeyButton Press
```python
# AI INTEGRATION HOOK: ChatGPT key press handler
# Future implementation:
# - Collect key sequences
# - Send to context analyzer
# - Trigger autocomplete update
```

### 3. Space Bar
```python
# AI INTEGRATION HOOK: Space bar long-press for voice/AI input
# Future implementation:
# - Detect long press (>500ms)
# - Activate voice recording
# - Send to Whisper API
# - Insert transcribed text
```

### 4. Enter Key
```python
# AI INTEGRATION HOOK: Enter key sends message to AI
# Future implementation:
# - Collect full message
# - Send to ChatGPT conversation
# - Handle response
# - Clear input field
```

### 5. Layout Switch
```python
# AI INTEGRATION HOOK: Layout switch event
# Future implementation:
# - Track layout preferences
# - AI-based layout suggestions
# - Context-aware symbol recommendations
```

## 🎨 Стили и темизация

### Color Palette
```python
COLORS = {
    'bg_keyboard': (28/255, 28/255, 30/255, 1),      # #1C1C1E
    'bg_panel': (30/255, 31/255, 35/255, 1),         # #1E1F23
    'key_normal': (44/255, 44/255, 46/255, 1),       # #2C2C2E
    'key_pressed': (58/255, 58/255, 60/255, 1),      # #3A3A3C
    'key_disabled': (31/255, 31/255, 33/255, 1),     # #1F1F21
    'text_normal': (242/255, 242/255, 247/255, 1),   # #F2F2F7
    'text_pressed': (1, 1, 1, 1),                    # #FFFFFF
    'text_disabled': (142/255, 142/255, 147/255, 1), # #8E8E93
    'accent_purple': (123/255, 97/255, 255/255, 1),  # #7B61FF
    'accent_cyan': (0, 209/255, 255/255, 1),         # #00D1FF
}
```

### Animation Parameters
```python
ANIMATIONS = {
    'press_duration': 0.07,      # 70ms
    'release_duration': 0.09,    # 90ms
    'press_scale': 0.97,         # 97% of original size
    'press_opacity': 0.96,       # 96% opacity
}
```

### Layout Dimensions
```python
DIMENSIONS = {
    'window_width': 390,
    'window_height': 380,
    'keyboard_height': 280,
    'safe_area': 34,
    'suggest_bar': 36,
    'row_spacing': 6,
    'key_spacing': 6,
    'key_width': 44,
    'key_height': 52,
    'key_radius': 12,
    'bottom_row': {
        '123_width': 58,
        'lang_width': 54,
        'space_min': 180,
        'enter_width': 76,
        'height': 54,
    }
}
```

## 🔧 Технические детали

### Kivy Canvas API
Используется для рисования:
- `Color` — установка цвета
- `RoundedRectangle` — скругленные прямоугольники
- `Line` — рамки для акцентных кнопок

### Kivy Animation API
```python
anim = Animation(
    opacity=0.96,
    duration=0.07
)
anim.start(widget)
```

### Kivy Properties
- `StringProperty` — текст на кнопке
- `ListProperty` — цвета (RGBA)
- `BooleanProperty` — флаги состояний
- `NumericProperty` — размеры

### Layout System
- `FloatLayout` — свободное позиционирование
- `BoxLayout` — последовательная компоновка
- `size_hint` — относительные размеры
- `size_hint_y=None` + `height=X` — фиксированная высота

## 📊 Производительность

### Оптимизации:
1. **Canvas caching** — фон обновляется только при изменении размера
2. **Bind optimization** — минимум биндингов на обновление
3. **Animation batching** — одновременные анимации opacity и scale
4. **Widget pooling** — переиспользование виджетов при смене раскладки

### Метрики:
- Время отклика на нажатие: < 16ms (60 FPS)
- Время переключения раскладки: ~100ms
- Memory footprint: ~15-20 MB (Kivy + Python)

## 🚀 Roadmap расширений

### Phase 1: Базовая AI интеграция
- [ ] OpenAI API подключение
- [ ] Контекстные подсказки в SuggestBar
- [ ] История вводов

### Phase 2: Продвинутые функции
- [ ] Голосовой ввод (Whisper API)
- [ ] Умные эмоджи рекомендации
- [ ] Мультиязычность

### Phase 3: Персонализация
- [ ] Обучение на истории пользователя
- [ ] Адаптивная раскладка
- [ ] Темы оформления

### Phase 4: Системная интеграция
- [ ] IME hooks для ввода в систему
- [ ] Clipboard integration
- [ ] Системные уведомления

