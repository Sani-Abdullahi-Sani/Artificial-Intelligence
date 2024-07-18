import chess
from reconchess import *
from reconchess.utilities import without_opponent_pieces
from reconchess.utilities import is_illegal_castle


def is_consistent_with_window(state_fen, window_description):
    board = chess.Board(state_fen)
    for piece_info in window_description.split(';'):
        square, piece = piece_info.split(':')
        board_piece = board.piece_at(chess.parse_square(square))
        # Check if the square is empty in the window description
        if piece == '?':
            if board_piece is not None:
                return False
        # Check if the piece on the board matches the one described in the window
        elif board_piece is None or board_piece.symbol() != piece:
            return False
    return True


n_states = int(input())

potential_states = [input() for _ in range(n_states)]

window_description = input()

consistent_states = []
for state in potential_states:
    if is_consistent_with_window(state, window_description):
        consistent_states.append(state)

sorted_consistent_states = sorted(consistent_states)

for state in sorted_consistent_states:
    print(state)