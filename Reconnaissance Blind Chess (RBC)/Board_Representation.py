import chess

# Read the FEN string from input
fen = input()
board = chess.Board(fen)
# Print the ASCII board
print(board)
