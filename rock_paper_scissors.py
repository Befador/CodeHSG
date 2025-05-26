import random
import time
import os

# For colored text in terminal (works in many terminals)
try:
    from colorama import Fore, Style, init
    init()
except ImportError:
    # colorama is optional, fallback if not installed
    class Dummy:
        def __getattr__(self, name): return ''
    Fore = Style = Dummy()

ASCII_ART = {
    "rock": """
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
""",
    "paper": """
     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
""",
    "scissors": """
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
"""
}

choices = ["rock", "paper", "scissors"]

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def countdown():
    for i in range(3, 0, -1):
        print(f"{Fore.YELLOW}{i}...{Style.RESET_ALL}")
        time.sleep(1)
        clear()

def get_user_choice():
    while True:
        choice = input("Choose Rock, Paper, or Scissors (r/p/s): ").lower()
        if choice in ['r', 'p', 's']:
            return {'r': 'rock', 'p': 'paper', 's': 'scissors'}[choice]
        print("Invalid choice, try again.")

def print_choices(user, comp):
    print(f"\nYou chose: {Fore.CYAN}{user}{Style.RESET_ALL}")
    print(ASCII_ART[user])
    print(f"Computer chose: {Fore.MAGENTA}{comp}{Style.RESET_ALL}")
    print(ASCII_ART[comp])

def decide_winner(user, comp):
    if user == comp:
        return "tie"
    wins = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}
    if wins[user] == comp:
        return "user"
    else:
        return "computer"

def main():
    user_score, comp_score = 0, 0
    rounds = 5

    clear()
    print(f"{Fore.GREEN}Welcome to Rock Paper Scissors! Best of {rounds} rounds.{Style.RESET_ALL}\n")

    for round_number in range(1, rounds + 1):
        print(f"{Fore.YELLOW}Round {round_number}{Style.RESET_ALL}")
        user_choice = get_user_choice()
        clear()
        print("Get ready...")
        countdown()
        comp_choice = random.choice(choices)
        print_choices(user_choice, comp_choice)

        winner = decide_winner(user_choice, comp_choice)
        if winner == "user":
            print(f"{Fore.GREEN}You win this round!{Style.RESET_ALL}")
            user_score += 1
        elif winner == "computer":
            print(f"{Fore.RED}Computer wins this round!{Style.RESET_ALL}")
            comp_score += 1
        else:
            print(f"{Fore.BLUE}It's a tie!{Style.RESET_ALL}")

        print(f"\nScore: You {user_score} - Computer {comp_score}\n")
        input("Press Enter to continue...")
        clear()

    print(f"{Fore.CYAN}Final Score: You {user_score} - Computer {comp_score}{Style.RESET_ALL}")
    if user_score > comp_score:
        print(f"{Fore.GREEN}Congratulations! You won the game!{Style.RESET_ALL}")
    elif comp_score > user_score:
        print(f"{Fore.RED}Sorry, the computer won the game.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}It's a tie game!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()