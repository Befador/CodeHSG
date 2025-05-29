#!/usr/bin/env python3
"""
DOCUMENTATION:

The idea is to implement a simple terminal-based Blackjack game
with a focus on user experience, strategy, and AI opponents.
This script provides a playable Blackjack game with the following features:
- ASCII art for cards and hands following the style of the other games. 
- Strategy matrices for optimal moves based on player and dealer hands. More specifically,
i used one of the main standard strategy matrices for Blackjack taken from 
https://derrickroselight.medium.com/python-blackjack-simulator-martingale-with-classic-strategy-5b9a2fb06187
- AI players that use the same strategy matrices to make decisions.
This enables the player to learn the previous cards that have been played and adapt its
strategy accordingly.

The game includes both the American and European variants of Blackjack,
with the following rules:
American (us):
- Dealer hits on soft 17.

European (eu):
- Dealer stands on soft 17.
- No hole card until player stands.
- Player can double down on any two cards.
- Player can split pairs, with specific rules for Aces.
- Player can double down after splitting.

The player can choose between both variants at the start of the game.

The functions are the following:
1. clear(): Clears the terminal screen.
2. check_escape_key(): Non-blocking check for ESC key press.
3. draw_card(card): Returns ASCII art lines for a single card.
4. draw_hand(hand, hide_first=False): Prints ASCII art for a hand of cards, optionally hiding the first card.
5. hand_value(hand): Calculates the blackjack value of a hand, accounting for Aces.
6. get_strategy_action(player_hand, dealer_upcard): Determines the optimal move using strategy matrices.
7. play_blackjack(variant, cash, num_ai, player_seat): Main game loop for playing Blackjack with AI players.
8. animate_card_flip(times=1, delay=0.1): Animates a card flipping in the menu corner.
9. animate_ai_turn(duration=0.5): Spinner animation for AI thinking.
10. main(): Main entry point for the Blackjack game, handling menu and user input.



"""


import random 
import sys
import termios
import tty
import select
import os
import time
import shutil
from colorama import init, Fore, Style
init(autoreset=True)

# Global player balance
balance = 0.0

def clear():
    os.system('cls' if os.name == 'nt' else 'clear') # as for the other games, this function clears the terminal screen

def check_escape_key(): # i m still using this function to check for the escape key press
    """
    Non-blocking check for ESC key press.
    Returns True if ESC (^[) is pressed, False otherwise.
    """
    dr, _, _ = select.select([sys.stdin], [], [], 0)
    if dr:
        old = termios.tcgetattr(sys.stdin)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ord(ch) == 27:
                return True
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old)
    return False

# ── Blackjack Strategy Matrices ───────────────────────────────────────────────

# This part is replicated from the website above. I know there are some alternatives
# that exist, in Wikipedia for example, but i wanted to use the one from the website above.

# Dealer upcards in order
UPCARDS = ['2','3','4','5','6','7','8','9','T','A'] 

# Hard totals strategy 
HARD_STRAT = {
    5: dict.fromkeys(UPCARDS, 'H'),
    6: dict.fromkeys(UPCARDS, 'H'),
    7: dict.fromkeys(UPCARDS, 'H'),
    8: dict.fromkeys(UPCARDS, 'H'),
    9: {**dict.fromkeys(UPCARDS, 'H'),
        **{u: 'Dh' for u in ['3','4','5','6']}},
    10:{u: 'Dh' for u in UPCARDS if u not in ['T','A']},
    11:{u: 'Dh' for u in UPCARDS},
    12:{**dict.fromkeys(UPCARDS, 'H'),
        **{u: 'S' for u in ['4','5','6']}},
    13:{u: ('S' if u in ['2','3','4','5','6'] else 'H') for u in UPCARDS},
    14:{u: ('S' if u in ['2','3','4','5','6'] else 'H') for u in UPCARDS},
    15:{u: ('S' if u in ['2','3','4','5','6'] else 'H') for u in UPCARDS},
    16:{u: ('S' if u in ['2','3','4','5','6'] else 'H') for u in UPCARDS},
    17:dict.fromkeys(UPCARDS, 'S'),
    18:dict.fromkeys(UPCARDS, 'S'),
    19:dict.fromkeys(UPCARDS, 'S'),
    20:dict.fromkeys(UPCARDS, 'S'),
}

# Soft totals strategy (total = Ace + card value)
SOFT_STRAT = {
    13:{u: ('Dh' if u in ['5','6'] else 'H') for u in UPCARDS},
    14:{u: ('Dh' if u in ['4','5','6'] else 'H') for u in UPCARDS},
    15:{u: ('Dh' if u in ['4','5','6'] else 'H') for u in UPCARDS},
    16:{u: ('Dh' if u in ['4','5','6'] else 'H') for u in UPCARDS},
    17:{u: ('Dh' if u in ['3','4','5','6'] else ('S' if u in ['2','7','8'] else 'H')) for u in UPCARDS},
    18:{u: ('Ds' if u in ['3','4','5','6'] else ('S' if u in ['2','7','8'] else 'H')) for u in UPCARDS},
    19:dict.fromkeys(UPCARDS, 'S'),
    20:dict.fromkeys(UPCARDS, 'S'),
}

# Pair splitting strategy
PAIR_STRAT = {
    'A': dict.fromkeys(UPCARDS, 'P'),
    'T': dict.fromkeys(UPCARDS, 'S'),
    '9': {u: ('P' if u in ['2','3','4','5','6','8','9'] else 'S') for u in UPCARDS},
    '8': dict.fromkeys(UPCARDS, 'P'),
    '7': {u: ('P' if u in ['2','3','4','5','6','7'] else 'H') for u in UPCARDS},
    '6': {u: ('P' if u in ['2','3','4','5','6'] else 'H') for u in UPCARDS},
    '5': {u: ('Dh' if u in ['2','3','4','5','6','7','8','9'] else 'H') for u in UPCARDS},
    '4': {u: ('P' if u in ['5','6'] else 'H') for u in UPCARDS},
    '3': {u: ('P' if u in ['2','3','4','5','6','7'] else 'H') for u in UPCARDS},
    '2': {u: ('P' if u in ['2','3','4','5','6','7'] else 'H') for u in UPCARDS},
}





# - ASCII art dimensions  ────────────────────────────────────────────────────────────
CARD_WIDTH = 9
CARD_HEIGHT = 5

def draw_card(card): # this is quite standard...
    """Return ASCII art lines for a single card."""
    rank, suit = card
    # Top border
    lines = ['┌' + '─' * (CARD_WIDTH - 2) + '┐']
    # Rank top-left
    r = rank if len(rank) == 2 else rank + ' '
    lines.append(f"│{r}{' ' * (CARD_WIDTH - 2 - len(r))}│")
    # Suit centered
    lines.append(f"│{' ' * ((CARD_WIDTH - 2 - 1) // 2)}{suit}{' ' * ((CARD_WIDTH - 2 - 1) // 2)}│")
    # Rank bottom-right
    r = rank if len(rank) == 2 else ' ' + rank
    lines.append(f"│{' ' * (CARD_WIDTH - 2 - len(r))}{r}│")
    # Bottom border
    lines.append('└' + '─' * (CARD_WIDTH - 2) + '┘')
    return lines

# ── UI Animations ────────────────────────────────────────────────────────────
# ASCII card back for flip animation
CARD_BACK = [
    '┌' + '─' * (CARD_WIDTH - 2) + '┐',
    '│' + '░' * (CARD_WIDTH - 2) + '│',
    '│' + '░' * (CARD_WIDTH - 2) + '│',
    '│' + '░' * (CARD_WIDTH - 2) + '│',
    '└' + '─' * (CARD_WIDTH - 2) + '┘'
]

FACE_CARD = draw_card(('A', '♠')) 

def animate_card_flip(times: int = 1, delay: float = 0.1): # my attempt to animate the card flipping
    """Animate a card flipping in the menu corner."""
    width, _ = shutil.get_terminal_size()
    indent = ' ' * (width - CARD_WIDTH)
    for _ in range(times):
        for frame in (CARD_BACK, FACE_CARD):
            clear()
            for line in frame:
                print(indent + line)
            time.sleep(delay)
    clear()

def animate_ai_turn(duration: float = 0.5): # at least this works...
    """Spinner animation for AI thinking."""
    spinner = ['|', '/', '-', '\\'] # the system goes through these characters.
    end_time = time.time() + duration
    while time.time() < end_time: # i use a while loop to keep the spinner going
        for ch in spinner:
            sys.stdout.write(f"\rAI thinking... {ch}")
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write("\r" + " " * 20 + "\r")


# Card definitions
SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['A'] + [str(n) for n in range(2, 11)] + ['J', 'Q', 'K'] # standard ranks for a card game

# ── Card Drawing and Hand Management ────────────────────────────────────────────
def draw_hand(hand, hide_first=False):
    """Print ASCII art for a hand of cards; can hide the dealer's first card."""
    lines = [''] * CARD_HEIGHT
    for idx, card in enumerate(hand):
        if idx == 0 and hide_first:
            # Face-down card
            blank = [
                '┌' + '─' * (CARD_WIDTH - 2) + '┐',
                '│' + ' ' * (CARD_WIDTH - 2) + '│',
                '│' + ' ' * (CARD_WIDTH - 2) + '│',
                '│' + ' ' * (CARD_WIDTH - 2) + '│',
                '└' + '─' * (CARD_WIDTH - 2) + '┘'
            ]
            art = blank
        else:
            art = draw_card(card)
        for i in range(CARD_HEIGHT):
            lines[i] += art[i] + ' '
    print('\n'.join(lines))

def hand_value(hand):
    """Calculate the blackjack value of a hand, accounting for Aces."""
    total = 0
    aces = 0
    for rank, _ in hand:
        if rank in ['J', 'Q', 'K']:
            total += 10
        elif rank == 'A': # Aces can be 1 or 11. This is an important feature of the game.
            aces += 1
            total += 11
        else:
            total += int(rank)
    # Adjust for Aces if total > 21
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def is_soft_17(hand):
    """
    Return True if hand is a soft 17 (contains an Ace counted as 11 and total==17).
    """
    raw_total = sum(11 if r == 'A' else 10 if r in ['J','Q','K'] else int(r) for r, _ in hand)
    return raw_total == 17 and hand_value(hand) == 17

def get_strategy_action(player_hand, dealer_upcard):
    """
    Determine optimal move using the strategy matrices.
    Returns 'H', 'S', 'Dh', 'Ds', or 'P'.
    """
    up = dealer_upcard[0]
    # Normalize dealer upcard ten
    up = 'T' if up in ['10','T','J','Q','K'] else up # standardize the dealer's upcard
    # Check for pair
    if len(player_hand) == 2 and player_hand[0][0] == player_hand[1][0]: # this is the case of a pair
        rank = player_hand[0][0]
        return PAIR_STRAT.get(rank, HARD_STRAT[hand_value(player_hand)]).get(up, 'H')
    # Check for soft
    total = hand_value(player_hand)
    has_ace = any(r == 'A' for r, _ in player_hand)
    if has_ace and total <= 20:
        return SOFT_STRAT.get(total, HARD_STRAT.get(total, {})).get(up, 'H')
    # Hard total
    return HARD_STRAT.get(total, {}).get(up, 'H') # this is the case of a hard total, i.e. no Aces in the hand or Aces counted as 1

def play_blackjack(variant: str, cash: float, num_ai: int, player_seat: int):
    """Play one full game of Blackjack with AI players."""
    clear()
    print(Fore.GREEN + "-" * 60)
    print(Fore.YELLOW + Style.BRIGHT + f"Starting Blackjack ({variant.upper()})".center(60))
    print(Fore.GREEN + "-" * 60)
    global balance # set the global balance variable to the cash amount
    while True:
        if check_escape_key():
            return "exit"
        # Prompt for bet
        while True:
            if check_escape_key():
                return "exit"
            clear()
            print(Fore.CYAN + f"Current Balance: ${balance:.2f}") # display the current balance
            try:
                bet = float(input("Enter your bet amount: ")) # prompt the user for a bet amount
                if bet <= 0 or bet > balance:
                    print("Invalid bet. Must be >0 and ≤ balance.")
                    time.sleep(1)
                    continue
            except ValueError: # handle the case where the user enters a non-numeric value
                print("Enter a numeric value.")
                time.sleep(1)
                continue
            balance -= bet # deduct the bet from the balance
            break

        # Build and shuffle multi-deck shoe
        deck = [(rank, suit) for rank in RANKS for suit in SUITS] * 6
        random.shuffle(deck)

        # Prepare hands in seating order: AI players, human, dealer last
        hands = []
        for i in range(num_ai):
            hands.append([deck.pop(), deck.pop()])  # AI hand
        human_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]

        # Initial reveal of AI and dealer hands to player
        clear()
        print(Fore.MAGENTA + "Initial deal:")
        for idx, ai_hand in enumerate(hands):
            print(Fore.CYAN + f"AI Player {idx+1} hand:")
            draw_hand(ai_hand)
        print(Fore.CYAN + "Dealer upcard:")
        draw_hand([dealer_hand[1]])
        print(Fore.CYAN + "Your hand:")
        draw_hand(human_hand)
        input("Press Enter to continue...")

        print("Welcome to Terminal Blackjack!")

        # AI players take their turns
        for idx, ai_hand in enumerate(hands):
            print(f"\nAI Player {idx+1} (seat {idx+1}) is playing...")
            while True:
                action = get_strategy_action(ai_hand, dealer_hand[1])
                if action == "H" or action == "Dh" or action == "Ds":
                    ai_hand.append(deck.pop())
                    print(f"AI {idx+1} hits: new total {hand_value(ai_hand)}")
                    animate_ai_turn()
                    print(Fore.CYAN + f"AI Player {idx+1} hand:")
                    draw_hand(ai_hand)
                    if hand_value(ai_hand) > 21:
                        print(f"AI {idx+1} busts!")
                        break
                else:
                    animate_ai_turn()
                    print(Fore.CYAN + f"AI Player {idx+1} hand:")
                    draw_hand(ai_hand)
                    print(f"AI {idx+1} stands at {hand_value(ai_hand)}")
                    break

        # Human's turn
        while True:
            if check_escape_key():
                return "exit"
            print("\nDealer's hand:")
            draw_hand(dealer_hand, hide_first=True)
            print("\nYour hand:")
            draw_hand(human_hand)
            player_total = hand_value(human_hand)
            dealer_up_value = hand_value([dealer_hand[1]])
            print(f"Your total: {player_total}, Dealer upcard: {dealer_up_value}")
            suggestion = get_strategy_action(human_hand, dealer_hand[1])
            print(f"Suggested: {suggestion}")

            action = input("Choose action ([h]it, [s]tand): ").lower()
            if action == 'h':
                human_hand.append(deck.pop())
                if hand_value(human_hand) > 21:
                    print("\nYou busted!")
                    break
            elif action == 's':
                break
            else:
                print("Invalid input, please enter 'h' or 's'.")

        # Dealer's turn and outcome
        player_total = hand_value(human_hand)
        if player_total <= 21:
            # European variant: deal hole card now
            if variant.startswith('e'):
                dealer_hand[0] = deck.pop()
                print("\nDealer's hole card:")
                draw_hand([dealer_hand[0]])
            # Dealer drawing logic
            while True:
                dv = hand_value(dealer_hand)
                if variant.startswith('u'):  # American: hit on soft 17
                    if dv < 17 or is_soft_17(dealer_hand):
                        dealer_hand.append(deck.pop())
                    else:
                        break
                else:  # European: stand on soft 17
                    if dv < 17:
                        dealer_hand.append(deck.pop())
                    else:
                        break
            print("\nDealer's final hand:")
            draw_hand(dealer_hand)
        dealer_total = hand_value(dealer_hand)

        # Payout
        if player_total > 21 or (dealer_total <= 21 and dealer_total > player_total):
            print(Fore.RED + "Dealer wins.")
            # bet is lost
        elif dealer_total > 21 or player_total > dealer_total:
            print(Fore.GREEN + "You win!")
            balance += bet * 2
        else:
            print(Fore.YELLOW + "Push.")
            balance += bet
        print(Fore.CYAN + f"New Balance: ${balance:.2f}")

        # Prompt for another round
        if check_escape_key():
            return "exit"
        again = input("Play again? (y/n): ").lower()
        if again != 'y':
            print("Thanks for playing!")
            break
    return

def main():
    """Main entry point for Blackjack."""
    global balance
    # Entrance animation and header
    if check_escape_key():
        return
    animate_card_flip(times=1)
    clear()
    print(Fore.GREEN + Style.BRIGHT + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + "♠♥ ♣♦   PY CASINO BLACKJACK   ♠♥ ♣♦".center(60))
    print(Fore.GREEN + Style.BRIGHT + "=" * 60)
    # Menu prompts
    print(Fore.CYAN + f"Current Balance: ${balance:.2f}")
    variant = input("Choose variant [American(us)/European(eu)]: ").strip().lower()
    if check_escape_key(): return
    cash = float(input("Enter your starting cash: "))
    if check_escape_key(): return
    num_ai = int(input("Number of AI players (0-5): "))
    if check_escape_key(): return
    seat = int(input(f"Choose your seat (1 to {num_ai+1}): "))
    if check_escape_key(): return
    balance = cash
    # Start game session
    play_blackjack(variant, cash, num_ai, seat)
    # Farewell
    print(Fore.MAGENTA + Style.BRIGHT + "\nThank you for playing at PY CASINO!")

if __name__ == "__main__":
    # Run Blackjack menu; allow ESC to exit
    main()