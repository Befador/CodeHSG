import curses
import random
import time

# Color constants matching your Snake game style
RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"
RED    = "\033[31m"
MAGENTA = "\033[35m"
WHITE  = "\033[37m"

# Snake-style boxed ASCII title for "ROCK PAPER SCISSORS"
ASCII_TITLE = [
    "╔══════════════════════════════════════════════════════════╗",
    "║                                                          ║",
    "║          R  O  C  K     P  A  P  E  R     S  C  I  S  S  O  R  S          ║",
    "║                                                          ║",
    "╚══════════════════════════════════════════════════════════╝",
]

# Finger ASCII art for rock, paper, scissors
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

CHOICES = ["rock", "paper", "scissors"]

def print_centered(stdscr, y, text, color_pair=0, bold=False):
    h, w = stdscr.getmaxyx()
    x = (w - len(text)) // 2
    attr = curses.color_pair(color_pair)
    if bold:
        attr |= curses.A_BOLD
    stdscr.addstr(y, x, text, attr)

def print_ascii_art(stdscr, start_y, art_lines, color_pair=0):
    h, w = stdscr.getmaxyx()
    for i, line in enumerate(art_lines):
        x = (w - len(line)) // 2
        stdscr.addstr(start_y + i, x, line, curses.color_pair(color_pair))

def print_title(stdscr):
    h, w = stdscr.getmaxyx()
    for i, line in enumerate(ASCII_TITLE):
        x = (w - len(line)) // 2
        stdscr.addstr(i + 1, x, line, curses.color_pair(2) | curses.A_BOLD)

def countdown(stdscr):
    h, w = stdscr.getmaxyx()
    for i in range(3, 0, -1):
        stdscr.clear()
        print_title(stdscr)
        print_centered(stdscr, h // 2, f"{i}...", color_pair=3, bold=True)
        stdscr.refresh()
        time.sleep(1)

def get_user_choice(stdscr):
    prompt = "Choose Rock (r), Paper (p), or Scissors (s): "
    h, w = stdscr.getmaxyx()
    while True:
        stdscr.clear()
        print_title(stdscr)
        print_centered(stdscr, h // 2 - 2, "Rock Paper Scissors", color_pair=5, bold=True)
        print_centered(stdscr, h // 2, prompt, color_pair=5)
        stdscr.refresh()
        c = stdscr.getch()
        if c in (ord('r'), ord('R')):
            return "rock"
        elif c in (ord('p'), ord('P')):
            return "paper"
        elif c in (ord('s'), ord('S')):
            return "scissors"

def decide_winner(user, comp):
    if user == comp:
        return "tie"
    wins = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
    return "user" if wins[user] == comp else "computer"

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    # Define color pairs matching your Snake game
    curses.init_pair(1, curses.COLOR_RED, -1)      # Computer win messages
    curses.init_pair(2, curses.COLOR_GREEN, -1)    # Title, user win messages
    curses.init_pair(3, curses.COLOR_YELLOW, -1)   # Countdown, tie messages
    curses.init_pair(4, curses.COLOR_CYAN, -1)     # User ASCII art
    curses.init_pair(5, curses.COLOR_MAGENTA, -1)  # Prompts & computer ASCII art

    rounds = 5
    user_score, comp_score = 0, 0

    for round_num in range(1, rounds + 1):
        stdscr.clear()
        print_title(stdscr)
        print_centered(stdscr, len(ASCII_TITLE) + 2, f"Round {round_num} of {rounds}", color_pair=3, bold=True)
        stdscr.refresh()

        user_choice = get_user_choice(stdscr)

        countdown(stdscr)

        comp_choice = random.choice(CHOICES)

        stdscr.clear()
        print_title(stdscr)
        # Show user choice and art
        print_centered(stdscr, len(ASCII_TITLE) + 4, f"You chose: {user_choice.upper()}", color_pair=4, bold=True)
        print_ascii_art(stdscr, len(ASCII_TITLE) + 6, ASCII_ART[user_choice], color_pair=4)

        # VERSUS banner
        print_centered(stdscr, len(ASCII_TITLE) + 13, "VERSUS", color_pair=3, bold=True)

        # Show computer choice and art
        print_centered(stdscr, len(ASCII_TITLE) + 15, f"Computer chose: {comp_choice.upper()}", color_pair=5, bold=True)
        print_ascii_art(stdscr, len(ASCII_TITLE) + 17, ASCII_ART[comp_choice], color_pair=5)
        stdscr.refresh()

        winner = decide_winner(user_choice, comp_choice)

        if winner == "user":
            result_msg = "You win this round!"
            color = 2
            user_score += 1
        elif winner == "computer":
            result_msg = "Computer wins this round!"
            color = 1
            comp_score += 1
        else:
            result_msg = "It's a tie!"
            color = 3

        print_centered(stdscr, len(ASCII_TITLE) + 24, result_msg, color_pair=color, bold=True)
        print_centered(stdscr, len(ASCII_TITLE) + 26, f"Score — You: {user_score}  Computer: {comp_score}", color_pair=5, bold=True)
        print_centered(stdscr, len(ASCII_TITLE) + 28, "Press any key to continue...", color_pair=5)
        stdscr.refresh()
        stdscr.getch()

    stdscr.clear()
    print_title(stdscr)
    if user_score > comp_score:
        final_msg = "CONGRATULATIONS! You won the game!"
        color = 2
    elif comp_score > user_score:
        final_msg = "SORRY! The computer won the game."
        color = 1
    else:
        final_msg = "IT'S A TIE GAME!"
        color = 3

    print_centered(stdscr, len(ASCII_TITLE) + 12, final_msg, color_pair=color, bold=True)
    print_centered(stdscr, len(ASCII_TITLE) + 14, f"Final Score — You: {user_score}  Computer: {comp_score}", color_pair=5, bold=True)
    print_centered(stdscr, len(ASCII_TITLE) + 16, "Press any key to exit.", color_pair=5)
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)