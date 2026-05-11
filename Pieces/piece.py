from constants import *
from moves_helper import MovesHelper

class Piece:
    def __init__(self, color, initial_position_index: int):
        self.color = color
        self.position_index = initial_position_index
        self.moves_helper = MovesHelper()

    def get_all_legal_moves(self, white_board: int, black_board: int):
        raise NotImplementedError

    def get_all_possible_captures(self, all_legal_moves: int, white_board: int, black_board: int):
        if self.color == COLOR_WHITE:
            return all_legal_moves & black_board

        return all_legal_moves & white_board

    def move_piece(self, new_position_index: int, white_board: int, black_board: int) -> (int, int):
        self.position_index = new_position_index

        if self.color == COLOR_WHITE:
            return self.moves_helper.move_piece(self.position_index, new_position_index, white_board, black_board)

        return self.moves_helper.move_piece(self.position_index, new_position_index, black_board, white_board)