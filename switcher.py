#!/usr/bin/env python3
"""Simple layout switcher similar to Caramba or Punto Switcher.

This script listens for keyboard events and can:
- Change layout of the previously typed word when double Shift is pressed.
- Automatically switch layout of a word when it seems typed in the wrong layout.

Events are logged to ``switcher.log`` so behaviour can be inspected later.

The implementation is simplified and intended for demonstration purposes.
"""
from __future__ import annotations

import argparse
import logging
import time
import re
from dataclasses import dataclass
from typing import Optional, Set

try:
    from pynput import keyboard
except ImportError:  # pragma: no cover - dependency missing
    keyboard = None  # type: ignore[assignment]

# Mapping between English and Russian layouts
ENG_KEYS = "qwertyuiop[]asdfghjkl;'zxcvbnm,./"
RUS_KEYS = "йцукенгшщзхъфывапролджэячсмитьбю."

EN_TO_RU = {e: r for e, r in zip(ENG_KEYS, RUS_KEYS)}
EN_TO_RU.update({e.upper(): r.upper() for e, r in zip(ENG_KEYS, RUS_KEYS)})
RU_TO_EN = {r: e for e, r in zip(ENG_KEYS, RUS_KEYS)}
RU_TO_EN.update({r.upper(): e.upper() for e, r in zip(ENG_KEYS, RUS_KEYS)})

LATIN_RE = re.compile(r"^[A-Za-z\[\];',./]+$")
CYRILLIC_RE = re.compile(r"^[А-Яа-яЁё]+$")

# Very small demonstration dictionaries. Real application should use
# comprehensive word lists.
ENGLISH_WORDS: Set[str] = {
    "hello", "how", "test", "word", "example", "python",
}
RUSSIAN_WORDS: Set[str] = {
    "привет", "как", "дела", "тест", "слово", "пример",
}


def switch_layout(word: str) -> str:
    """Return ``word`` converted to the opposite keyboard layout."""
    converted = []
    for ch in word:
        if ch in EN_TO_RU:
            converted.append(EN_TO_RU[ch])
        elif ch in RU_TO_EN:
            converted.append(RU_TO_EN[ch])
        else:
            converted.append(ch)
    return "".join(converted)


def detect_layout(word: str) -> str:
    if CYRILLIC_RE.match(word):
        return "ru"
    if LATIN_RE.match(word):
        return "en"
    return "mixed"


def auto_correct(word: str) -> Optional[str]:
    layout = detect_layout(word)
    switched = switch_layout(word)
    if layout == "en":
        if word.lower() not in ENGLISH_WORDS and switched.lower() in RUSSIAN_WORDS:
            return switched
    elif layout == "ru":
        if word.lower() not in RUSSIAN_WORDS and switched.lower() in ENGLISH_WORDS:
            return switched
    return None


@dataclass
class State:
    last_word: str = ""
    last_shift_ts: float = 0.0


class Listener:
    def __init__(self) -> None:
        if keyboard is None:
            raise SystemExit("pynput library is required: pip install pynput")
        self.state = State()
        self.ctrl = keyboard.Controller()
        logging.basicConfig(
            filename="switcher.log",
            level=logging.INFO,
            format="%(asctime)s %(message)s",
        )

    # Key handling -----------------------------------------------------
    def on_press(self, key: keyboard.KeyCode | keyboard.Key) -> None:
        try:
            char = key.char  # type: ignore[attr-defined]
        except AttributeError:
            char = ""

        if key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r):
            self._handle_shift()
            return

        if key == keyboard.Key.space or key == keyboard.Key.enter:
            self._handle_delim()
            return

        if char:
            self.state.last_word += char

    def _handle_shift(self) -> None:
        now = time.time()
        if now - self.state.last_shift_ts < 0.5 and self.state.last_word:
            switched = switch_layout(self.state.last_word)
            self._replace_last_word(switched)
            logging.info("double-shift: %s -> %s", self.state.last_word, switched)
            self.state.last_word = switched
        self.state.last_shift_ts = now

    def _handle_delim(self) -> None:
        if not self.state.last_word:
            return
        correction = auto_correct(self.state.last_word)
        if correction:
            self._replace_last_word(correction)
            logging.info("auto-switch: %s -> %s", self.state.last_word, correction)
        self.state.last_word = ""

    def _replace_last_word(self, new_word: str) -> None:
        # Remove previous characters
        for _ in range(len(self.state.last_word)):
            self.ctrl.press(keyboard.Key.backspace)
            self.ctrl.release(keyboard.Key.backspace)
        self.ctrl.type(new_word)

    # Public API ------------------------------------------------------
    def run(self) -> None:
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()


# Demo mode -----------------------------------------------------------

def run_demo() -> None:
    samples = ["ghbdtn", "hello", "ghbdtn", "ntrcn", "test"]
    print("Demo mode: showing auto-corrections")
    for w in samples:
        corr = auto_correct(w)
        print(f"{w} -> {corr}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple keyboard layout switcher")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="run demonstration instead of listening to keyboard",
    )
    args = parser.parse_args()
    if args.demo:
        run_demo()
    else:
        Listener().run()
