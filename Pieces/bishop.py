from Pieces.piece import Piece
from evaluation.evaluator_config import BISHOP_VALUE

class Bishop(Piece):
    def __init__(self, color, initial_position_index):
        super().__init__(color, initial_position_index)
    
    def get_all_legal_moves(self, white_board: int, black_board: int):
        return self.moves_helper.get_legal_diagonal_moves(self.position_index, 
                                                          white_board, 
                                                          black_board, 
                                                          self.color)
    
    def get_piece_value(self) -> int:
        return BISHOP_VALUE