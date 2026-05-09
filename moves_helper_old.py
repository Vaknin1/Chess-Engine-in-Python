from colorama import Fore, Style
from constants import *

class MovesHelperOld:
    LEFT_EDGE =   (1 << 0) | (1 << 8) | (1 << 16) | (1 << 24) | (1 << 32) | (1 << 40) | (1 << 48) | (1 << 56)
    RIGHT_EDGE =  (1 << 7) | (1 << 15) | (1 << 23) | (1 << 31) | (1 << 39) | (1 << 47) | (1 << 55) | (1 << 63)
    UPPEAR_LIMIT = 64
    LOWER_LIMIT = -1

    def get_legal_diagonal_moves(self, white_board: int, black_board: int, position_index: int) -> int:
        bitboard_moves = 0

        # Do all right upper side moves
        for i in range(position_index+9, self.UPPEAR_LIMIT, 9):
            if self._is_on_left_edge(i):
                break

            if self._is_occupied(white_board, i):
            bitboard_moves = bitboard_moves | (1 << i)
            if self._is_occupied(board_map, i):
                break

        # Do all left lower side moves
        for i in range(position_index - 9, self.LOWER_LIMIT, -9):
            if self._is_on_right_edge(i):
                break
            bitboard_moves = bitboard_moves | (1 << i)
            if self._is_occupied(board_map, i):
                break

        # Do all right lower moves
        for i in range(position_index - 7, self.LOWER_LIMIT, -7):
            if self._is_on_left_edge(i):
                break
            bitboard_moves = bitboard_moves | (1 << i)
            if self._is_occupied(board_map, i):
                break

        # Do all left upper moves
        for i in range(position_index + 7, self.UPPEAR_LIMIT, +7):
            if self._is_on_right_edge(i):
                break
            bitboard_moves = bitboard_moves | (1 << i)
            if self._is_occupied(board_map, i):
                break

        return bitboard_moves

    def get_legal_horizontal_vertical_moves(self, board_map: int, position_index: int) -> int:
        bitboard_moves = 0

        # Do all upper moves
        for i in range(position_index + 8, self.UPPEAR_LIMIT, +8):
            bitboard_moves = bitboard_moves | (1 << i)
            if self._is_occupied(board_map, i):
                break

        # Do all lower moves
        for i in range(position_index - 8, self.LOWER_LIMIT, -8):
            bitboard_moves = bitboard_moves | (1 << i)
            if self._is_occupied(board_map, i):
                break

        # Do all right moves
        if not self._is_on_right_edge(position_index):
            i = 1
            while True:
                bitboard_moves = bitboard_moves | (1 << position_index+i)
                if self._is_occupied(board_map, position_index+i) or self._is_on_right_edge(position_index+i):
                    break
                i = i + 1

        # Do all left moves
        if not self._is_on_left_edge(position_index):
            i = 1
            while True:
                bitboard_moves = bitboard_moves | (1 << position_index - i)
                if self._is_occupied(board_map, position_index - i) or self._is_on_left_edge(position_index - i):
                    break
                i = i + 1

        return bitboard_moves

    def get_legal_L_moves(self, board_map: int, position_index: int) -> int:
        bitboard_moves = 0

        # LEFT
        if not self._is_on_left_edge(position_index):
            if not self._is_on_left_edge(position_index-1):
                if position_index + 6 < self.UPPEAR_LIMIT:
                    bitboard_moves = bitboard_moves | (1 << position_index + 6)
                if position_index - 10 > self.LOWER_LIMIT:
                    bitboard_moves = bitboard_moves | (1 << position_index - 10)

            if position_index + 15 < self.UPPEAR_LIMIT:
                bitboard_moves = bitboard_moves | (1 << position_index + 15)
            if position_index - 17 > self.LOWER_LIMIT:
                bitboard_moves = bitboard_moves | (1 << position_index - 17)

        # RIGHT
        if not self._is_on_right_edge(position_index):
            if not self._is_on_right_edge(position_index+1):
                if position_index + 10 < self.UPPEAR_LIMIT:
                    bitboard_moves = bitboard_moves | (1 << position_index + 10)
                if position_index - 6 > self.LOWER_LIMIT:
                    bitboard_moves = bitboard_moves | (1 << position_index - 6)

            if position_index + 17 < self.UPPEAR_LIMIT:
                bitboard_moves = bitboard_moves | (1 << position_index + 17)
            if position_index - 15 > self.LOWER_LIMIT:
                bitboard_moves = bitboard_moves | (1 << position_index - 15)

        return bitboard_moves

    def get_legal_pawn_moves(self, board_map: int, position_index: int, color: int) -> int:
        bitboard_moves = 0

        if color == COLOR_WHITE:
            assert position_index + 8 >= self.UPPEAR_LIMIT, \
                f"Attempted to move a pawn who should be promoted. pawn index is: {position_index}"

            if not self._is_occupied(board_map, position_index + 8):
                bitboard_moves = bitboard_moves | (1 << position_index + 8)

            if


    def _is_occupied(self,  board_map: int, position_index: int) -> bool:
        return (board_map >> position_index & 1) > 0

    def _is_on_right_edge(self, position_index: int) -> bool:
        return (self.RIGHT_EDGE & (1 << position_index)) > 0

    def _is_on_left_edge(self, position_index: int) -> bool:
        return (self.LEFT_EDGE & (1 << position_index)) > 0



def print_board(board):
    for row in range(7, -1, -1):
        for col in range(8):
            bit = (board >> (row * 8 + col)) & 1
            if bit:
                print(Fore.GREEN + "1" + Style.RESET_ALL, end=" ")
            else:
                print("0", end=" ")
        print()

print_board(MovesHelper().get_legal_horizontal_vertical_moves(0,35))
