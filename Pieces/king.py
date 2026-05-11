from Pieces.piece import Piece
from constants import *

class King(Piece):
    def __init__(self, color, initial_position_index: int, 
                 kingside_rook, queenside_rook):
        super().__init__(color, initial_position_index)
        self.can_still_castle = True

        self.kingside_rook = kingside_rook
        self.queenside_rook = queenside_rook

    def get_all_legal_moves(self, white_board: int, black_board: int, squares_enemy_attacks: int):
        legal_moves = self.moves_helper.get_legal_king_moves(self.position_index, white_board, black_board, self.color)

        if self.can_still_castle:
            legal_moves = legal_moves | self._get_legal_castling_moves(white_board, black_board, squares_enemy_attacks)
    
        return legal_moves

    def _get_legal_castling_moves(self, white_board, black_board, squares_enemy_attacks: int):
        legal_castling_moves = 0

        if self.color == COLOR_WHITE:
            backline = (1 << 1) | (1 << 2) | (1 << 3) | (1 << 5) | (1 << 6)
            
            if (white_board & backline) > 0:
                return 0
            
            if not self.kingside_rook.has_moved:
                legal_castling_moves = (1 << 6)
            
            if not self.queenside_rook.has_moved:
                legal_castling_moves = legal_castling_moves | (1 << 2)
        
        return legal_castling_moves