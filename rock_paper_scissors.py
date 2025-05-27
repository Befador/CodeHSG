#!/usr/bin/env python3
import curses
import random
import time
import locale

# Set terminal encoding for decoding user input gracefully
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

CHOICES = ["rock","paper","scissors"]

# ── DRAWING HELPERS ────────────────────────────────────────────────────────────

def print_centered(stdscr, y, text, color_pair, bold=False):
    h, w = stdscr.getmaxyx()
    x = max(0, min(w - len(text), (w - len(text)) // 2))
    attr = curses.color_pair(color_pair)
    if bold:
        attr |= curses.A_BOLD
    try:
        stdscr.addstr(y, x, text, attr)
    except curses.error:
        pass

def print_ascii_art(stdscr, start_y, art_lines, color_pair):
    h, w = stdscr.getmaxyx()
    for i, line in enumerate(art_lines):
        x = max(0, min(w - len(line), (w - len(line)) // 2))
        try:
            stdscr.addstr(start_y + i, x, line, curses.color_pair(color_pair))
        except curses.error:
            pass

def print_title(stdscr):
    h, w = stdscr.getmaxyx()
    for i, line in enumerate(ASCII_TITLE):
        x = max(0, min(w - len(line), (w - len(line)) // 2))
        try:
            stdscr.addstr(i, x, line, curses.color_pair(2)|curses.A_BOLD)
        except curses.error:
            pass

def print_score(stdscr, name, user_score, comp_score):
    h, w = stdscr.getmaxyx()
    score_text = f"{name}: {user_score}   AI: {comp_score}"
    # place on line 1, flush right with a 2-char margin
    y = 1
    x = max(0, w - len(score_text) - 2)
    try:
        stdscr.addstr(y, x, score_text, curses.color_pair(5)|curses.A_BOLD)
    except curses.error:
        pass

# ── INPUT HELPERS ──────────────────────────────────────────────────────────────

def prompt_name(stdscr, row):
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
    prompt = f"{name}, choose Rock (r), Paper (p) or Scissors (s): "
    while True:
        stdscr.move(row, 0)
        stdscr.clrtoeol()
        print_centered(stdscr, row, prompt, 5)
        stdscr.refresh()
        c = stdscr.getch()
        if c == 27:  # ESC key to exit
            return None
        if c in (ord('r'), ord('R')): return "rock"
        if c in (ord('p'), ord('P')): return "paper"
        if c in (ord('s'), ord('S')): return "scissors"

def countdown(stdscr, row):
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
    if user == comp:
        return "tie"
    wins = {"rock":"scissors","scissors":"paper","paper":"rock"}
    return "user" if wins[user] == comp else "computer"

def main(stdscr):
    # —— Initialize curses & colors —— 
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED,   -1)  # computer wins
    curses.init_pair(2, curses.COLOR_GREEN, -1)  # title & user wins
    curses.init_pair(3, curses.COLOR_YELLOW,-1)  # countdown & tie
    curses.init_pair(4, curses.COLOR_CYAN,  -1)  # user art
    curses.init_pair(5, curses.COLOR_MAGENTA,-1) # prompts & comp art

    # heights
    title_h = len(ASCII_TITLE)
    art_h   = len(ASCII_ART["rock"])

    # 1) Prompt for name
    stdscr.clear()
    print_title(stdscr)
    print_score(stdscr, "…", 0, 0)           # blank score until we know name
    name = prompt_name(stdscr, title_h + 1)
    time.sleep(0.3)

    # 2) Play best-of-5 (first to 3)
    user_score = comp_score = 0
    rounds     = 5
    needed     = rounds//2 + 1

    for rnd in range(1, rounds+1):
        stdscr.clear()
        print_title(stdscr)
        print_score(stdscr, name, user_score, comp_score)

        # Round header
        print_centered(stdscr, title_h + 1,
                       f"Round {rnd} of {rounds}", 3, bold=True)

        # Get user choice
        user_choice = get_user_choice(stdscr, title_h + 3, name)
        if user_choice is None:
            return  # exit gracefully if ESC pressed

        # Countdown
        countdown(stdscr, title_h + 5)

        # Computer picks
        comp_choice = random.choice(CHOICES)

        # Show both choices
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

        # Decide winner
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

        # Print round result + updated score
        res_y = title_h + 3 + art_h*2 + 6
        print_centered(stdscr, res_y, msg, col, bold=True)
        print_centered(stdscr, res_y + 2,
                       f"Score — {name}: {user_score}   AI: {comp_score}",
                       5, bold=True)
        print_centered(stdscr, res_y + 4, "Press any key to continue…", 5)
        stdscr.refresh()
        stdscr.getch()

        # early exit if someone already won best-of-5
        if user_score == needed or comp_score == needed:
            break

    # Final summary
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
    curses.wrapper(main)