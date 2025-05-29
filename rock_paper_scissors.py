#!/usr/bin/env python3
"""
DOCUMENTATION

This script implements a terminal-based Rock-Paper-Scissors game using the curses library.
It displays an ASCII-art title, prompts the player for their name, and then runs a best-of-5
match against the computer opponent.  Key features include:

- Centered title, prompts, and ASCII art for rock/paper/scissors.
- A countdown of 3 2 1 before each round.
- Colourized output to highlight wins, losses, & ties.
- Easay exit via the ESC key at any prompt.
"""

# ── IMPORTS & LOCALE SETUP ─────────────────────────────────────────────────────
import curses       # for character-cell display handling
import random       # for computer’s random choice
import time         # for countdown delays
import locale       # to handle wide/Unicode characters in user input

# Ensure the terminal can decode user-entered names properly
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

# ── CONFIGURATION ─────────────────────────────────────────────────────────────
ASCII_TITLE = [
    "╔══════════════════════════════════════════════════════════╗",
    "║                                                          ║",
    "║  R  O  C  K     P  A  P  E  R    S  C  I  S  S  O  R  S  ║",
    "║                                                          ║",
    "╚══════════════════════════════════════════════════════════╝",
]

# Pre-defined ASCII art for each choice
ASCII_ART = {
    "rock": [
        "    _______",
        "---'   ____)",
        "      (_____)",
        "      (_____)",
        "      (____)",
        "---.__(___)"
    ],
    "paper": [
        "     _______",
        "---'    ____)____",
        "           ______)",
        "          _______)",
        "         _______)",
        "---.__________)"
    ],
    "scissors": [
        "    _______",
        "---'   ____)____",
        "          ______)",
        "       __________)",
        "      (____)",
        "---.__(___)"
    ],
}

CHOICES = ["rock", "paper", "scissors"]  # Valid moves

# ── DRAWING HELPERS ────────────────────────────────────────────────────────────
def print_centered(stdscr, y, text, color_pair, bold=False):
    """
    Print a single line of text centered horizontally at row y.

    Args:
        stdscr        : the main curses window
        y (int)       : row on which to print
        text (str)    : the string to display
        color_pair (int): curses color pair number
        bold (bool)   : whether to add a bold attribute
    """
    h, w = stdscr.getmaxyx()
    x = max(0, min(w - len(text), (w - len(text)) // 2))
    attr = curses.color_pair(color_pair)
    if bold:
        attr |= curses.A_BOLD
    try:
        stdscr.addstr(y, x, text, attr)
    except curses.error:
        # Ignoring errors when window is too small
        pass

def print_ascii_art(stdscr, start_y, art_lines, color_pair):
    """
    Render multi-line ASCII art centered horizontally.

    Args:
        stdscr        : the curses window
        start_y (int) : top row for the art
        art_lines (list[str]): lines of ASCII art
        color_pair (int): curses color pair for the art
    """
    h, w = stdscr.getmaxyx()
    for i, line in enumerate(art_lines):
        x = max(0, min(w - len(line), (w - len(line)) // 2))
        try:
            stdscr.addstr(start_y + i, x, line, curses.color_pair(color_pair))
        except curses.error:
            pass

def print_title(stdscr):
    """
    Display the ASCII_TITLE banner at the top of the screen.
    """
    h, w = stdscr.getmaxyx()
    for i, line in enumerate(ASCII_TITLE):
        x = max(0, min(w - len(line), (w - len(line)) // 2))
        try:
            stdscr.addstr(i, x, line, curses.color_pair(2) | curses.A_BOLD)
        except curses.error:
            pass

def print_score(stdscr, name, user_score, comp_score):
    """
    Show the current score in the top-right corner.

    Args:
        stdscr      : the curses window
        name (str)  : player’s name
        user_score (int) : player’s score
        comp_score (int) : computer’s score
    """
    h, w = stdscr.getmaxyx()
    score_text = f"{name}: {user_score}   AI: {comp_score}"
    y = 1
    x = max(0, w - len(score_text) - 2)
    try:
        stdscr.addstr(y, x, score_text, curses.color_pair(5) | curses.A_BOLD)
    except curses.error:
        pass

# ── INPUT HELPERS ──────────────────────────────────────────────────────────────
def prompt_name(stdscr, row):
    """
    Prompt the player to enter their name.

    Args:
        stdscr : curses window
        row (int): vertical position to display prompt

    Returns:
        str: the entered name (defaults to "Player" if blank)
    """
    prompt = "Enter your name: "
    curses.echo()
    print_centered(stdscr, row, prompt, 5, bold=True)
    stdscr.refresh()
    h, w = stdscr.getmaxyx()
    col = min(w - 1, (w - len(prompt)) // 2 + len(prompt))
    name = stdscr.getstr(row, col, 20).decode(code).strip()
    curses.noecho()
    return name or "Player"

def get_user_choice(stdscr, row, name):
    """
    Prompt and read one of (r/p/s) or ESC to quit.

    Args:
        stdscr : curses window
        row (int): where to display the prompt
        name (str): player’s name for personalization

    Returns:
        "rock"|"paper"|"scissors"|None
    """
    prompt = f"{name}, choose Rock (r), Paper (p) or Scissors (s): "
    while True:
        stdscr.move(row, 0)
        stdscr.clrtoeol()
        print_centered(stdscr, row, prompt, 5)
        stdscr.refresh()
        c = stdscr.getch()
        if c == 27:  # ESC key
            return None
        if c in (ord('r'), ord('R')): return "rock"
        if c in (ord('p'), ord('P')): return "paper"
        if c in (ord('s'), ord('S')): return "scissors"

def countdown(stdscr, row):
    """
    Display a 3-2-1 countdown before revealing choices.

    Args:
        stdscr : curses window
        row (int): row for countdown text
    """
    for i in (3, 2, 1):
        stdscr.move(row, 0)
        stdscr.clrtoeol()
        print_centered(stdscr, row, f"{i}...", 3, bold=True)
        stdscr.refresh()
        time.sleep(1)
    stdscr.move(row, 0)
    stdscr.clrtoeol()
    stdscr.refresh()

# ── GAME LOGIC ────────────────────────────────────────────────────────────────
def decide_winner(user, comp):
    """
    Determine outcome of one round.

    Args:
        user (str): user’s choice
        comp (str): computer’s choice

    Returns:
        "user" | "computer" | "tie"
    """
    if user == comp:
        return "tie"
    wins = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
    return "user" if wins[user] == comp else "computer"

def main(stdscr):
    """
    Main loop: initialize curses, get name, play best-of-5, and show final result.
    """
    # —— Initialize curses & colors —— 
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.start_color()
    curses.use_default_colors()
    # Define color pairs for results, UI elements, and art
    curses.init_pair(1, curses.COLOR_RED,   -1)  # computer wins
    curses.init_pair(2, curses.COLOR_GREEN, -1)  # title & user wins
    curses.init_pair(3, curses.COLOR_YELLOW,-1)  # countdown & tie
    curses.init_pair(4, curses.COLOR_CYAN,  -1)  # user art
    curses.init_pair(5, curses.COLOR_MAGENTA,-1) # prompts & comp art

    title_h = len(ASCII_TITLE)          # height of banner
    art_h   = len(ASCII_ART["rock"])    # height of rock art

    # 1) Prompt for player name
    stdscr.clear()
    print_title(stdscr)
    print_score(stdscr, "…", 0, 0)      # placeholder score
    name = prompt_name(stdscr, title_h + 1)
    time.sleep(0.3)

    # 2) Play best-of-5 rounds
    user_score = comp_score = 0
    rounds     = 5
    needed     = rounds // 2 + 1

    for rnd in range(1, rounds + 1):
        stdscr.clear()
        print_title(stdscr)
        print_score(stdscr, name, user_score, comp_score)

        # Round header
        print_centered(stdscr, title_h + 1,
                       f"Round {rnd} of {rounds}", 3, bold=True)

        # a) Get user’s move (or exit)
        user_choice = get_user_choice(stdscr, title_h + 3, name)
        if user_choice is None:
            return  # user pressed ESC

        # b) Countdown
        countdown(stdscr, title_h + 5)

        # c) Computer random move
        comp_choice = random.choice(CHOICES)

        # d) Display both choices with ASCII art
        stdscr.clear()
        print_title(stdscr)
        print_score(stdscr, name, user_score, comp_score)

        print_centered(stdscr, title_h + 1,
                       f"{name} chose: {user_choice.upper()}", 4, bold=True)
        print_ascii_art(stdscr, title_h + 3, ASCII_ART[user_choice], 4)

        print_centered(stdscr, title_h + 3 + art_h + 1,
                       "VERSUS", 3, bold=True)

        print_centered(stdscr, title_h + 3 + art_h + 3,
                       f"Computer chose: {comp_choice.upper()}", 5, bold=True)
        print_ascii_art(stdscr, title_h + 3 + art_h + 5,
                        ASCII_ART[comp_choice], 5)

        stdscr.refresh()
        time.sleep(1)

        # e) Decide winner and update score
        result = decide_winner(user_choice, comp_choice)
        if result == "user":
            msg = "You win this round!"
            user_score += 1
            col = 2
        elif result == "computer":
            msg = "Computer wins this round!"
            comp_score += 1
            col = 1
        else:
            msg = "It's a tie!"
            col = 3

        # f) Show round result and wait for key
        res_y = title_h + 3 + art_h * 2 + 6
        print_centered(stdscr, res_y, msg, col, bold=True)
        print_centered(stdscr, res_y + 2,
                       f"Score — {name}: {user_score}   AI: {comp_score}",
                       5, bold=True)
        print_centered(stdscr, res_y + 4, "Press any key to continue…", 5)
        stdscr.refresh()
        stdscr.getch()

        # Early exit if match decided
        if user_score == needed or comp_score == needed:
            break

    # ── Final match summary ───────────────────────────────────────────────
    stdscr.clear()
    print_title(stdscr)
    print_score(stdscr, name, user_score, comp_score)

    if user_score > comp_score:
        final = "CONGRATULATIONS! You won the match!"
        col = 2
    elif comp_score > user_score:
        final = "SORRY! The computer won the match."
        col = 1
    else:
        final = "IT'S A DRAW!"
        col = 3

    print_centered(stdscr, title_h + 2, final, col, bold=True)
    print_centered(stdscr, title_h + 4,
                   f"Final Score — {name}: {user_score}   AI: {comp_score}",
                   5, bold=True)
    print_centered(stdscr, title_h + 6, "Press any key to exit…", 5)
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    # Wrap main in curses.wrapper to ensure proper cleanup on exit
    curses.wrapper(main)