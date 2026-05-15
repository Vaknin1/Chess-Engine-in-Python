from Pieces.piece import Piece
from evaluation.evaluator_config import PAWN_VALUE

class Pawn(Piece):

    def __init__(self, color, initial_position_index):
        super().__init__(color, initial_position_index)
    
    def get_all_legal_moves(self, white_board, black_board):
        return self.moves_helper.get_legal_pawn_moves(self.position_index, white_board, black_board, self.color)

        # Should implement En Passaunt or whatever its called

    def get_piece_value(self) -> int:
        return PAWN_VALUE