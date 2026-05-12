

from Pieces.king import King
from Pieces.piece import Piece


class Rook(Piece):

    def __init__(self, color, initial_position_index):
        super().__init__(color, initial_position_index)
        self.has_moved = False
    
    def get_all_legal_moves(self, white_board, black_board):
        return self.moves_helper.get_legal_horizontal_vertical_moves(self.position_index, white_board, black_board, self.color)
    
    def move_piece(self, new_position_index, white_board, black_board):
        self.has_moved = True
        return super().move_piece(new_position_index, white_board, black_board)