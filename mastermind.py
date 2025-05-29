#!/usr/bin/env python3
"""
DOCUMENTATION

This script implements a terminal-based Mastermind game using simple console I/O
and colored output via Colorama. Players can:

- Enter their name.
- Choose a digit range for the secret code (1–6 or 0–9).
- Select difficulty (easy: 10 attempts, hard: 6 attempts).
- Attempt to guess a 4-digit secret code within the defined number of tries.
- Receive feedback on “exact” (correct digit & position) and “partial” (correct digit, wrong position) matches.
- Exit easily at any prompt by typing ESC or teh literal “^[”.
"""

# ── IMPORTS & INITIALIZATION ───────────────────────────────────────────────────
import os                         # for clearing the console
import random                     # for secret code generation
from colorama import init, Fore, Style  # for colored terminal text

# Initialize Colorama to auto-reset styles after each print
init(autoreset=True)

# ── COLOUR CONSTANTS ───────────────────────────────────────────────────────────
RESET   = Style.RESET_ALL
BOLD    = Style.BRIGHT
GREEN   = Fore.GREEN
YELLOW  = Fore.YELLOW
CYAN    = Fore.CYAN
MAGENTA = Fore.MAGENTA
RED     = Fore.RED

# ── ASCII BANNER ───────────────────────────────────────────────────────────────
ASCII_MASTERMIND = f"""{GREEN}{BOLD}
╔════════════════════════════════════════╗
║                                        ║
║      M  A  S  T  E  R  M  I  N  D      ║
║                                        ║
╚════════════════════════════════════════╝
{RESET}
"""

def clear() -> None:
    """
    Clear the console screen in a cross-platform way.
    Uses 'cls' on Windows and 'clear' on Unix-like systems.
    """
    os.system("cls" if os.name == "nt" else "clear")

def print_header(player_name: str, attempt: int, max_attempts: int) -> None:
    """
    Clear the screen and display the Mastermind banner plus the player's status.

    Args:
        player_name (str): Name of the current player.
        attempt (int):     Current attempt number.
        max_attempts (int):Total allowed attempts.
    """
    clear()
    # Print the colored ASCII banner without adding an extra newline
    print(ASCII_MASTERMIND, end="")
    # Build a status line showing player name and round info, right-aligned
    status = f"{MAGENTA}{player_name}{RESET}   {CYAN}Round:{RESET} {attempt}/{max_attempts}"
    print(status.rjust(80))

def input_or_exit(prompt: str = "") -> str:
    """
    Prompt the user for input. If they type ESC (or the literal "^["),
    raise KeyboardInterrupt to signal an exit to the main menu.

    Args:
        prompt (str): Text to display before reading input.

    Returns:
        str: The stripped user input.
    """
    try:
        user_input = input(prompt)
        # If the user types the two-character sequence ^[, treat as ESC
        if user_input.strip() == "^[":  
            raise KeyboardInterrupt
        # If a single ESC character was entered
        if user_input and len(user_input) == 1 and ord(user_input) == 27:
            raise KeyboardInterrupt
    except KeyboardInterrupt:
        # Reraise so outer code can catch it
        raise
    return user_input.strip()

def get_player_name() -> str:
    """
    Prompt the player to enter their name at the start of the game.
    Names them to "Player" if they enter nothing.

    Returns:
        str: The chosen or default player name.
    """
    clear()
    print(ASCII_MASTERMIND)
    name = input_or_exit(f"{MAGENTA}Enter your name: {RESET}")
    return name if name else "Player"

def choose_range() -> tuple[int, int]:
    """
    Let the player select the digit range for the secret code:
      1) 1–6
      2) 0–9

    Returns:
        (min_digit, max_digit): Tuple of ints defining the inclusive range.
    """
    clear()
    print(ASCII_MASTERMIND)
    print(f"{CYAN}Select digit range:{RESET}")
    print("  1) 1–6")
    print("  2) 0–9")
    while True:
        choice = input_or_exit(f"{MAGENTA}Enter 1 or 2: {RESET}")
        if choice == "1":
            return 1, 6
        if choice == "2":
            return 0, 9
        # Prompt again on invalid input
        print(f"{RED}Invalid choice. Please enter 1 or 2.{RESET}")

def choose_difficulty() -> int:
    """
    Let the player select difficulty level:
      1) Easy   → 10 attempts
      2) Hard   → 6 attempts

    Returns:
        int: Maximum number of attempts allowed.
    """
    clear()
    print(ASCII_MASTERMIND)
    print(f"{CYAN}Select difficulty:{RESET}")
    print("  1) Easy   (10 attempts)")
    print("  2) Hard   (6 attempts)")
    while True:
        choice = input_or_exit(f"{MAGENTA}Enter 1 or 2: {RESET}")
        if choice == "1":
            return 10
        if choice == "2":
            return 6
        print(f"{RED}Invalid choice. Please enter 1 or 2.{RESET}")

def generate_code(length: int, min_digit: int, max_digit: int) -> list[str]:
    """
    Generate a random secret code of the given length and digit range.

    Args:
        length (int):    Number of digits in the code.
        min_digit (int): Minimum digit value (inclusive).
        max_digit (int): Maximum digit value (inclusive).

    Returns:
        list[str]: The secret code as a list of digit strings.
    """
    return [str(random.randint(min_digit, max_digit)) for _ in range(length)]

def grade_guess(secret: list[str], guess: list[str]) -> tuple[int, int]:
    """
    Compare the player's guess against the secret code.

    Args:
        secret (list[str]): The secret code digits.
        guess  (list[str]): The player's guessed digits.

    Returns:
        (exact, partial):
          exact   = number of digits correct in both value and position.
          partial = number of correct digits in wrong positions.
    """
    # Count exact matches first
    exact = sum(s == g for s, g in zip(secret, guess))

    # Build lists of non-matching digits for partial check
    rem_secret = []
    rem_guess  = []
    for s, g in zip(secret, guess):
        if s != g:
            rem_secret.append(s)
            rem_guess.append(g)

    # Count partial matches without double-counting
    partial = 0
    for g in rem_guess:
        if g in rem_secret:
            partial += 1
            rem_secret.remove(g)

    return exact, partial

def main() -> None:
    """
    Main game loop: set up player, generate secret code, process each attempt,
    give feedback, and handle win/lose conditions. Exits gracefully on ESC.
    """
    try:
        CODE_LEN = 4  # Number of digits in the secret code

        # 1) Player setup
        player     = get_player_name()
        min_d, max_d = choose_range()
        max_tries  = choose_difficulty()

        # Intro screen
        print_header(player, 0, max_tries)
        print(f"{YELLOW}I’ve chosen a {CODE_LEN}-digit code, digits {min_d}–{max_d}.{RESET}")
        print(f"{YELLOW}You have {max_tries} attempts to crack it!{RESET}")
        input_or_exit("\nPress ENTER to begin…")

        # 2) Secret code generation and guessing loop
        secret = generate_code(CODE_LEN, min_d, max_d)
        for attempt in range(1, max_tries + 1):
            print_header(player, attempt, max_tries)

            # Prompt for a valid guess
            while True:
                raw = input_or_exit(f"{CYAN}Attempt {attempt}/{max_tries}, enter {CODE_LEN} digits ({min_d}–{max_d}): {RESET}")
                if (len(raw) == CODE_LEN
                    and all(ch.isdigit() for ch in raw)
                    and all(min_d <= int(ch) <= max_d for ch in raw)):
                    break
                print(f"{RED}Invalid: need {CODE_LEN} digits between {min_d} and {max_d}.{RESET}")

            # Grade the guess
            exact, partial = grade_guess(secret, list(raw))

            # Win condition
            if exact == CODE_LEN:
                print_header(player, attempt, max_tries)
                print(f"\n{GREEN} Cracked in {attempt} {'try' if attempt==1 else 'tries'}! Code was {''.join(secret)}.{RESET}\n")
                break

            # Feedback and continue
            print(f"{GREEN}Exact matches   (correct digit & position):{RESET} {exact}")
            print(f"{YELLOW}Partial matches (correct digit, wrong position):{RESET} {partial}\n")
            input_or_exit("Press ENTER for next round…")
        else:
            # Ran out of attempts
            print_header(player, max_tries, max_tries)
            print(f"\n{RED}Out of attempts! The code was {''.join(secret)}.{RESET}\n")

        input_or_exit("Press ENTER to return to the main menu…")

    except KeyboardInterrupt:
        # Handle user-initiated exit (ESC key)
        print(f"\n{RED}Returning to main menu...{RESET}")

if __name__ == "__main__":
    main()