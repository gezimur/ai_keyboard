# Руководство по загрузке иконок

## Обзор

Виртуальная клавиатура поддерживает загрузку иконок в форматах SVG, PNG, JPG и других изображений через функцию `load_icon()`.

## Установка зависимостей

Для поддержки SVG иконок установите необходимые библиотеки:

```bash
pip install -r requirements.txt
```

Или вручную:

```bash
pip install cairosvg pillow
```

**Примечание:** Если библиотеки не установлены, система автоматически попытается загрузить SVG как обычное изображение (может не работать для некоторых SVG).

## Функция load_icon()

### Описание

```python
load_icon(icon_path, size=(24, 24))
```

**Параметры:**
- `icon_path` (str): Путь к файлу иконки (относительный или абсолютный)
- `size` (tuple): Размер иконки (width, height) для SVG файлов

**Возвращает:**
- `CoreImage` object или `None` если файл не найден

### Особенности

- **Кэширование**: Иконки кэшируются для повышения производительности
- **SVG поддержка**: Автоматическая конвертация SVG в PNG
- **Fallback**: Если cairosvg не установлен, попытка загрузить как обычное изображение

## Примеры использования

### 1. Простая загрузка SVG иконки

```python
# Загрузка SVG иконки размером 24x24
icon = load_icon('icons/del.svg', size=(24, 24))
```

### 2. Использование в стилях кнопок

```python
# Через make_dark_key_button_style
delete_button = ButtonWithIcon(
    make_dark_key_button_style(icon='icons/del.svg')
)

# Или напрямую через StyleMap
style = StyleMap(
    icon='icons/enter.svg',
    background=ButtonColor(color_normal=COLORS['accent_purple']),
    border_radius=6,
    text=None
)
button = ButtonWithIcon(style)
```

### 3. Динамическая установка иконки

```python
# Создание кнопки
button = ButtonWithIcon(make_key_button_style(text='Del'))

# Позже установка иконки
button.set_icon('icons/del.svg')
```

### 4. Разные иконки для разных состояний

```python
# Создание ButtoIcon с разными иконками для normal/checked состояний
icon = ButtoIcon(
    icon_normal='icons/mic_off.svg',
    icon_checked='icons/mic_on.svg'
)

style = StyleMap(
    icon=icon,
    background=ButtonColor(color_normal=COLORS['key_normal']),
    border_radius=6
)
button = ButtonWithIcon(style)
```

### 5. Загрузка PNG/JPG иконок

```python
# Функция работает с любыми форматами изображений
png_icon = load_icon('icons/logo.png', size=(32, 32))
jpg_icon = load_icon('icons/avatar.jpg', size=(48, 48))
```

## Структура директории иконок

```
keyboard7/
├── icons/
│   ├── del.svg          # Иконка удаления
│   ├── enter.svg        # Иконка Enter
│   ├── lang.svg         # Иконка смены языка
│   ├── mic_on.svg       # Иконка микрофона (включен)
│   ├── mic_off.svg      # Иконка микрофона (выключен)
│   └── ...
├── keyboard_widget.py
└── requirements.txt
```

## Создание собственных SVG иконок

### Рекомендации по SVG

1. **Размер**: Используйте viewBox для масштабируемости
2. **Цвета**: Используйте `currentColor` для автоматической адаптации цвета
3. **Простота**: Избегайте сложных эффектов и градиентов
4. **Оптимизация**: Используйте SVGO для оптимизации файлов

### Пример простой SVG иконки

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
</svg>
```

## Обработка ошибок

Функция `load_icon()` обрабатывает следующие ошибки:

```python
# Файл не найден
icon = load_icon('icons/nonexistent.svg')  # Вернёт None, выведет warning

# Библиотека не установлена
# Выведет предупреждение и попытается загрузить как обычное изображение

# Ошибка загрузки
# Выведет error и вернёт None
```

## Производительность

- **Кэширование**: Иконки кэшируются по ключу `{path}_{width}x{height}`
- **Повторная загрузка**: Повторные вызовы с теми же параметрами возвращают кэшированную версию
- **Память**: Кэш хранится в памяти на всё время работы приложения

## Отладка

Для отладки загрузки иконок проверьте консоль на наличие сообщений:

```
[WARNING] Icon file not found: icons/del.svg
[WARNING] cairosvg or PIL not installed. Install with: pip install cairosvg pillow
[INFO] Falling back to regular image loading for: icons/del.svg
[ERROR] Failed to load icon icons/del.svg: [error message]
```

## Примеры из keyboard_widget.py

### Кнопка удаления с иконкой

```python
self.delete_button = ButtonWithIcon(make_dark_key_button_style(icon='icons/del.svg'))
self.delete_button.size_hint_x = None
self.delete_button.size = (57, 52)
```

### Кнопка Enter с иконкой

```python
self.enter_button = ButtonWithIcon(make_accent_button_style(icon='icons/enter.svg'))
self.enter_button.size_hint_x = 1.1
```

### Кнопка смены языка с иконкой

```python
self.lang_button = ButtonWithIcon(make_key_button_style(icon='icons/lang.svg'))
self.lang_button.size_hint_x = 1.0
```

## FAQ

**Q: Можно ли использовать внешние URL для иконок?**  
A: Нет, функция работает только с локальными файлами.

**Q: Какой максимальный размер иконки?**  
A: Ограничений нет, но для производительности рекомендуется использовать размеры до 128x128.

**Q: Можно ли анимировать SVG иконки?**  
A: Нет, SVG конвертируется в статичное PNG изображение.

**Q: Работает ли функция на Android/iOS?**  
A: Да, при условии, что установлены необходимые библиотеки (cairosvg, pillow).

## Лицензия

Убедитесь, что используемые SVG иконки имеют соответствующую лицензию для вашего проекта.


