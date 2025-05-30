
# CodeHSG
Group project repository for the Code@HSG group project | SP25

## 🎯 Project Overview  
This repository was developed as a collaborative group project during the Spring 2025 semester at HSG. The central concept was to create a **modular gaming platform** that allows contributors to add their own Python-based games accessible via a unified **main menu interface**.

The main entry point is the `main_menu.py` script. From your terminal, simply run:

```bash
python main_menu.py
```

This will launch an interactive menu that lets users choose among the available games. The framework was designed to be extensible and beginner-friendly, so that each team member could easily contribute a game or two. 

PS: it was also easier to find consensus for this idea 😄

## 🕹️ Available Games

### 🃏 Blackjack  
A casino-style blackjack game where players compete against the house. It includes both European and American rule variants. Cards are drawn from a finite, non-replacing deck to enhance realism. AI hands and dealer cards are displayed after each turn.

### 💀 Hangman  
A classic word guessing game. Players guess one letter at a time to reveal the hidden word before running out of attempts. The key feature the contributor tried to implement is a hint mechanism where the player can trade away tries against it.

### 🧠 Mastermind  
A code-breaking game where the player attempts to guess a hidden sequence of numbers within a limited number of tries. The key feature of this game is the possibility to adjust of the difficulty level.

### ✊ Rock Paper Scissors  
The player select rock, paper, or scissors, and the result is shown instantly. This project demonstrate the contributor experimentation with random sampling and ASCII style art. 

### 🎡 Roulette *(Terminal-Incompatible)*  
Simulates a roulette allowing the player to gamble away fake money. In this game, the contributor experimented with the **pygame** package and developed a separate interface. 

### 🐍 Snake  
A terminal-based implementation of the classic Snake game. The player can control the growing snake with directional input while avoiding walls and self-collision. Each time the snake grows, its speed increases, thereby incrementally rendering the game more difficult.

### ❌ Tic Tac Toe  
The tic tac toe is the first project made in this repo. The games allows the player either to play in the pass-&-play mode or against an AI. In this project, the AI will follow an optimal strategy, with some noise though, thereby making the game challenging to play.


📝 **Note**: All games except *Roulette* are playable directly within the terminal. We've tested everything using **Visual Studio Code**, and it runs smoothly, though we recommend verifying that all the packages are well installed. In the main_menu.py script, the code tries to install all the packages. You may want to have a look at it before running the code.


