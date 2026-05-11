from Pieces.piece import Piece


class King(Piece):
    def __init__(self, color, initial_position_index: int):
        super().__init__(color, initial_position_index)

