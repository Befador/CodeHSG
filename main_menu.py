

"""
DOCUMENTATION

So this script is the main menu for a collection of terminal games, including Tic‑Tac‑Toe, Snake,  (To be finished), and Hangman.

The whole script is designed to be run in a terminal, and it dynamically imports the game modules when the user selects a game.
This enables us to create separate game files while keeping the main menu clean and organized. Furthermore, it allows for easy addition of new games in the future.

The theme we went for is a retro terminal style, reminiscent of classic text-based games, with a focus on simplicity and ease of use.
Also, we found it fun to use ASCII art for the logo and menu items, giving it a nostalgic feel.
"""
# Check if the necessary packages are installed, and install them if not.

import subprocess
import sys

def ensure_package(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Only needed on Windows
if sys.platform.startswith("win"):
    ensure_package("curses")  # actually installs 'windows-curses'


# Import necessary modules
import os 
import time
from pathlib import Path
from typing import Dict, Callable
import importlib
import traceback

# This script auto-installs missing modules (e.g. 'windows-curses' for Windows).

# Set terminal styles for output
RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"

# Define the ASCII-style logo for the main menu
ASCII_LOGO = f"""{GREEN}{BOLD} 
╔═════════════════════════════════════════════════════════╗
║                                                         ║
║   █████╗  ██████╗   ██████╗  █████╗  ██████╗  ███████╗  ║                                               
║  ██╔══██╗ ██╔══██╗ ██╔════╝ ██╔══██╗ ██╔══██╗ ██╔════╝  ║
║  ███████║ ██████╔╝ ██║      ███████║ ██║  ██║ █████╗    ║
║  ██╔══██║ ██╔══██╗ ██║      ██╔══██║ ██║  ██║ ██╔══╝    ║
║  ██║  ██║ ██║  ██║ ╚██████╗ ██║  ██║ ██████╔╝ ███████╗  ║
║  ╚═╝  ╚═╝ ╚═╝  ╚═╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚══════╝  ║
║                                                         ║
║                     {CYAN}CODE @ HSG{RESET}{GREEN}{BOLD}                          ║
╚═════════════════════════════════════════════════════════╝{RESET}
"""


# now the functions that will be used to clear the terminal, pause for a moment, and launch the games
def clear() -> None: # 
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear") 

# This function is used to pause the execution for a specified number of seconds, allowing the user to see transition text before proceeding.
def pause(seconds: float = 1.2) -> None:
    """Sleep a moment so the user sees transition text."""
    time.sleep(seconds)

# This function is a placeholder for launching games that are not yet implemented.
# It clears the screen, prints a message indicating the game is launching, and then shows a "Coming soon!" message.
def _launch_placeholder(game_name: str) -> None:
    """Temporary stub for games not yet wired up."""
    clear()
    print(f"{YELLOW}{BOLD}Launching {game_name} ...{RESET}")
    pause()
    print(f"{CYAN}Coming soon!{RESET}")
    input("\nPress Enter to return to the main menu...") # Wait for user input before returning to the main menu


# ── Tic‑Tac‑Toe launcher ─────────────────────────────────────────────────────
def start_tic_tac_toe() -> None:
    """Import and start Tic‑Tac‑Toe (tic_tac_toe.py)."""
    # Ensure the current script directory is in the module search path
    script_dir = Path(__file__).resolve().parent
    script_path = str(script_dir)
    if script_path in sys.path:
        sys.path.remove(script_path)
    sys.path.insert(0, script_path)

    # Reload the module if already imported
    if "tic_tac_toe" in sys.modules:
        del sys.modules["tic_tac_toe"]
    try:
        ttt_mod = importlib.import_module("tic_tac_toe")
        importlib.reload(ttt_mod)
        # Call the game's main function
        getattr(ttt_mod, "main")()
    except Exception:
        print(f"{YELLOW}Error launching Tic‑Tac‑Toe:{RESET}")
        traceback.print_exc()
        input("\nPress Enter to return to the main menu...")
        return

# ── Snake launcher ────────────────────────────────────────────────────────
def start_snake() -> None:
    """Import and start Snake (snake.py)."""
    # Ensure the current script directory is in the module search path
    script_dir = Path(__file__).resolve().parent
    script_path = str(script_dir)
    if script_path in sys.path:
        sys.path.remove(script_path)
    sys.path.insert(0, script_path)

    # Reload the module if already imported
    if "snake" in sys.modules:
        del sys.modules["snake"]
    try:
        snake_mod = importlib.import_module("snake")
        importlib.reload(snake_mod)
        # Call the game's main function
        getattr(snake_mod, "main")()
    except Exception:
        print(f"{YELLOW}Error launching Snake:{RESET}")
        traceback.print_exc()
        input("\nPress Enter to return to the main menu...")
        return

# ── Hangman launcher ──────────────────────────────────────────────────────────
def start_hangman() -> None:
    """Import and start Hangman (hangman.py)."""
    # Ensure the current script directory is in the module search path
    script_dir = Path(__file__).resolve().parent
    script_path = str(script_dir)
    if script_path in sys.path:
        sys.path.remove(script_path)
    sys.path.insert(0, script_path)

    # Reload the module if already imported
    if "hangman" in sys.modules:
        del sys.modules["hangman"]
    try:
        hangman_mod = importlib.import_module("hangman")
        importlib.reload(hangman_mod)
        # Call the game's main function
        getattr(hangman_mod, "main")()
    except Exception:
        print(f"{YELLOW}Error launching Hangman:{RESET}")
        traceback.print_exc()
        input("\nPress Enter to return to the main menu...")
        return

# ── Rock, Paper, Scissors launcher ──────────────────────────────────────────────────────────
def start_rock_paper_scissors() -> None:
    """Import and start Rock Paper Scissors (rock_paper_scissors.py)."""
    import curses
    # Ensure the current script directory is in the module search path
    script_dir = Path(__file__).resolve().parent
    script_path = str(script_dir)
    if script_path in sys.path:
        sys.path.remove(script_path)
    sys.path.insert(0, script_path)

    # Reload the module if already imported
    if "rock_paper_scissors" in sys.modules:
        del sys.modules["rock_paper_scissors"]
    try:
        rps_mod = importlib.import_module("rock_paper_scissors")
        importlib.reload(rps_mod)
        # Call the game's main function using curses.wrapper
        curses.wrapper(rps_mod.main)
    except Exception:
        print(f"{YELLOW}Error launching Rock Paper Scissors:{RESET}")
        traceback.print_exc()
        input("\nPress Enter to return to the main menu...")
        return

def start_mastermind() -> None:
    """Import and start Mastermind (mastermind.py)."""
    # Clear the menu before launching the game
    clear()
    # Ensure the current script directory is in the module search path
    script_dir = Path(__file__).resolve().parent
    script_path = str(script_dir)
    if script_path in sys.path:
        sys.path.remove(script_path)
    sys.path.insert(0, script_path)

    # Reload the module if already imported
    if "mastermind" in sys.modules:
        del sys.modules["mastermind"]
    try:
        mastermind_mod = importlib.import_module("mastermind")
        importlib.reload(mastermind_mod)
        # Call the game's main function
        getattr(mastermind_mod, "main")()
    except Exception:
        print(f"{YELLOW}Error launching Mastermind:{RESET}")
        traceback.print_exc()
        input("\nPress Enter to return to the main menu…")
        return
    # Clear the screen again after the user exits the game
    clear()

# ── Menu configuration ────────────────────────────────────────────────────────
 # Mapping of menu item names to their corresponding launcher functions
MENU_ITEMS: Dict[str, Callable[[], None]] = {
    "Tic‑Tac‑Toe": start_tic_tac_toe,
    "Snake":       start_snake,
    "Hangman":     start_hangman,
    "Rock Paper Scissors": start_rock_paper_scissors,
    "Mastermind":           start_mastermind,
}

# ── Core drawing & loop ────────────────────────────────────────────────────────
def draw_menu() -> None:
    """
    Clear the screen and display the ASCII logo followed by the numbered game menu items.

    This function clears the terminal, prints the ASCII art logo, and then lists all available
    games with their corresponding menu numbers. The menu items alternate colors for better
    readability. An option to exit (0) is also provided.
    """
    clear()
    print(ASCII_LOGO)
    for idx, title in enumerate(MENU_ITEMS, 1):
        color = CYAN if idx % 2 else GREEN
        print(f"   {color}{idx}. {title}{RESET}")
    print(f"   0. Exit\n")

def main() -> None:
    """
    Main application loop: draw the menu, process user input to launch games or exit.

    This function repeatedly displays the menu, prompts the user for input, and launches
    the selected game. If the user enters 0, the program exits gracefully. Invalid input
    is ignored and the menu is redrawn.
    """
    while True:
        draw_menu()
        choice = input(BOLD + "Select a game (0‑{}): ".format(len(MENU_ITEMS)) + RESET)
        if not choice.isdigit():
            continue
        idx = int(choice)
        if idx == 0:
            clear()
            print(YELLOW + BOLD + "See you next time! 👋" + RESET)
            pause(0.8)
            break
        if 1 <= idx <= len(MENU_ITEMS):
            list(MENU_ITEMS.values())[idx-1]()

if __name__ == "__main__": 
    # This ensures the main function is called only when the script is run directly, not when imported.
    main()