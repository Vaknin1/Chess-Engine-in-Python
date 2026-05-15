from Pieces.piece import Piece

from Pieces.bishop import Bishop
from Pieces.king import King
from Pieces.pawn import Pawn
from Pieces.queen import Queen
from Pieces.rook import Rook

from constants import *

class GameManager:

    WHITE_BOARD = ((1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5)
                   | (1 << 6) | (1 << 7) | (1 << 8) | (1 << 9) | (1 << 10) |
                   (1 << 11) | (1 << 12) | (1 << 13) | (1 << 14) | (1 << 15))

    BLACK_BOARD = ((1 << 48) | (1 << 49) | (1 << 50) | (1 << 51) | (1 << 52) | (1 << 53)
                   | (1 << 54) | (1 << 55) | (1 << 56) | (1 << 57) | (1 << 58) | (1 << 59)
                   | (1 << 60) | (1 << 61) | (1 << 62) | (1 << 63))

    white_kingside_rook = Rook(COLOR_WHITE, 7)
    white_queenside_rook = Rook(COLOR_WHITE, 0)

    WHITE_PIECES = {
        "kingside_rook": white_kingside_rook,
        "queenside_rook": white_queenside_rook,
        "kingside_bishop": Bishop(COLOR_WHITE, 5),
        "queenside_bishop": Bishop(COLOR_WHITE, 2),
        "queen": Queen(COLOR_WHITE, 3),
        "king": King(COLOR_WHITE, 4, white_kingside_rook, white_queenside_rook)
    }

    black_kingside_rook = Rook(COLOR_BLACK, 63)
    black_queenside_rook = Rook(COLOR_BLACK, 56)

    BLACK_PIECES = {
        "kingside_rook": black_kingside_rook,
        "queenside_rook": black_queenside_rook,
        "kingside_bishop": Bishop(COLOR_WHITE, 61),
        "queenside_bishop": Bishop(COLOR_WHITE, 58),
        "queen": Queen(COLOR_WHITE, 59),
        "king": King(COLOR_WHITE, 60, black_kingside_rook, black_queenside_rook)
    }

    def __init__(self, color):
        self.color = color
        if self.color == COLOR_WHITE:
            self.pieces = self.WHITE_PIECES
        else:
            self.pieces = self.BLACK_PIECES


    def convert_position_to_bitboard_index(self, position: str):
        column, row = position[0], int(position[1])
        column_as_num = ord(column) - ord('a') - 1

        return column_as_num  + row * 8

    def evaluate_engine_move(self, white):

if __name__ == '__main__':
    print("Select Color: (w) / (b)")
    game_manager = GameManager(COLOR_WHITE if input() == "w" else COLOR_BLACK)

    while True:
        print("Enter move played")
