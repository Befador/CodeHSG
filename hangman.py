#!/usr/bin/env python3
"""
Retro-styled bilingual Hangman game (English / French).
"""

import os
import random
import sys
import time
from pathlib import Path

# ── ANSI style ──────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"
RED    = "\033[31m"

BANNER = [
    "╔═══════════════════════════════════════╗",
    "║          H  A  N  G  M  A  N          ║",
    "╚═══════════════════════════════════════╝"
]

# ── Load dictionary from external JSON ────────────────────────────────
import json
DICTIONARIES = {
    "EN": json.load(open(Path(__file__).with_name("english_dict.json"))),
    "FR": json.load(open(Path(__file__).with_name("french_dict.json")))
}

MAX_TRIES = 6

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def get_language_choice():
    clear()
    print("\n".join(BANNER))
    print()
    print(f"{BOLD}Choose a language / Choisissez une langue:{RESET}")
    print("1. English")
    print("2. Français")
    while True:
        choice = input("> ").strip()
        if choice == "1":
            return "EN"
        if choice == "2":
            return "FR"

def select_word(language):
    word = random.choice(list(DICTIONARIES[language].keys()))
    hint = DICTIONARIES[language][word]
    return word, hint

def render(word, guessed):
    return " ".join([c if c in guessed else "_" for c in word])

def print_status(word, guessed, tries, language, hint_used=False, hint=None):
    clear()
    print("\n".join(BANNER))
    print()
    gallows = [
        "",
        "  O  ",
        "  O  \n  |  ",
        "  O  \n /|  ",
        "  O  \n /|\\",
        "  O  \n /|\\\n /   ",
        "  O  \n /|\\\n / \\"
    ]
    print(RED + gallows[tries] + RESET)
    print()
    print(render(word, guessed))
    print()
    print(f"{YELLOW}Guessed: {', '.join(sorted(guessed))}{RESET}")
    print(f"{CYAN}Tries left: {MAX_TRIES - tries}{RESET}")
    print()
    if hint_used and hint:
        print(f"{CYAN}Hint: {hint}{RESET}")
    print(f"{CYAN}(Press 0 to get a hint - costs 3 tries. ESC to quit to menu){RESET}")

def end_screen(word, won, language):
    print()
    if won:
        print(GREEN + BOLD + ("You win!" if language == "EN" else "Gagné !") + RESET)
    else:
        print(RED + BOLD + ("You lose!" if language == "EN" else "Perdu !") + RESET)
        print(f"The word was: {CYAN}{word}{RESET}")
    print()
    print("Play again? (y/n) / Rejouer ? (o/n)")
    while True:
        again = input("> ").lower()
        if again in ("y", "o"):
            return True
        if again in ("n",):
            return False

def main():
    while True:
        language = get_language_choice()
        word, hint = select_word(language)
        guessed = set()
        tries = 0
        hint_used = False

        while tries < MAX_TRIES and not all(c in guessed for c in word):
            print_status(word, guessed, tries, language, hint_used, hint)
            guess = input("> ").strip()
            if guess == "\x1b":  # ESC key
                return
            if guess == "0" and not hint_used and tries <= MAX_TRIES - 3:
                hint_used = True
                tries += 3
                continue
            guess = guess.upper()
            if not guess.isalpha() or len(guess) != 1:
                continue
            if guess in guessed:
                continue
            guessed.add(guess)
            if guess not in word:
                tries += 1

        print_status(word, guessed, tries, language, hint_used, hint)
        won = all(c in guessed for c in word)
        if not end_screen(word, won, language):
            break

if __name__ == "__main__":
    main()