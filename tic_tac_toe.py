

# Tic-Tac-Toe Game in Python
# This script implements a simple Tic-Tac-Toe game that can be played in two modes:
# 1. Single Player: Play against an AI opponent.
# 2. Pass & Play: Two players take turns playing on the same device.
# The game features a console-based interface, allowing players to input their moves using numbers
# corresponding to the cells on the board. The AI uses the Minimax algorithm with alpha-beta pruning
# to determine the best move, and it can also make random moves to add unpredictability.
# The game keeps track of scores and displays the current state of the board after each move.
# The game also includes an opening book loaded from a JSON file, which contains pre-calculated optimal moves
# for various board states. If the board state is not found in the book, the AI falls back to the Minimax algorithm.

# List of functions:
# 1. clear(): Clears the console screen.
# 2. no_possible_win(board): Checks if there are no possible winning conditions left on the board.
# 3. print_board(board, score, players, show_numbers): Displays the current state of the board with player names and scores.
# 4. check_win(board, player): Checks if the given player has achieved a win on the board.
# 5. board_full(board): Checks if the board is full (no empty cells).
# 6. get_move(board, player): Prompts the player to enter their move.
# 7. minimax(board, depth, is_maximizing, alpha, beta): Implements the Minimax algorithm with alpha-beta pruning.
# PS: This function did not work that well, so I used a JSON file with pre-calculated moves.
#    to determine the best move for the AI.
# 8. load_opening_book(): Loads the opening book from a JSON file.
# 9. best_move(board): Determines the best move for the AI using the Minimax algorithm.
# 10. ai_move(board): Determines the AI's move on the board.
# 11. play_round(players, single_mode, score, show_numbers): Plays a single round of Tic-Tac-Toe.
# 12. game_loop(single_mode): Main game loop for playing rounds.
# 13. main_menu(): Displays the main menu and handles user input to navigate between modes.



# Import necessary libraries
import os # For clearing the console screen
import shutil # For getting terminal size
import time # For adding delays in the game
import random # For generating random moves for the AI --> see AI_RANDOMNESS
import json # For loading the opening book of optimal moves from a JSON file

# ── Opening-book of optimal moves ─────────────────────────────────────────
BOOK = {}
try:
    from pathlib import Path
    BOOK = json.load(Path(__file__).with_name("tictactoe_book.json").open())
except (FileNotFoundError, json.JSONDecodeError):
    print("Warning: opening‑book not found; AI will use Minimax only.")

# Constants

# AI randomness probability
# This value determines the chance that the AI will make a random move instead of using the Minimax algorithm.
# A value of 0.2 means there is a 20% chance the AI will make a random move.
AI_RANDOMNESS = 0.2  # 20% chance to make a random move


# it clears the console screen
def clear():
    # Clear the console screen based on the operating system
    os.system('cls' if os.name == 'nt' else 'clear') 

# check if no winning condition is possible by using a table of winning conditions
def no_possible_win(board):
    """
    Check if there is no possible winning condition left on the board.

    Args:
        board (list of list of str): A 3x3 tic-tac-toe board where each cell contains 'X', 'O', or ''.

    Returns:
        bool: True if no winning condition is possible, False otherwise.
    """
    # Define all possible winning conditions
    win_cond = [
        (0,0,0,1,0,2), (1,0,1,1,1,2), (2,0,2,1,2,2),  # Rows
        (0,0,1,0,2,0), (0,1,1,1,2,1), (0,2,1,2,2,2),  # Columns
        (0,0,1,1,2,2), (0,2,1,1,2,0)                 # Diagonals
    ]
    # Check if any line has both 'X' and 'O', making it impossible to win
    for x1, y1, x2, y2, x3, y3 in win_cond:
        line = [board[x1][y1], board[x2][y2], board[x3][y3]]
        if not ('X' in line and 'O' in line):
            return False
    return True

# Function to print the game board
def print_board(board, score, players, show_numbers):
    """
    Clears the console and prints the current state of the tic-tac-toe board with player names and scores.

    Args:
        board (list of list of str): The 3x3 game board. Each cell contains 'X', 'O', or ' '.
        score (dict): A dictionary with players' names as keys and their current scores as values.
        players (list of str): List containing names of the two players. Expected order: [player1, player2].
        show_numbers (bool): If True, empty cells are annotated with their corresponding cell number (1-9).

    Returns:
        None
    """
    clear()  # Clear the console screen
    
    # Get the terminal width to format the output centrally
    width = shutil.get_terminal_size().columns
    
    # Create header and score display strings
    header = f"{players[0]} vs {players[1]}"
    score_line = f"Score: {players[0]} {score[players[0]]} - {score[players[1]]} {players[1]}"
    
    # Print the header centered and the score right-aligned
    print(header.center(width))
    print(score_line.rjust(width))
    print("\n")
    
    # Prepare the display board with numbers in empty cells if show_numbers is True
    display = []
    for i in range(3):
        row = []
        for j in range(3):
            # If showing numbers and cell is empty (' '), display cell number starting at 1
            if show_numbers and board[i][j] == ' ':
                row.append(f"({i*3+j+1})")
            else:
                row.append(board[i][j])
        display.append(row)
    
    # Define cell width and separator line for board display
    cell_width = 7
    sep_line = "+" + "+".join(["=" * cell_width] * 3) + "+"
    
    # Print each row of the board with appropriate formatting
    for row in display:
        # Center each item in the cell
        line = "|" + "|".join(item.center(cell_width) for item in row) + "|"
        pad = " " * ((width - len(line)) // 2)
        print(pad + sep_line)
        print(pad + line)
    
    # Print the bottom separator line
    pad = " " * ((width - len(sep_line)) // 2)
    print(pad + sep_line)
    
    # Display additional help message
    print("\nType 'esc' to return to menu at any time.\n")

# check if a player has won
def check_win(board, player):
    """
    Check if the given player has achieved a win on the tic-tac-toe board.

    Args:
        board (list of list of str): A 3x3 tic-tac-toe board. Each cell contains 'X', 'O', or ' '.
        player (str): The player's symbol ('X' or 'O') to check for a win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # we have eight possible winning conditions as tuples of cell indices.
    win_cond = [
        (0,0, 0,1, 0,2),  # Top row
        (1,0, 1,1, 1,2),  # Middle row
        (2,0, 2,1, 2,2),  # Bottom row
        (0,0, 1,0, 2,0),  # Left column
        (0,1, 1,1, 2,1),  # Middle column
        (0,2, 1,2, 2,2),  # Right column
        (0,0, 1,1, 2,2),  # Diagonal from top-left to bottom-right
        (0,2, 1,1, 2,0)   # Diagonal from top-right to bottom-left
    ]
    
    # Iterate through each winning condition
    for x1, y1, x2, y2, x3, y3 in win_cond:
        # Check if all three cells in the current winning condition have the player's symbol.
        if board[x1][y1] == board[x2][y2] == board[x3][y3] == player:
            return True  # Winning condition met
    
    # If none of the winning conditions are met, return False.
    return False

# Function to check if the board is full
def board_full(board):
    """
    Check if the tic-tac-toe board is full.

    Args:
        board (list of list of str): The 3x3 game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    return all(cell != ' ' for row in board for cell in row)

# Function to get a player's move
def get_move(board, player):
    """
    Prompt the player to enter their move on the tic-tac-toe board.

    Args:
        board (list of list of str): The 3x3 game board. Each cell contains 'X', 'O', or ' '.
        player (str): The name or symbol of the player making the move.

    Returns:
        tuple: A tuple (row, column) representing the player's chosen cell, or 'esc' if the player exits.
    """
    while True:
        move = input(f"{player}, enter your move (1-9): ")
        if move.lower() == 'esc':
            return 'esc'
        if move.isdigit() and 1 <= int(move) <= 9:
            r, c = divmod(int(move) - 1, 3) # Convert move to row and column indices
            if board[r][c] == ' ': # Check if the cell is empty
                return r, c 
            else:
                print("Cell is taken!") # Prompt if the cell is already occupied
        else:
            print("Invalid input.") # Prompt if the input is not a valid number between 1 and 9



# ── Minimax Algorithm with Alpha-Beta Pruning ─────────────────────────────

# Minimax algorithm with alpha-beta pruning. It is still being worked on, but it is not used in the final version of the game.
def minimax(board, depth, is_maximizing, alpha, beta):
    """
    Recursively evaluates the tic-tac-toe board using the Minimax algorithm enhanced
    with alpha-beta pruning to determine the best score achievable from a given state.

    Args:
        board (list of list of str): The current 3x3 tic-tac-toe board.
        depth (int): The current recursion depth, used to penalize longer wins.
        is_maximizing (bool): Flag indicating whether we are maximizing (True for 'O')
                              or minimizing (False for 'X') the score.
        alpha (float): The best already explored option along the path to the root for the maximizer.
        beta (float): The best already explored option along the path to the root for the minimizer.

    Returns:
        int: The score of the board using evaluation rules. A higher score indicates a more favorable
             outcome for 'O', while a lower score favors 'X'.
    """
    # If AI ('O') wins, return a high positive score, adjusted by depth to prefer faster wins.
    if check_win(board, 'O'):
        return 10 - depth

    # If human ('X') wins, return a high negative score, adjusted by depth to delay losses.
    if check_win(board, 'X'):
        return depth - 10

    # If the board is full (or no moves lead to a win), it's a tie.
    if board_full(board):
        return 0

    # Prioritized order to check moves: center, corners, then edges.
    priority = [(1, 1)] + [(0, 0), (0, 2), (2, 0), (2, 2)] + [(0, 1), (1, 0), (1, 2), (2, 1)]

    if is_maximizing:
        max_eval = -float('inf')
        # Evaluate moves for AI ('O')
        for i, j in [(i, j) for i, j in priority if board[i][j] == ' ']:
            board[i][j] = 'O'  # Try a move
            # Evaluate resulting board recursively
            eval = minimax(board, depth + 1, False, alpha, beta)
            board[i][j] = ' '  # Undo move
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)  # Update alpha if a better move is found
            if beta <= alpha:
                # Beta cutoff: stop exploring this branch if minimizer already has a better choice
                break
        return max_eval
    else:
        min_eval = float('inf')
        # Evaluate moves for human ('X')
        for i, j in [(i, j) for i, j in priority if board[i][j] == ' ']:
            board[i][j] = 'X'  # Try a move
            eval = minimax(board, depth + 1, True, alpha, beta)
            board[i][j] = ' '  # Undo move
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)  # Update beta if a lower score is found
            if beta <= alpha:
                # Alpha cutoff: stop exploring this branch if maximizer already has a better option
                break
        return min_eval






# Function to determine the best move for the AI
def best_move(board):
    """
    Determines the best move for the AI ('O') using the Minimax algorithm.

    Args:
        board (list of list of str): The current 3x3 tic-tac-toe board.

    Returns:
        tuple: A tuple (row, column) representing the best move for the AI.
    """
    best_val = -float('inf')  # Initialize the best value to negative infinity
    best = None  # Initialize the best move as None

    # Prioritized order to check moves: center, corners, then edges
    priority = [(1, 1)] + [(0, 0), (0, 2), (2, 0), (2, 2)] + [(0, 1), (1, 0), (1, 2), (2, 1)]

    # Iterate through all possible moves in the prioritized order
    for i, j in [(i, j) for i, j in priority if board[i][j] == ' ']:
        board[i][j] = 'O'  # Try the move
        # Evaluate the move using the Minimax algorithm
        move_val = minimax(board, 0, False, -float('inf'), float('inf'))
        board[i][j] = ' '  # Undo the move

        # Update the best move if the current move has a higher evaluation score
        if move_val > best_val:
            best_val = move_val
            best = (i, j)

    return best  # Return the best move


# ── AI Move Function ─────────────────────────────────────────────────────
# Function to make the AI's move
def ai_move(board):
    """
    Determines the AI's move on the tic-tac-toe board.

    Args:
        board (list of list of str): The current 3x3 tic-tac-toe board.

    Returns:
        tuple: A tuple (row, column) representing the AI's chosen cell.
    """
    if random.random() < AI_RANDOMNESS: # Introduce randomness in AI moves
        # Random move to add unpredictability
        return random.choice([(i, j) for i in range(3) for j in range(3) if board[i][j] == ' '])
    
    # Generate a key representing the current board state
    key = "".join(cell if cell != ' ' else '-' for row in board for cell in row)
    
    # Check if the current board state exists in the opening book
    if key in BOOK:
        idx = BOOK[key]
        return divmod(idx, 3)  # Convert the index to row and column
    
    # Use the Minimax algorithm to determine the best move
    mv = best_move(board)
    if mv:
        return mv
    
    # Fallback to a random move if no optimal move is found
    return random.choice([(i, j) for i in range(3) for j in range(3) if board[i][j] == ' '])


# Load optimal move book from JSON
# The json file should contain a mapping of board states to optimal moves taken from teh web.
# The keys are strings representing the board state, and the values are indices of the optimal move.
# Example: {"-X O O": 4} means the optimal move for the board state "-X O O" is at index 4 (row 1, column 1).
def load_opening_book():
    """
    Load the opening book from a JSON file. The file should contain a mapping of board states to optimal moves.

    Returns:
        dict: A dictionary where keys are strings representing board states and values are indices of optimal moves.
    """
    try:
        with open(os.path.join(os.path.dirname(__file__), "tictactoe_book.json")) as f:
            return json.load(f)
    except FileNotFoundError:
        print("Warning: tictactoe_book.json not found, falling back to Minimax.")
        return {}



# ── Game Logic ──────────────────────────────────────────────────────────

# Function to play a single round of Tic-Tac-Toe
def play_round(players, single_mode, score, show_numbers):
    board = [[' ']*3 for _ in range(3)]  # Initialize an empty board
    turn = 0  # Track the current turn
    while True:
        print_board(board, score, players, show_numbers)  # Display the board
        current = players[turn%2]  # Determine the current player
        symbol = 'X' if turn%2==0 else 'O'  # Determine the player's symbol
        if single_mode and current=="AI":
            time.sleep(0.5)  # Add a delay for AI moves
            r,c = ai_move(board)  # Get AI's move
        else:
            mv = get_move(board, current)  # Get player's move
            if mv=='esc':  # Check if the player wants to exit
                return 'esc'
            r,c = mv
        board[r][c]=symbol  # Update the board with the player's move
        if check_win(board, symbol):  # Check if the player has won
            print_board(board, score, players, show_numbers)
            print(f"{current} wins!")
            score[current]+=1  # Update the player's score
            time.sleep(1)
            return
        if board_full(board) or no_possible_win(board):  # Check for a tie
            print_board(board, score, players, show_numbers)
            print("It's a tie!")
            time.sleep(1)
            return
        turn+=1  # Increment the turn counter

# Main game loop
def game_loop(single_mode):
    clear()
    if single_mode:
        p1 = input("Enter your name: ")
        players = [p1, "AI"]
    else:
        p1 = input("Player 1 name: ")
        p2 = input("Player 2 name: ")
        players = [p1, p2]
    
    # Ask if the user wants to display a numbered grid for empty cells
    while True:
        ch = input("Numbered grid? (y/n): ")
        if ch.lower() == 'esc': 
            return  # Exit to menu if 'esc' is entered
        if ch.lower() in ('y', 'n'): 
            show_numbers = ch.lower() == 'y'
            break  # Exit the loop if valid input is provided
    
    # Ask for the number of rounds to play
    while True:
        rd = input(f"{players[0]}, how many rounds? ")
        if rd.lower() == 'esc': 
            return  # Exit to menu if 'esc' is entered
        if rd.isdigit() and int(rd) > 0: 
            rounds = int(rd)
            break  # Exit the loop if valid input is provided
    
    # Initialize the score dictionary for both players
    score = {players[0]: 0, players[1]: 0}
    
    # Play the specified number of rounds
    for _ in range(rounds):
        if play_round(players, single_mode, score, show_numbers) == 'esc': 
            return  # Exit to menu if 'esc' is entered during a round
    
    # Display the final score and determine the winner
    clear()
    print_board([[' '] * 3] * 3, score, players, show_numbers)
    print(f"Final: {players[0]} {score[players[0]]} - {score[players[1]]} {players[1]}")
    
    if score[players[0]] > score[players[1]]:
        print(f"{players[0]} wins!")
    elif score[players[0]] < score[players[1]]:
        print(f"{players[1]} wins!")
    else:
        print("Draw!")
    
    # Wait for user input before returning to the menu
    input("Enter to menu...")

def main() -> None:
    """
    Zero‑argument entrypoint so the arcade launcher can start the game.
    Launches the Tic‑Tac‑Toe menu.
    """
    main_menu()

# Main menu function
def main_menu():
    """
    Displays the main menu for the Tic-Tac-Toe game and handles user input to navigate
    between single-player mode, pass-and-play mode, and exiting the game.

    Returns:
        None
    """
    while True:
        clear()  # Clear the console screen
        # Display the menu header
        print("=" * 50)
        print(" ★ TIC-TAC-TOE TERMINAL EDITION ★ ".center(50))
        print("=" * 50)
        # Display menu options
        print("1. Single Player")
        print("2. Pass & Play")
        print("3. Exit")
        print("esc to menu.")
        # Get user input for menu choice
        c = input("Choice: ")
        if c == '1':  # Single-player mode
            game_loop(True)
        elif c == '2':  # Pass-and-play mode
            game_loop(False)
        elif c == '3':  # Exit the game
            break
        else:  # Invalid input, wait briefly before re-displaying the menu
            time.sleep(1)


if __name__ == "__main__":
    main()
