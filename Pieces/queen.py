from Pieces.piece import Piece
from constants import *
from evaluation.evaluator_config import QUEEN_VALUE

class Queen(Piece):
    def __init__(self, color, initial_position_index: int):
        super().__init__(color, initial_position_index)

    def get_all_legal_moves(self, white_board: int, black_board: int):
        return (self.moves_helper.get_legal_diagonal_moves
                        (self.position_index, white_board, black_board, self.color)
                + self.moves_helper.get_legal_horizontal_vertical_moves
                        (self.position_index, white_board, black_board, self.color))

    def get_piece_value(self) -> int:
        return QUEEN_VALUE