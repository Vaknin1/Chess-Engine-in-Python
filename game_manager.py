from Pieces.piece import Piece

from Pieces.bishop import Bishop
from Pieces.king import King
from Pieces.pawn import Pawn
from Pieces.queen import Queen
from Pieces.rook import Rook

from constants import *

class GameManager:
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