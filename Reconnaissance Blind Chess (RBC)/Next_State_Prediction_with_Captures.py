import chess
from reconchess import *
from reconchess.utilities import without_opponent_pieces
from reconchess.utilities import is_illegal_castle
# Read the FEN string from input
fen = input()

# Read the square on which a capture took place
capture_square = input()

# Create a board object from the FEN string
board = chess.Board(fen)

# Generate all possible legal moves for the current position
possible_moves = list(board.pseudo_legal_moves)

# Generate next positions by applying each move to the current board position
next_positions = []
for move in possible_moves:
    # Check if the move captures on the given square
    if board.is_capture(move) and move.to_square == chess.parse_square(capture_square):
        # Make a copy of the current board
        next_board = board.copy()
        # Apply the move to the copied board
        next_board.push(move)
        # Get the FEN string of the next position and add it to the list
        next_positions.append(next_board.fen())

# Sort the resulting positions alphabetically
sorted_positions = sorted(next_positions)

# Output the sorted list of positions
for position in sorted_positions:
    print(position)