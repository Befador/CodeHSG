#!/usr/bin/env python3
"""
Retro‑arcade style main menu for CodeHSG games collection.
Feel free to customise colours, ASCII logo, and menu items.
"""

import os
import sys
import time
from pathlib import Path
from typing import Dict, Callable
import importlib
import traceback

# ── ANSI escape sequences for style ────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"

ASCII_LOGO = f"""{GREEN}{BOLD}
╔═════════════════════════════════════════════════════════╗
║                                                         ║
║   ██████╗  █████╗ ██████╗  █████╗  ██████╗ ███████╗     ║
║   ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔════╝     ║
║   ██████╔╝███████║██████╔╝███████║██║  ██╗ █████╗       ║
║   ██╔══██╗██╔══██║██╔══██╗██╔══██║██║  ╚██╗██╔══╝       ║
║   ██████╔╝██║  ██║██║  ██║██║  ██║╚██████╔╝███████╗     ║
║   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝     ║
║                                                         ║
║              {CYAN}A R C A D E   C L A S S I C S{RESET}{GREEN}{BOLD}              ║
╚═════════════════════════════════════════════════════════╝{RESET}
"""

# ── Utility functions ──────────────────────────────────────────────────────────
def clear() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")

def pause(seconds: float = 1.2) -> None:
    """Sleep a moment so the user sees transition text."""
    time.sleep(seconds)

def _launch_placeholder(game_name: str) -> None:
    """Temporary stub for games not yet wired up."""
    clear()
    print(f"{YELLOW}{BOLD}Launching {game_name} ...{RESET}")
    pause()
    print(f"{CYAN}Coming soon!{RESET}")
    input("\nPress Enter to return to the main menu...")

def start_tic_tac_toe() -> None:
    """Import and start Tic‑Tac‑Toe. Tries several common entrypoints before falling back to a placeholder."""
    script_dir = Path(__file__).resolve().parent
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

# ── Menu configuration ────────────────────────────────────────────────────────
MENU_ITEMS: Dict[str, Callable[[], None]] = {
    "Tic‑Tac‑Toe": start_tic_tac_toe,
    "Snake":       start_snake,
    "Minesweeper": lambda: _launch_placeholder("Minesweeper"),
    "Hangman":     start_hangman,
}

# ── Core drawing & loop ────────────────────────────────────────────────────────
def draw_menu() -> None:
    clear()
    print(ASCII_LOGO)
    for idx, title in enumerate(MENU_ITEMS, 1):
        color = CYAN if idx % 2 else GREEN
        print(f"   {color}{idx}. {title}{RESET}")
    print(f"   0. Exit\n")

def main() -> None:
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
    main()