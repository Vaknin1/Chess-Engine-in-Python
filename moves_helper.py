import os

from constants import *
from colorama import Fore, Style

class MovesHelper:

    base_dir = os.path.dirname(os.path.abspath(__file__))

    BISHOP_CACHED_ALL_MOVES_PATH = os.path.join(base_dir, "chess_engine_all_moves/bishop")
    ROOK_CACHED_ALL_MOVES_PATH = os.path.join(base_dir, "chess_engine_all_moves/rook")
    KNIGHT_CACHED_ALL_MOVES_PATH = os.path.join(base_dir, "chess_engine_all_moves/knight")
    KING_CACHED_ALL_MOVES_PATH = os.path.join(base_dir, "chess_engine_all_moves/king")

    BISHOP_CACHED_BLOCKER_MOVES_PATH = os.path.join(base_dir, "chess_engine_blocker_moves/bishop")
    ROOK_CACHED_BLOCKER_MOVES_PATH = os.path.join(base_dir, "chess_engine_blocker_moves/rook")
    KNIGHT_CACHED_BLOCKER_MOVES_PATH = os.path.join(base_dir, "chess_engine_blocker_moves/knight")
    KING_CACHED_BLOCKER_MOVES_PATH = os.path.join(base_dir, "chess_engine_blocker_moves/king")

    LEFT_EDGE =   (1 << 0) | (1 << 8) | (1 << 16) | (1 << 24) | (1 << 32) | (1 << 40) | (1 << 48) | (1 << 56)
    RIGHT_EDGE =  (1 << 7) | (1 << 15) | (1 << 23) | (1 << 31) | (1 << 39) | (1 << 47) | (1 << 55) | (1 << 63)
    UPPEAR_LIMIT = 64
    LOWER_LIMIT = -1 

    _instance = None

    @staticmethod
    def _convert_lookups_into_dicts(folder_path: str, position_index: int) -> dict:
        data = {}

        with open(f"{folder_path}/{position_index}.txt", "r") as f:
            for line in f.readlines():
                line = line.strip("\n")

                blocker_variation, possible_moves = line.split(": ")
                data[blocker_variation] = possible_moves

        return data

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Create all moves dict data
            cls._instance.all_moves_data = {}
            for piece, path in [(BISHOP, MovesHelper.BISHOP_CACHED_ALL_MOVES_PATH),
                                (ROOK, MovesHelper.ROOK_CACHED_ALL_MOVES_PATH),
                                (KNIGHT, MovesHelper.KNIGHT_CACHED_ALL_MOVES_PATH),
                                (KING, MovesHelper.KING_CACHED_ALL_MOVES_PATH)]:

                cls._instance.all_moves_data[piece] = {}

                for pos in range(64):
                    cls._instance.all_moves_data[piece][pos] = MovesHelper._convert_lookups_into_dicts(path, pos)

            # Create blocker moves dict data
            cls._instance.blocker_moves_data = {}
            for piece, path in [(BISHOP, MovesHelper.BISHOP_CACHED_BLOCKER_MOVES_PATH),
                                (ROOK, MovesHelper.ROOK_CACHED_BLOCKER_MOVES_PATH)]:

                cls._instance.blocker_moves_data[piece] = {}

                for pos in range(64):
                    cls._instance.blocker_moves_data[piece][pos] = MovesHelper._convert_lookups_into_dicts(path, pos)

        return cls._instance

    # ------ REGULAR MOVES ------
    def get_legal_diagonal_moves(self, position_index: int, white_board: int, black_board: int, color) -> int:
        return self._get_legal_moves(BISHOP, position_index, white_board, black_board, color)

    def get_legal_horizontal_vertical_moves(self, position_index: int, white_board: int, black_board: int, color) -> int:
        return self._get_legal_moves(ROOK, position_index, white_board, black_board, color)

    def get_legal_L_moves(self, position_index: int, white_board: int, black_board: int, color) -> int:
        all_legal_moves = self.all_moves_data[KNIGHT][position_index]['0']
        all_legal_moves = int(all_legal_moves)

        # Remove friendly pieces from allowed moves
        if color == COLOR_WHITE:
            all_legal_moves = all_legal_moves & ~white_board
        else:
            all_legal_moves = all_legal_moves & ~black_board

        return all_legal_moves

    def get_legal_king_moves(self, position_index: int, white_board: int, black_board: int, color) -> int:
        all_legal_moves = self.all_moves_data[KING][position_index]['0']
        all_legal_moves = int(all_legal_moves)

        # Remove friendly pieces from allowed moves
        if color == COLOR_WHITE:
            all_legal_moves = all_legal_moves & ~white_board
        else:
            all_legal_moves = all_legal_moves & ~black_board

        return all_legal_moves

    def get_legal_pawn_moves(self, position_index: int, white_board: int, black_board: int, color) -> int:
        if color == COLOR_WHITE:
            return self._legal_pawn_moves(position_index, white_board, black_board, 
                                          position_index + 9, position_index + 7, position_index + 8)
        else:
            return self._legal_pawn_moves(position_index, black_board, white_board, 
                                          position_index - 7, position_index - 9, position_index - 8)

    # ------ HELPER MOVES ------
    def _legal_pawn_moves(self, position_index, own_board, enemy_board, 
                          right_step, left_step, forward_step):
        possible_moves = 0

        if not self._is_occupied((own_board | enemy_board), forward_step):
            possible_moves = possible_moves | (1 << forward_step)

        if not self._is_on_left_edge(position_index) and self._is_occupied(enemy_board, left_step):
            possible_moves = possible_moves | (1 << left_step)

        if not self._is_on_right_edge(position_index) and self._is_occupied(enemy_board, right_step):
            possible_moves = possible_moves | (1 << right_step)

        return possible_moves

    def _get_legal_moves(self, piece, position_index: int, white_board: int, black_board: int, color) -> int:
        """
            :param position_index: Position of the piece on the board
            :param white_board: White's board of pieces (bitboard of where white's pieces are)
            :param black_board: Black's board of pieces (bitboard of where black's pieces are)
            :param color: If player is playing white or black
            :return: list of possible moves
        """

        all_legal_moves = self.all_moves_data[piece][position_index]['0']
        all_legal_moves = int(all_legal_moves)
        blocker_variation = all_legal_moves & (white_board | black_board)

        if blocker_variation == 0:  # No blocking detected
            return all_legal_moves

        possible_moves = int(self.blocker_moves_data[piece][position_index][str(blocker_variation)])

        # Remove friendly pieces from allowed moves
        if color == COLOR_WHITE:
            possible_moves = possible_moves & ~white_board
        else:
            possible_moves = possible_moves & ~black_board

        return possible_moves

    # ------ ACTIONS ------
    def move_piece(self, position_index: int, new_position_index: int, own_board: int, enemy_board: int) -> (int, int):
        enemy_board = enemy_board & ~(1 << new_position_index)
        own_board = own_board & ~(1 << position_index)

        own_board = own_board | (1 << new_position_index)

        return own_board, enemy_board

    # ------ GENERAL HELPERS ------
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

if __name__ == '__main__':
    legal_moves = MovesHelper().get_legal_diagonal_moves(34, 0, 0, COLOR_WHITE)
    print_board(legal_moves)