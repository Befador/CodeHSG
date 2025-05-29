"""
DOCUMENTATION

This script implements a simple terminal-based Roulette game using Pygame for graphics and input handling.
The game allows players to:
- Start with a specified amount of coins.
- Place bets on a number between 0 and 36.
- Spin the roulette wheel to get a random number.
- Win or lose coins based on the bet and the result.
- Play multiple rounds until they choose to exit.

The functions are:
1. draw_window(): Renders the game window with current balance, last result, and messages.
2. get_user_input() : Handles user input for betting and balance management.
3. spin_wheel() : Simulates spinning the roulette wheel and calculates winnings or losses.
4. ask_next_round() : Prompts the player to continue or exit the game.
"""


# imports
import pygame # for game graphics and input handling
import random # for random number generation
import sys

# Initialize Pygame
pygame.init() # Initialize the Pygame library

# Set up display
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Roulette Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (0, 128, 0)

# Set up fonts
FONT = pygame.font.SysFont('arial', 24)
BIG_FONT = pygame.font.SysFont('arial', 36)

# Define roulette numbers and colors
ROULETTE_NUMBERS = list(range(0, 37))
ROULETTE_COLORS = {0: GREEN}
for num in range(1, 37):
    ROULETTE_COLORS[num] = RED if num % 2 == 1 else BLACK

# Game state
balance = 0
bet_amount = 0
bet_number = None
result_number = None
message = ""

# Constants
MIN_BET = 10
PAYOUT = 35


def draw_window():
    win.fill(WHITE)
    # Balance display
    bal_txt = FONT.render(f"Balance: {balance} coins", True, BLACK)
    win.blit(bal_txt, (50, 50))

    # Last result display
    if result_number is not None:
        res_txt = BIG_FONT.render(f"Last Result: {result_number}", True, ROULETTE_COLORS[result_number])
        win.blit(res_txt, (WIDTH // 2 - res_txt.get_width() // 2, HEIGHT // 2 - res_txt.get_height() // 2))

    # Message display
    msg_txt = FONT.render(message, True, RED)
    win.blit(msg_txt, (50, 100))

    pygame.display.flip()


def get_user_input():
    global balance, bet_amount, bet_number

    while balance < MIN_BET:
        print(f"\nYou have only {balance} coins.")
        choice = input("Would you like to buy more coins? (y/n): ").lower()
        if choice == "y":
            try:
                add = int(input("How many coins would you like to purchase? "))
                if add > 0:
                    balance += add
                    print(f"New balance: {balance} coins.")
                else:
                    print("Invalid amount.")
            except ValueError:
                print("Please enter a valid number.")
        else:
            print("Thanks for playing!")
            pygame.quit()
            sys.exit()

    while True:
        try:
            bet_amount = int(input(f"\nEnter your bet amount (min {MIN_BET} coins): "))
            if bet_amount < MIN_BET:
                print(f"The minimum bet is {MIN_BET} coins.")
            elif bet_amount > balance:
                print("You don't have enough coins for that bet.")
            else:
                break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        try:
            bet_number = int(input("Bet on a number (0–36): "))
            if 0 <= bet_number <= 36:
                break
            else:
                print("Choose a number between 0 and 36.")
        except ValueError:
            print("Please enter a valid number.")


def spin_wheel():
    global balance, result_number, message

    result_number = random.choice(ROULETTE_NUMBERS)

    if bet_number == result_number:
        winnings = bet_amount * PAYOUT
        balance += winnings
        message = f"You won! Number: {result_number}, Winnings: {winnings} coins."
    else:
        balance -= bet_amount
        message = f"You lost. Number: {result_number}. You lost {bet_amount} coins."


def ask_next_round():
    while True:
        choice = input("\nPlay again? (y/n): ").lower()
        if choice == "y":
            return True
        elif choice == "n":
            print("Thanks for playing!")
            pygame.quit()
            return False
        else:
            print("Please enter 'y' or 'n'.")


def main():
    global balance

    print("🎰 Welcome to Python Roulette!")
    while True:
        try:
            balance = int(input("How many coins would you like to start with? "))
            if balance >= MIN_BET:
                break
            else:
                print(f"Please start with at least {MIN_BET} coins.")
        except ValueError:
            print("Please enter a valid number.")

    clock = pygame.time.Clock()
    running = True

    while running:
        get_user_input()
        spin_wheel()

        # Run one frame to show result
        draw_window()

        pygame.time.delay(1000)

        print(f"\nYour balance: {balance} coins")
        if not ask_next_round():
            running = False

        clock.tick(30)

    pygame.quit()
    return "exit"


if __name__ == "__main__":
    main()
