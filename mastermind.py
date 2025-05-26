#!/usr/bin/env python3
import os
import random
from colorama import init, Fore, Style

# ── Colour constants (match main menu & hangman) ─────────────────────────────
init(autoreset=True)
RESET   = Style.RESET_ALL
BOLD    = Style.BRIGHT
GREEN   = Fore.GREEN
YELLOW  = Fore.YELLOW
CYAN    = Fore.CYAN
MAGENTA = Fore.MAGENTA
RED     = Fore.RED

# ── ASCII banner for Mastermind ───────────────────────────────────────────────
ASCII_MASTERMIND = f"""{GREEN}{BOLD}
╔════════════════════════════════════════╗
║                                        ║
║      M  A  S  T  E  R  M  I  N  D      ║
║                                        ║
╚════════════════════════════════════════╝
{RESET}
"""

def clear():
    os.system("cls" if os.name=="nt" else "clear")

def print_header(player_name: str, attempt: int, max_attempts: int):
    """Clear & re-print banner plus top-right status bar."""
    clear()
    print(ASCII_MASTERMIND, end="")
    status = f"{MAGENTA}{player_name}{RESET}   {CYAN}Round:{RESET} {attempt}/{max_attempts}"
    print(status.rjust(80))
    print()

def get_player_name() -> str:
    clear()
    print(ASCII_MASTERMIND)
    name = input(f"{MAGENTA}Enter your name: {RESET}").strip()
    return name if name else "Player"

def choose_range() -> tuple[int,int]:
    clear()
    print(ASCII_MASTERMIND)
    print(f"{CYAN}Select digit range:{RESET}")
    print("  1) 1–6")
    print("  2) 0–9")
    while True:
        choice = input(f"{MAGENTA}Enter 1 or 2: {RESET}").strip()
        if choice == "1":
            return 1, 6
        if choice == "2":
            return 0, 9
        print(f"{RED}Invalid choice. Please enter 1 or 2.{RESET}")

def choose_difficulty() -> int:
    clear()
    print(ASCII_MASTERMIND)
    print(f"{CYAN}Select difficulty:{RESET}")
    print("  1) Easy   (10 attempts)")
    print("  2) Hard   (6 attempts)")
    while True:
        choice = input(f"{MAGENTA}Enter 1 or 2: {RESET}").strip()
        if choice == "1":
            return 10
        if choice == "2":
            return 6
        print(f"{RED}Invalid choice. Please enter 1 or 2.{RESET}")

def generate_code(length: int, min_digit: int, max_digit: int) -> list[str]:
    return [str(random.randint(min_digit, max_digit)) for _ in range(length)]

def grade_guess(secret: list[str], guess: list[str]) -> tuple[int,int]:
    exact = sum(s == g for s, g in zip(secret, guess))
    # prepare leftovers for partial matches
    rem_secret = []
    rem_guess  = []
    for s, g in zip(secret, guess):
        if s != g:
            rem_secret.append(s)
            rem_guess.append(g)
    partial = 0
    for g in rem_guess:
        if g in rem_secret:
            partial += 1
            rem_secret.remove(g)
    return exact, partial

def main() -> None:
    CODE_LEN = 4

    # 1) Player setup
    player      = get_player_name()
    min_d, max_d= choose_range()
    max_tries   = choose_difficulty()

    print_header(player, 0, max_tries)
    print(f"{YELLOW}I’ve chosen a {CODE_LEN}-digit code, digits {min_d}–{max_d}.{RESET}")
    print(f"{YELLOW}You have {max_tries} attempts to crack it!{RESET}")
    input("\nPress ENTER to begin…")

    # 2) Game loop
    secret = generate_code(CODE_LEN, min_d, max_d)
    for attempt in range(1, max_tries + 1):
        print_header(player, attempt, max_tries)

        while True:
            raw = input(f"{CYAN}Attempt {attempt}/{max_tries}, enter {CODE_LEN} digits ({min_d}–{max_d}): {RESET}")
            if len(raw)==CODE_LEN and all(ch.isdigit() for ch in raw) and \
               all(min_d <= int(ch) <= max_d for ch in raw):
                break
            print(f"{RED}Invalid: need {CODE_LEN} digits between {min_d} and {max_d}.{RESET}")

        exact, partial = grade_guess(secret, list(raw))

        if exact == CODE_LEN:
            print_header(player, attempt, max_tries)
            print(f"\n{GREEN}🎉 Cracked in {attempt} {'try' if attempt==1 else 'tries'}! Code was {''.join(secret)}.{RESET}\n")
            break

        # feedback
        print(f"{GREEN}Exact matches   (correct digit & position):{RESET} {exact}")
        print(f"{YELLOW}Partial matches (correct digit, wrong position):{RESET} {partial}\n")
        input("Press ENTER for next round…")
    else:
        # out of attempts
        print_header(player, max_tries, max_tries)
        print(f"\n{RED}Out of attempts! The code was {''.join(secret)}.{RESET}\n")

    input("Press ENTER to return to the main menu…")

if __name__ == "__main__":
    main()
