#!/usr/bin/env python3
"""
DOCUMENTATION

In this script, the idea is to create a simple Hangman game in French and English that can be 
played in a terminal. 

As for the other games, there is a main menu that allows you to choose the language and start the game.
Additionally, one of the maain feature is the possibility to ask for a hint. This feature was a bit harder to
implement, or rather to scale up efficiently, because it requires a dictionary of words with their hints in both languages.

"""
# as usual we import the necessary modules
import os
import random
import sys
import time
from pathlib import Path
import json

# We set the styles parameters for the terminal output and the banner
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


# We load the dictionaries for both languages from JSON files.
DICTIONARIES = {
    "EN": json.load(open(Path(__file__).with_name("english_dict.json"))),
    "FR": json.load(open(Path(__file__).with_name("french_dict.json")))
}

# Maximum number of incorrect tries allowed before losing
# (this can be adjusted to make the game easier or harder)
MAX_TRIES = 6

def clear():
    """
    Clear the terminal screen using the appropriate system command.
    """
    os.system("cls" if os.name == "nt" else "clear") # 'cls' for Windows, 'clear' for Unix-like systems

# This function is used to display the language selection menu and return the chosen language code. The way we do it
# is by using print statements to show the options and then waiting for the user to input their choice.
def get_language_choice():
    """
    Display the language selection menu and return the chosen language code.
    
    Returns:
        str: 'EN' for English or 'FR' for French.
    """
    clear()
    print("\n".join(BANNER))
    print()
    print(f"{BOLD}Choose a language / Choisissez une langue:{RESET}")
    print("1. English")
    print("2. Français")
    while True:
        choice = input("> ").strip() # Get user input and strip whitespace
        if choice == "1": # If the user chooses English
            return "EN"
        if choice == "2": # If the user chooses French
            return "FR"

def select_word(language): 
    """
    Select a random word and its hint from the dictionary for the given language.

    Parameters:
        language (str): Language code ('EN' or 'FR').

    Returns:
        tuple: (word, hint) where word is the secret word and hint is its description.
    """
    word = random.choice(list(DICTIONARIES[language].keys())) # Randomly select a word from the dictionary
    hint = DICTIONARIES[language][word] # Get the corresponding hint for the selected word
    return word, hint # Return the word and its hint

# The key challenge was to have an easily scalable way to create hints. For now, we have randomly selected words from a dictionary and then
# asked an LLM to generate hints for them. This way, we can easily add more words and hints without changing the code.

# Another way I thought implementing it was to download open-source datasets of words and their definitions,
# but I didn't find any that were easy to use and the size of the dataset was too big for this project. (especially considering the later upload to GitHub)

def render(word, guessed):
    """
    Render the word's current state, showing guessed letters and underscores.

    Parameters:
        word (str): The secret word.
        guessed (set): Set of letters that have been guessed.

    Returns:
        str: The formatted display of the word.
    """
    return " ".join([c if c in guessed else "_" for c in word]) 


def print_status(word, guessed, tries, language, hint_used=False, hint=None):
    """
    Display the game status screen, including hangman art, current word, guesses, and hint.

    Parameters:
        word (str): The secret word.
        guessed (set): Set of letters that have been guessed.
        tries (int): Number of incorrect guesses so far.
        language (str): Current language code.
        hint_used (bool): Whether the hint has been used.
        hint (str): The hint text to display if used.
    """
    clear()
    print("\n".join(BANNER))
    print()
    # art for hangman states keyed by number of incorrect tries
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

    # as usual, we use print statements to display the current status of the game and the hangman art.

def end_screen(word, won, language):
    """
    Show the end-of-game screen, indicate win or loss, and ask to play again.

    Parameters:
        word (str): The secret word.
        won (bool): True if the player guessed the word.
        language (str): Current language code.

    Returns:
        bool: True if the player wants to play another round.
    """
    print()
    if won:
        print(GREEN + BOLD + ("You win!" if language == "EN" else "Gagné !") + RESET)
    else:
        print(RED + BOLD + ("You lose!" if language == "EN" else "Perdu !") + RESET)
        print(f"The word was: {CYAN}{word}{RESET}")
    print()
    print("Play again? (y/n) / Rejouer ? (o/n)") # I made it so that you can answer in both languages.
    while True:
        again = input("> ").lower()
        if again in ("y", "o"):
            return True
        if again in ("n",):
            return False


# This function is the main game loop, where we handle the language selection, word guessing, and replay logic.
def main():
    """
    Main game loop: handle language selection, word guessing, and replay logic.
    """
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
            if guess == "0" and not hint_used and tries <= MAX_TRIES - 3: # The max tries can be changed above.
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

        print_status(word, guessed, tries, language, hint_used, hint)   # Display the final status after the loop ends
        won = all(c in guessed for c in word) # Check if the player won by guessing all letters
        # If the player won, we display a message and ask if they want to play again.
        if not end_screen(word, won, language):
            break

if __name__ == "__main__": # This is the entry point of the script, where we call the main function to start the game.
    main()

# print a smiley (or my attempt to make one)
def print_smiley():
    """
    Print a decorative smiley face.
    """
    print("  ^_^  ")
    print(" (o o) ")
    print("  \\_/  ")
    print("   |   ")
    print("  / \\  ")
    print(" /   \\ ")
    print("/     \\")