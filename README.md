# iOS Keyboard Visual Prototype

Визуальный прототип iOS-клавиатуры на Python 3.11 + Kivy

## 📋 Требования

- Python 3.11
- Kivy 2.2.0+

## 🚀 Установка Kivy

```bash
pip install kivy
```

Для Windows можно также установить через:

```bash
python -m pip install kivy[base] kivy_examples
```

## ▶️ Запуск

```bash
python keyboard_widget.py
```

Откроется окно 390x380 px с темной клавиатурой iOS.

## ✨ Реализованные компоненты

### KeyboardContainer
- Корневой контейнер с dark-фоном (#1C1C1E)
- Safe-area bottom = 34 px

### SuggestBar
- Панель подсказок высотой 36 px
- 3 демо-чипа автодополнения

### KeyboardRows
- 3 ряда букв QWERTY
- Нижний служебный ряд
- Переключение ABC ↔ 123

### KeyButton
- Кастомная кнопка с RoundedRectangle
- Состояния: normal/pressed/disabled
- Анимация scale 0.97 (70 ms)
- Радиус скругления 12 px

### Нижний ряд (SwitchBar)
- **123/ABC** — переключатель режимов (58x54 px)
- **🌐** — язык/эмоджи (54x54 px)
- **space** — пробел, гибкая ширина (min 180x54 px)
- **⏎** — Enter с акцентной рамкой (76x54 px)

### EmojiPanel
- Скрытая панель-заглушка
- Демо-строка из 8 эмоджи

## 🎨 Цветовая схема (iOS Dark)

| Элемент | Цвет | Hex |
|---------|------|-----|
| Фон клавиатуры | Dark gray | #1C1C1E |
| Фон панелей | Dark panel | #1E1F23 |
| Клавиша (normal) | Gray | #2C2C2E |
| Клавиша (pressed) | Light gray | #3A3A3C |
| Текст (normal) | Light | #F2F2F7 |
| Текст (pressed) | White | #FFFFFF |
| Акцент (Enter) | Purple-Cyan | #7B61FF → #00D1FF |

## 🎯 Режимы раскладки

1. **ABC** — QWERTY английская раскладка
   - 3 ряда букв
   - Специальные клавиши: Shift (⇧), Delete (⌫)

2. **123** — Цифры и символы
   - Цифры 0-9
   - Специальные символы: -/:;()$&@"
   - Переключатель #+=

3. **Emoji** — Панель эмоджи (заглушка)
   - Демо-строка смайлов

## 🤖 AI Integration Hooks

В коде добавлены комментарии для будущей интеграции с ChatGPT:

```python
# AI INTEGRATION HOOK: ChatGPT key press handler
# AI INTEGRATION HOOK: ChatGPT autocomplete suggestions
# AI INTEGRATION HOOK: Space bar long-press for voice/AI input
# AI INTEGRATION HOOK: Enter key sends message to AI
# AI INTEGRATION HOOK: Layout switch event
# AI INTEGRATION HOOK: Emoji/language selector
```

Эти якоря указывают места для:
- Обработки нажатий клавиш
- Автодополнения от AI
- Голосового ввода
- Отправки сообщений
- Смены раскладок
- Интеграции эмоджи

## 📐 Технические параметры

- **Размер окна**: 390 x 380 px
- **Размер клавиатуры**: 390 x 280 px
- **Safe area bottom**: 34 px
- **Межрядовый зазор**: 6 px
- **Межклавишный зазор**: 6 px
- **Базовая клавиша**: ≥44 x 52 px
- **Радиус скругления**: 12 px
- **Анимация нажатия**: 70-90 ms, scale 0.97, opacity 0.96

## 🔧 Особенности реализации

- Один файл `keyboard_widget.py` без .kv
- Все стили в Python коде
- Никаких сетевых вызовов
- Только визуальные элементы (без логики ввода/IME)
- ButtonBehavior + Widget для кастомных кнопок
- Kivy Canvas для графики
- Animation API для эффектов нажатия

## 📝 Примечания

- Это **визуальный прототип** — логика ввода и IME-хуки не реализованы
- Клавиши реагируют на нажатия визуально, но не вводят текст
- Готово к интеграции с ChatGPT API для автодополнения

## 🎓 Roadmap для AI интеграции

1. Подключение к ChatGPT API для предложений
2. Контекстно-зависимое автодополнение
3. Транскрипция голосового ввода
4. Умные рекомендации эмоджи
5. Мультиязычная поддержка с AI-переводом

