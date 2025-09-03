# Simple Layout Switcher

This project provides a minimal Python implementation of a keyboard layout
switcher similar to Caramba Switcher or Punto Switcher.

## Features

- **Double Shift** — converts the previous word or selected text and toggles the
  system layout.
- **Automatic switching** — when a word does not exist in the current language
  dictionary but exists after layout conversion, the word is automatically
  replaced.
- **Selection support** — double Shift also converts highlighted text.
- **Logging** — all switches are written to `switcher.log` so that behaviour can
  be inspected later.

## Usage

```bash
pip install -r requirements.txt
python switcher.py            # run listener
python switcher.py --demo     # run simple demo without keyboard hooks
```

The script is cross-platform but needs accessibility permissions to capture and
emit keyboard events on macOS.

## Dictionaries

For demonstration, the script ships with very small built‑in word lists. Edit
`ENGLISH_WORDS` and `RUSSIAN_WORDS` in `switcher.py` or load more comprehensive
dictionaries for better accuracy.

## 🇷🇺 Описание на русском

Проект реализует упрощённый переключатель раскладки.

### Возможности

- **Двойной Shift** — меняет раскладку предыдущего слова или выделенного
  фрагмента и переключает системную раскладку.
- **Автозамена** — если введённое слово не найдено в словаре текущего языка,
  но присутствует после смены раскладки, оно заменяется автоматически.
- **Работа с выделением** — выделенный текст тоже можно преобразовать двойным
  нажатием Shift.
- **Логирование** — все операции фиксируются в `switcher.log`.

### Использование

```bash
pip install -r requirements.txt
python switcher.py            # запустить прослушку клавиатуры
python switcher.py --demo     # демонстрационный режим без перехвата
```

Скрипт требует разрешения на управление компьютером в настройках
доступности macOS.
