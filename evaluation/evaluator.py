from Pieces.king import King
from Pieces.piece import Piece
from evaluator_config import *

def evaluate(white_regular_pieces: list[Piece], black_regular_pieces: list[Piece],
             all_attacking_white_squares: int, all_attacking_black_squares: int,
             white_king: King, black_king: King) -> int:

    white_evaluation = 0
    black_evaluation = 0

    # Calculate pieces values:
    for piece in white_regular_pieces:
        white_evaluation += piece.get_piece_value()

    for piece in black_regular_pieces:
        black_evaluation += piece.get_piece_value()

    # Calculate attacking pieces evaluation
    white_evaluation += all_attacking_white_squares.bit_count() * SQUARE_IN_VIEW_VALUE
    black_evaluation += all_attacking_black_squares.bit_count() * SQUARE_IN_VIEW_VALUE

    # Calculate checking king value
    if (all_attacking_black_squares & (1 << white_king.position_index)) > 0:
        black_evaluation += CHECKS_ENEMY_KING_VALUE

    if (all_attacking_white_squares & (1 << black_king.position_index)) > 0:
        white_evaluation += CHECKS_ENEMY_KING_VALUE

    return white_evaluation - black_evaluation