import chess.engine

# Initialize the Stockfish engine
engine = chess.engine.SimpleEngine.popen_uci('/opt/stockfish/stockfish', setpgrp=True)

def generate_move(fen: str) -> str:
    try:
        # Create a board object from the FEN string
        board = chess.Board(fen)

        # Check if the opposing king is under attack
        enemy_king_square = board.king(not board.turn)
        if enemy_king_square:
            # Check if any of our pieces can capture the opposing king
            enemy_king_attackers = board.attackers(board.turn, enemy_king_square)
            if enemy_king_attackers:
                # If so, capture the opposing king
                attacker_square = enemy_king_attackers.pop()
                return attacker_square.uci() + enemy_king_square.uci()

        # Otherwise, ask Stockfish for a move with a time limit of 0.5 seconds
        result = engine.play(board, chess.engine.Limit(time=0.5))
        return result.move.uci()
    except chess.engine.EngineTerminatedError as e:
        print(f'Stockfish Engine terminated unexpectedly: {e}')
        return ''
    except chess.engine.EngineError as e:
        print(f'Stockfish Engine encountered an error: {e}')
        return ''

# Read the number of boards
n_boards = int(input())

# Initialize a dictionary to store the frequency of moves
move_freq = {}

# Iterate through each board
for _ in range(n_boards):
    # Read the FEN string representing the position
    fen = input()

    # Generate the move for the board
    move = generate_move(fen)

    # Increment the frequency of the move in the dictionary
    move_freq[move] = move_freq.get(move, 0) + 1

# Find the most commonly recommended move
most_common_moves = [move for move, freq in move_freq.items() if freq == max(move_freq.values())]

# Sort the most common moves alphabetically
most_common_moves.sort()

# Output the most commonly recommended move in UCI format
if most_common_moves:
    print(most_common_moves[0])
else:
    print("No valid move found")

# Close the Stockfish engine
engine.quit()
