
"""
DOCUMENTATION

So this script is the main menu for a collection of terminal games, including Tic‑Tac‑Toe, Snake, Minesweeper (To be finished), and Hangman.

The whole script is designed to be run in a terminal, and it dynamically imports the game modules when the user selects a game.
This enables us to create separate game files while keeping the main menu clean and organized. Furthermore, it allows for easy addition of new games in the future.

The theme we went for is a retro terminal style, reminiscent of classic text-based games, with a focus on simplicity and ease of use.
Also, we found it fun to use ASCII art for the logo and menu items, giving it a nostalgic feel.
"""

# Import necessary modules
import os 
import sys
import time
from pathlib import Path
from typing import Dict, Callable
import importlib
import traceback

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
    """Import and start Tic‑Tac‑Toe. Tries several common entrypoints before falling back to a placeholder."""
    script_dir = Path(__file__).resolve().parent # Get the directory of the current script. 
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))

    try:
        ttt = importlib.import_module("tic_tac_toe") 
    except ModuleNotFoundError:
        _launch_placeholder("Tic‑Tac‑Toe (module not found)")
        return

    # Try a sequence of likely entry‑points.
    for attr in ("main", "game_loop", "play"):
        if hasattr(ttt, attr):
            try:
                getattr(ttt, attr)()
                return  # Success!
            except Exception as exc:  # pragma: no cover
                print(f"{YELLOW}Error while running {attr}(): {exc}{RESET}")
                break

    _launch_placeholder("Tic‑Tac‑Toe (no usable entrypoint)") 

# ── Snake launcher ────────────────────────────────────────────────────────
def start_snake() -> None:
    """Import and start Snake (snake.py)."""
    script_dir = Path(__file__).resolve().parent
    script_path = str(script_dir)
    # Ensure project directory is first in search path
    if script_path in sys.path:
        sys.path.remove(script_path)
    sys.path.insert(0, script_path)

    # Hot‑reload so edits are picked up without restarting the menu
    if "snake" in sys.modules:
        del sys.modules["snake"]
    try:
        snake_mod = importlib.import_module("snake")
        importlib.reload(snake_mod)
        getattr(snake_mod, "main")()
    except Exception:
        print(f"{YELLOW}Error launching Snake:{RESET}")
        traceback.print_exc()
        input("\nPress Enter to return to the main menu...")
        return

# ── Hangman launcher ──────────────────────────────────────────────────────────
def start_hangman() -> None:
    """Import and start Hangman (hangman.py)."""
    script_dir = Path(__file__).resolve().parent
    script_path = str(script_dir)
    if script_path in sys.path:
        sys.path.remove(script_path)
    sys.path.insert(0, script_path)

    if "hangman" in sys.modules:
        del sys.modules["hangman"]
    try:
        hangman_mod = importlib.import_module("hangman")
        importlib.reload(hangman_mod)
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
    script_dir = Path(__file__).resolve().parent
    script_path = str(script_dir)
    if script_path in sys.path:
        sys.path.remove(script_path)
    sys.path.insert(0, script_path)

    if "rock_paper_scissors" in sys.modules:
        del sys.modules["rock_paper_scissors"]
    try:
        rps_mod = importlib.import_module("rock_paper_scissors")
        importlib.reload(rps_mod)
        # Instead of calling main() directly, use curses.wrapper to run it properly
        curses.wrapper(rps_mod.main)
    except Exception:
        print(f"{YELLOW}Error launching Rock Paper Scissors:{RESET}")
        traceback.print_exc()
        input("\nPress Enter to return to the main menu...")
        return

# ── Menu configuration ────────────────────────────────────────────────────────
 # Mapping of menu item names to their corresponding launcher functions
MENU_ITEMS: Dict[str, Callable[[], None]] = {
    "Tic‑Tac‑Toe": start_tic_tac_toe,
    "Snake":       start_snake,
    "Minesweeper": lambda: _launch_placeholder("Minesweeper"),
    "Hangman":     start_hangman,
    "Rock Paper Scissors": start_rock_paper_scissors,
}

# ── Core drawing & loop ────────────────────────────────────────────────────────
def draw_menu() -> None:
    """
    Clear the screen and display the ASCII logo followed by the numbered game menu items.
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

if __name__ == "__main__": # This ensures the main function is called only when the script is run directly, not when imported.
    main()