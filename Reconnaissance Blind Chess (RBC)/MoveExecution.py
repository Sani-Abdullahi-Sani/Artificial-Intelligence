import chess

# Read the FEN string from input
fen = input()

board = chess.Board(fen)

# Read the move from input
move_uci = input()

# Convert the move from UCI format to Move object
move = chess.Move.from_uci(move_uci)

# Make the move
board.push(move)

print(board.fen())