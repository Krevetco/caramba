# Simple Layout Switcher

This project provides a minimal Python implementation of a keyboard layout
switcher similar to Caramba Switcher or Punto Switcher.

## Features

- **Double Shift** — converts the previous word to the opposite keyboard layout.
- **Automatic switching** — when a word does not exist in the current language
  dictionary but exists after layout conversion, the word is automatically
  replaced.
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
