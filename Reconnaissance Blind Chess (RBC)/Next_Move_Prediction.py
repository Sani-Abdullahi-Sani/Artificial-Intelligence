import chess
from reconchess import *
from reconchess.utilities import without_opponent_pieces
from reconchess.utilities import is_illegal_castle

# Read the FEN string from input
fen = input()

# Create a board object from the FEN string
board = chess.Board(fen)

# Generate all possible legal moves for the current position, including null move
possible_moves = list(board.pseudo_legal_moves)
possible_moves.append(chess.Move.null())

# Generate castling moves without opponent pieces
for move in without_opponent_pieces(board).generate_castling_moves():
    if not is_illegal_castle(board, move):
        # Add the valid castling move to the list of possible moves
        possible_moves.append(move)

# Sort the resulting moves alphabetically
sorted_moves = list(sorted(set(possible_moves), key=str))

# Output the sorted list of moves
for move in sorted_moves:
    print(move)