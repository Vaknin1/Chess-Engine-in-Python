from constants import *

class MovesHelper:
    BISHOP_CACHED_ALL_MOVES_PATH = "chess_engine_all_moves/bishop"
    ROOK_CACHED_ALL_MOVES_PATH = "chess_engine_all_moves/rook"
    KNIGHT_CACHED_ALL_MOVES_PATH = "chess_engine_all_moves/knight"
    KING_CACHED_ALL_MOVES_PATH = "chess_engine_all_moves/king"

    BISHOP_CACHED_BLOCKER_MOVES_PATH = "chess_engine_blocker_moves/bishop"
    ROOK_CACHED_BLOCKER_MOVES_PATH = "chess_engine_blocker_moves/rook"
    KNIGHT_CACHED_BLOCKER_MOVES_PATH = "chess_engine_blocker_moves/knight"
    KING_CACHED_BLOCKER_MOVES_PATH = "chess_engine_blocker_moves/king"

    _instance = None

    @staticmethod
    def convert_lookups_into_dicts(folder_path: str, position_index: int) -> dict:
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
                    cls._instance.all_moves_data[piece][pos] = MovesHelper.convert_lookups_into_dicts(path, pos)

            # Create blocker moves dict data
            cls._instance.blocker_moves_data = {}
            for piece, path in [(BISHOP, MovesHelper.BISHOP_CACHED_BLOCKER_MOVES_PATH),
                                (ROOK, MovesHelper.ROOK_CACHED_BLOCKER_MOVES_PATH)]:

                cls._instance.blocker_moves_data[piece] = {}

                for pos in range(64):
                    cls._instance.blocker_moves_data[piece][pos] = MovesHelper.convert_lookups_into_dicts(path, pos)

        return cls._instance


    def get_legal_diagonal_moves(self, position_index: int, white_board: int, black_board: int, color) -> list:
        """
        :param position_index: Position of the piece on the board
        :param white_board: White's board of pieces (bitboard of where white's pieces are)
        :param black_board: Black's board of pieces (bitboard of where black's pieces are)
        :param color: If player is playing white or black
        :return: list of possible moves
        """
        all_legal_moves = self.all_moves_data[BISHOP][position_index]
