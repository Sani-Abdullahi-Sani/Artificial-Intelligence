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
                attacker_square = chess.square_name(enemy_king_attackers.pop())
                return attacker_square + chess.square_name(enemy_king_square)


        # Otherwise, ask Stockfish for a move with a time limit of 0.5 seconds
        result = engine.play(board, chess.engine.Limit(time=0.5))
        return result.move.uci()
    except chess.engine.EngineTerminatedError as e:
        print(f'Stockfish Engine terminated unexpectedly: {e}')
        return ''
    except chess.engine.EngineError as e:
        print(f'Stockfish Engine encountered an error: {e}')
        return ''

# Read the FEN string representing the position
fen = input()

# Generate the move
move = generate_move(fen)

# Output the move in UCI format
if move:
    print(move)
else:
    print("No valid move found")

# Close the Stockfish engine
engine.quit()
