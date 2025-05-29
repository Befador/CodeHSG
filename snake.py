#!/usr/bin/env python3
"""
Terminal Snake – retro‑arcade edition for CodeHSG.

Controls are  ← ↑ ↓ →  (arrow keys)   |   ESC = quit (the keyboard)
The game is played in a terminal window, where the player controls a snake
using the arrow keys, trying to eat food (represented by a 2×2 square of '*')
without hitting the walls (if solid) or biting its own tail.
Speed increases with each food item eaten, making the game progressively harder.
The game features a main menu with options to start the game and choose whether
walls are solid or wrapped (teleporting).

This script uses the curses module to handle terminal input and output.
The game consists of several functions:

These functions are 
1. _start_screen: displays the game banner and instructions, waits for SPACE or ENTER to start.
2. _ask_walls: asks whether walls are solid or wrapped, returns True/False.
3. _game: main game loop, handles snake movement, food generation, and collision detection.
4. _new_food: generates a new food position not occupied by the snake.
5. _is_opposite: checks if two direction vectors are opposite.
6. _game_over: displays the game over screen with the final score and asks if the player wants to play again.


"""

# This is a terminal-based Snake game written with the curses module.
# The player controls a snake using arrow keys, trying to eat food
# (represented by a 2×2 square of '*') without hitting the walls (if solid)
# or biting its own tail. Speed increases with each food item eaten.

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

ASCII_SNAKE = [
    "╔════════════════════════════════════════╗",
    "║              S  N  A  K  E             ║",
    "╚════════════════════════════════════════╝",
]

def _start_screen(stdscr) -> bool:
    """
    Show the banner and instructions.
    Return False if the user presses ESC, True otherwise.
    Only handles the 'Press SPACE/Enter' logic.
    """
    stdscr.nodelay(False)
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    # Center the banner
    for i, line in enumerate(ASCII_SNAKE):
        stdscr.addstr(i + 2, (w - len(line)) // 2, line, curses.A_BOLD)

    # Display the core instructions and wait for the player to press SPACE or ENTER.
    info = [
        "Controls: Arrow keys   |   ESC to quit",
        "Eat the '*' food and avoid walls or yourself.",
        "",
        "Press SPACE or ENTER to start…"
    ]
    for j, txt in enumerate(info, len(ASCII_SNAKE) + 4):
        stdscr.addstr(j + 2, (w - len(txt)) // 2, txt)

    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key in (27,):                 # ESC
            return False
        if key in (curses.KEY_ENTER, 10, 13, ord(' ')):
            stdscr.nodelay(True)
            return True

# --- Dedicated walls question window ---
def _ask_walls(stdscr) -> bool:
    """
    Separate screen asking whether walls are solid.
    Returns True if the player answers 'y', otherwise False.
    ESC also returns False.
    """
    stdscr.clear()
    stdscr.nodelay(False)
    h, w = stdscr.getmaxyx()

    # Re‑draw banner centred
    for i, line in enumerate(ASCII_SNAKE):
        stdscr.addstr(i + 2, (w - len(line)) // 2, line, curses.A_BOLD)

    # Ask the user whether walls should be solid or wrapped (teleporting).
    prompt = "Walls solid? y/n (default n): "
    stdscr.addstr(len(ASCII_SNAKE) + 5,
                  (w - len(prompt)) // 2,
                  prompt,
                  curses.color_pair(5) | curses.A_BOLD)
    stdscr.refresh()

    while True:
        ch = stdscr.getch()
        if ch in (27, curses.KEY_EXIT):  # ESC closes, treat as 'n'
            return False
        if ch in (ord('y'), ord('Y')):
            return True
        if ch in (ord('n'), ord('N'), 10, 13):
            return False

# ── Game parameters ───────────────────────────────────────────────────────────
BOARD_H = 20
BOARD_W = 40
# Dynamic speed parameters
BASE_DELAY  = 0.15   # starting delay (seconds)
SPEEDUP     = 0.005  # amount to subtract per food eaten
MIN_DELAY   = 0.05   # lower cap – game never gets faster than this

# Maps each arrow key to a direction vector (dy, dx).
KEY_DIR = {
    curses.KEY_UP:    (-1, 0),
    curses.KEY_DOWN:  ( 1, 0),
    curses.KEY_LEFT:  ( 0,-1),
    curses.KEY_RIGHT: ( 0, 1),
}

PLAY_AGAIN = False  # set in _game_over() and read by main()

# ── Core game loop inside curses wrapper ──────────────────────────────────────
def _game(stdscr: "curses._CursesWindow") -> None:
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN,  -1)   # snake body
    curses.init_pair(2, curses.COLOR_YELLOW, -1)   # snake head
    curses.init_pair(3, curses.COLOR_CYAN,   -1)   # walls / banner
    curses.init_pair(4, curses.COLOR_RED,    -1)   # food
    curses.init_pair(5, curses.COLOR_WHITE,  -1)   # score text

    if not _start_screen(stdscr):
        return
    walls_solid = _ask_walls(stdscr)
    stdscr.nodelay(True)   # resume non‑blocking input for the gameplay loop

    # Set up initial game state.
    # Initial snake: two cells in middle
    snake = [(BOARD_H // 2, BOARD_W // 2 - 1),
             (BOARD_H // 2, BOARD_W // 2)]
    direction = KEY_DIR[curses.KEY_RIGHT]
    food = _new_food(snake)

    score = 0
    last_key = curses.KEY_RIGHT
    banner_lines = ASCII_SNAKE
    frame_delay = BASE_DELAY


    max_y, max_x = stdscr.getmaxyx()
    top = len(banner_lines)
    need_y = top + BOARD_H + 4          # banner + board + footer lines
    need_x = BOARD_W + 2                # board width incl. borders
    if max_y < need_y or max_x < need_x:
        stdscr.nodelay(False)
        stdscr.clear()
        stdscr.addstr(0, 0, f"{YELLOW}{BOLD}Terminal window too small!{RESET}")
        stdscr.addstr(2, 0, f"Need at least {need_x}×{need_y} characters.")
        stdscr.addstr(3, 0, f"Detected {max_x}×{max_y}.")
        stdscr.addstr(5, 0, "Resize the window and try again.")
        stdscr.addstr(7, 0, "Press any key to return to menu...")
        stdscr.refresh()
        stdscr.getch()
        return

    while True:
        # Handle user input: arrow keys and ESC.
        try:
            key = stdscr.getch()
        except KeyboardInterrupt:
            break
        if key == 27:                      # ESC
            break
        if key in KEY_DIR and not _is_opposite(KEY_DIR[key], direction):
            direction = KEY_DIR[key]
            last_key = key

        # Determine the snake's next head position, with wrap-around if enabled.
        if walls_solid:
            ny = snake[-1][0] + direction[0]
            nx = snake[-1][1] + direction[1]
        else:
            ny = (snake[-1][0] + direction[0]) % BOARD_H
            nx = (snake[-1][1] + direction[1]) % BOARD_W
        new_head = (ny, nx)

        # The current food item occupies a 2x2 block.
        food_cells = [(food[0], food[1]), (food[0]+1, food[1]), (food[0], food[1]+1), (food[0]+1, food[1]+1)]

        # Check if the snake hits itself or (if solid) a wall.
        if walls_solid and (ny < 0 or ny >= BOARD_H or nx < 0 or nx >= BOARD_W):
            _game_over(stdscr, score)
            return
        if new_head in snake:
            _game_over(stdscr, score)
            return

        # Add new head; check if food is eaten, update score and delay.
        snake.append(new_head)
        if new_head in food_cells:
            score += 1
            food = _new_food(snake)
            frame_delay = max(MIN_DELAY, frame_delay - SPEEDUP)
        else:
            snake.pop(0)

        # Render the game board and elements to the terminal.
        stdscr.erase()

        left = (max_x - (BOARD_W + 2)) // 2

        # banner
        for idx, line in enumerate(ASCII_SNAKE):
            stdscr.addstr(idx, left + (BOARD_W + 2 - len(line)) // 2,
                          line, curses.color_pair(3) | curses.A_BOLD)

        # border
        top = len(ASCII_SNAKE)
        wall_attr = curses.color_pair(3)
        for x in range(BOARD_W + 2):
            stdscr.addch(top, left + x, '#', wall_attr)
            stdscr.addch(top + BOARD_H + 1, left + x, '#', wall_attr)
        for y in range(1, BOARD_H + 1):
            stdscr.addch(top + y, left, '#', wall_attr)
            stdscr.addch(top + y, left + BOARD_W + 1, '#', wall_attr)

        # food
        fy, fx = food
        food_cells = [(fy, fx), (fy+1, fx), (fy, fx+1), (fy+1, fx+1)]
        for cy, cx in food_cells:
            stdscr.addch(top + 1 + cy, left + 1 + cx, '*', curses.color_pair(4))

        # snake
        for y, x in snake[:-1]:
            stdscr.addch(top + 1 + y, left + 1 + x, 'O', curses.color_pair(1))
        hy, hx = snake[-1]
        stdscr.addch(top + 1 + hy, left + 1 + hx, '@', curses.color_pair(2) | curses.A_BOLD)

        # score line
        stdscr.addstr(top + BOARD_H + 3, left,
                      f"Score: {score}", curses.color_pair(5) | curses.A_BOLD)

        stdscr.refresh()
        time.sleep(frame_delay)

def _new_food(snake: list[tuple[int,int]]) -> tuple[int,int]:
    """Return a random board cell not occupied by the snake."""
    # Randomly find a 2x2 area not occupied by the snake.
    while True:
        y = random.randrange(BOARD_H - 1)
        x = random.randrange(BOARD_W - 1)
        square = [(y, x), (y+1, x), (y, x+1), (y+1, x+1)]
        if all(cell not in snake for cell in square):
            return (y, x)

def _is_opposite(a: tuple[int,int], b: tuple[int,int]) -> bool:
    """True if direction `a` is the exact opposite of `b`."""
    return a[0] == -b[0] and a[1] == -b[1]

def _game_over(stdscr, score: int) -> None:
    # Show final score and ask player whether to restart.
    msg = f"GAME OVER!  Score: {score}"
    banner_attr = curses.color_pair(3) | curses.A_BOLD
    stdscr.nodelay(False)
    stdscr.clear()
    for i, line in enumerate(ASCII_SNAKE):
        stdscr.addstr(i + 1, 0, line, banner_attr)
    stdscr.addstr(6, 0, msg, curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(8, 0, "Press any key to return to menu…", curses.color_pair(5))
    stdscr.refresh()
    stdscr.addstr(10, 0, "Play again? (y/n): ", curses.color_pair(5))
    while True:
        ch = stdscr.getch()
        if ch in (ord('y'), ord('Y'), ord('n'), ord('N')):
            break
    global PLAY_AGAIN
    PLAY_AGAIN = ch in (ord('y'), ord('Y'))

# ── Public entrypoint for arcade launcher ─────────────────────────────────────
def main() -> None:
    # Run the game in a loop, restarting if the player chooses to play again.
    global PLAY_AGAIN
    while True:
        PLAY_AGAIN = False
        curses.wrapper(_game)
        if not PLAY_AGAIN:
            break

if __name__ == "__main__":
    main()