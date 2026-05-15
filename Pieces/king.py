from Pieces.piece import Piece
from Pieces.rook import Rook
from constants import *
from evaluation.evaluator_config import KING_VALUE

class King(Piece):
    def __init__(self, color, initial_position_index: int, 
                 kingside_rook: Rook, queenside_rook: Rook):
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
    
    def move_piece(self, new_position_index, white_board, black_board):
        if not self.can_still_castle:
            return super().move_piece(new_position_index, white_board, black_board)
        
        old_position = self.position_index
        self.position_index = new_position_index

        if self.color == COLOR_WHITE:
            if new_position_index == 6:
                white_board, black_board = self.moves_helper.move_piece(old_position, 6, white_board, black_board)
                return self.kingside_rook.move_piece(5, white_board, black_board)
            
            if new_position_index == 2:
                white_board, black_board = self.moves_helper.move_piece(old_position, 6, white_board, black_board)
                return self.queenside_rook.move_piece(3, white_board, black_board)
            
        else:
            if new_position_index == 62:
                white_board, black_board = self.moves_helper.move_piece(old_position, 62, white_board, black_board)
                return self.kingside_rook.move_piece(61, white_board, black_board)
            
            if new_position_index == 58:
                white_board, black_board = self.moves_helper.move_piece(old_position, 58, white_board, black_board)
                return self.queenside_rook.move_piece(59, white_board, black_board)

        self.can_still_castle = False
        return self.moves_helper.move_piece(old_position, new_position_index, black_board, white_board)

    def get_piece_value(self) -> int:
        return KING_VALUE