

#!/usr/bin/env python3
"""
Terminal Snake – retro‑arcade edition for CodeHSG.

Controls:  ← ↑ ↓ →  (arrow keys)   |   ESC = quit
"""

import curses
import os
import random
import sys
import time
from pathlib import Path

# ── Colour constants (match main menu) ────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"
RED    = "\033[31m"

ASCII_SNAKE = f"""{GREEN}{BOLD}
╔════════════════════════════════════════╗
║         {CYAN}★  S N A K E  ★{GREEN}          ║
╚════════════════════════════════════════╝{RESET}
"""

# ── Game parameters ───────────────────────────────────────────────────────────
BOARD_H = 20
BOARD_W = 40
FRAME_DELAY = 0.09   # seconds between frames

KEY_DIR = {
    curses.KEY_UP:    (-1, 0),
    curses.KEY_DOWN:  ( 1, 0),
    curses.KEY_LEFT:  ( 0,-1),
    curses.KEY_RIGHT: ( 0, 1),
}

# ── Core game loop inside curses wrapper ──────────────────────────────────────
def _game(stdscr: "curses._CursesWindow") -> None:
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    # Initial snake: two cells in middle
    snake = [(BOARD_H // 2, BOARD_W // 2 - 1),
             (BOARD_H // 2, BOARD_W // 2)]
    direction = KEY_DIR[curses.KEY_RIGHT]
    food = _new_food(snake)

    score = 0
    last_key = curses.KEY_RIGHT
    banner_lines = ASCII_SNAKE.splitlines()

    while True:
        # ---- input -----------------------------------------------------------
        try:
            key = stdscr.getch()
        except KeyboardInterrupt:
            break
        if key == 27:                      # ESC
            break
        if key in KEY_DIR and not _is_opposite(KEY_DIR[key], direction):
            direction = KEY_DIR[key]
            last_key = key

        # ---- update snake ----------------------------------------------------
        new_head = (snake[-1][0] + direction[0],
                    snake[-1][1] + direction[1])

        # collision with walls or self
        if (new_head[0] < 0 or new_head[0] >= BOARD_H or
            new_head[1] < 0 or new_head[1] >= BOARD_W or
            new_head in snake):
            _game_over(stdscr, score)
            return

        snake.append(new_head)
        if new_head == food:
            score += 1
            food = _new_food(snake)
        else:
            snake.pop(0)

        # ---- draw frame ------------------------------------------------------
        stdscr.erase()

        # banner
        for idx, line in enumerate(banner_lines):
            stdscr.addstr(idx, 0, line)

        # border
        top = len(banner_lines)
        for x in range(BOARD_W + 2):
            stdscr.addstr(top, x, GREEN + "═" + RESET)
            stdscr.addstr(top + BOARD_H + 1, x, GREEN + "═" + RESET)
        for y in range(1, BOARD_H + 1):
            stdscr.addstr(top + y, 0, GREEN + "║" + RESET)
            stdscr.addstr(top + y, BOARD_W + 1, GREEN + "║" + RESET)

        # food
        fy, fx = food
        stdscr.addstr(top + 1 + fy, 1 + fx, RED + "◆" + RESET)

        # snake
        for y, x in snake[:-1]:
            stdscr.addstr(top + 1 + y, 1 + x, GREEN + "■" + RESET)
        hy, hx = snake[-1]
        stdscr.addstr(top + 1 + hy, 1 + hx, YELLOW + BOLD + "■" + RESET)

        # score line
        stdscr.addstr(top + BOARD_H + 3, 0,
                      f"{CYAN}Score: {score}{RESET}")

        stdscr.refresh()
        time.sleep(FRAME_DELAY)

def _new_food(snake: list[tuple[int,int]]) -> tuple[int,int]:
    """Return a random board cell not occupied by the snake."""
    while True:
        pos = (random.randrange(BOARD_H), random.randrange(BOARD_W))
        if pos not in snake:
            return pos

def _is_opposite(a: tuple[int,int], b: tuple[int,int]) -> bool:
    """Return True if direction vectors `a` and `b` are exact opposites."""
    return a[0] == -b[0] and a[1] == -b[1]

def _game_over(stdscr, score: int) -> None:
    msg = f"{YELLOW}{BOLD}GAME OVER!  Score: {score}{RESET}"
    stdscr.nodelay(False)
    stdscr.clear()
    stdscr.addstr(1, 0, ASCII_SNAKE)
    stdscr.addstr(6, 0, msg)
    stdscr.addstr(8, 0, "Press any key to return to menu...")
    stdscr.refresh()
    stdscr.getch()

# ── Public entrypoint for arcade launcher ─────────────────────────────────────
def main() -> None:
    curses.wrapper(_game)

if __name__ == "__main__":
    main()