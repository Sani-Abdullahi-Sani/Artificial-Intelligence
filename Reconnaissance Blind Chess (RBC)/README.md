# Reconnaissance Blind Chess (RBC) Project

## Introduction

In this project, we developed an agent to play Reconnaissance Blind Chess (RBC), a variant of chess that incorporates imperfect information. Unlike traditional chess, players in RBC cannot see their opponents' pieces and must deduce their positions using limited sensing moves. Our goal was to build an agent that can effectively play RBC by overcoming the challenges of partial observability.

## System Setup

- **Environment:** Python
- **Libraries:** ReconChess, Stockfish

To install the necessary Python library, run the following command:
```bash
pip install reconchess
```

## Reconnaissance Blind Chess

RBC follows the same rules as standard chess with the key difference that players cannot see their opponents' pieces. Instead, each player can make a "sensing" move each turn to observe a 3x3 area of the board, gaining information about that region. The objective of RBC is to capture the opponent's king.

## Rules

- The game starts with the standard chess setup.
- Each turn consists of two phases:
  1. **Sensing Phase:** The player selects a square to sense, revealing a 3x3 window around it.
  2. **Move Phase:** The player makes a standard chess move or passes.
- Players are informed if a move is illegal, and they pass their turn.

For a detailed overview of the rules, visit the [RBC Game Rules](https://rbc.jhuapl.edu/gameRules).

## Requirements

Our agent is designed to play RBC by handling the partial observability of the game. The primary tasks included:

1. **Board Representation:** Keeping track of all possible board configurations given the uncertainty about the opponent’s pieces.
2. **Move Execution:** Running Stockfish on all potential board states and choosing the most popular move suggested by Stockfish across all the boards.
3. **Sensing:** Selecting a square to sense uniformly at random and using the information to narrow down possible board states.

### Steps to Build the Agent

1. **Read Documentation:** Start by reading the [ReconChess documentation](https://reconchess.readthedocs.io/en/latest/).
2. **Setup:** Install the ReconChess package and copy the Trout bot example.
3. **Play a Game:** Follow the instructions to play a game between your Trout bot and a random agent.

### Agent Strategy

- **Board Tracking:** Maintain a list of possible board configurations based on the observed information.
- **Sensing:** Randomly select squares to sense and use the information to update possible board states.
- **Move Selection:** Use Stockfish to determine the best move across all potential board states and execute the most popular move.

## Object Detection

The agent uses sensing information to detect the presence of pieces in specific areas of the board. This information is used to eliminate impossible board configurations and focus on the most likely states.

## Conclusion

In this project, we developed an agent for Reconnaissance Blind Chess that effectively handles the challenges of partial observability. Key learnings included the importance of maintaining an accurate representation of possible board states and utilizing sensing information to make informed decisions. Our agent uses Stockfish to select the best moves, ensuring competitive performance in the game.

---
