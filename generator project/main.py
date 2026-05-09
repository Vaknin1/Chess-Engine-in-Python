from colorama import Style, Fore
import os

class main:
    piece = "bishop"
    LEFT_EDGE = (1 << 0) | (1 << 8) | (1 << 16) | (1 << 24) | (1 << 32) | (1 << 40) | (1 << 48) | (1 << 56)
    RIGHT_EDGE = (1 << 7) | (1 << 15) | (1 << 23) | (1 << 31) | (1 << 39) | (1 << 47) | (1 << 55) | (1 << 63)
    UPPEAR_LIMIT = 64
    LOWER_LIMIT = -1

    def get_all_bishop_moves(self, position_index: int) -> int:
        bitboard_moves = 0

        # Do all upper moves
        for i in range(position_index + 8, self.UPPEAR_LIMIT, +8):
            bitboard_moves = bitboard_moves | (1 << i)

        # Do all lower moves
        for i in range(position_index - 8, self.LOWER_LIMIT, -8):
            bitboard_moves = bitboard_moves | (1 << i)

        # Do all right moves
        if not self._is_on_right_edge(position_index):
            i = 1
            while True:
                bitboard_moves = bitboard_moves | (1 << position_index + i)
                if self._is_on_right_edge(position_index + i):
                    break
                i = i + 1

        # Do all left moves
        if not self._is_on_left_edge(position_index):
            i = 1
            while True:
                bitboard_moves = bitboard_moves | (1 << position_index - i)
                if self._is_on_left_edge(position_index - i):
                    break
                i = i + 1

        return bitboard_moves

    def remove_square(self, bitboard, square_index):
        # 1. Create a bitboard with only the target square set: (1 << square_index)
        # 2. Invert it (~): All bits become 1, target becomes 0
        # 3. AND it with the original bitboard
        return bitboard & ~(1 << square_index)



    # THE KEYS INSIDE THE BLOCKERS LOOKUP TABLE
    # @generic
    def get_all_blocking_variations(self, bitboard_moves: int) -> list:
        blocking_variations = []
        bitboard_mapper = self.get_bitboard_mapper(bitboard_moves)
        possible_squares_amount = len(bitboard_mapper.keys())

        for i in range(2**possible_squares_amount):
            variation = 0
            for j in range(possible_squares_amount):
                if (i>>j & 1) > 0:
                    variation = variation + bitboard_mapper[j]

            if variation != 0:
                blocking_variations.append(variation)

        return blocking_variations

    def get_possible_moves_with_blockers(self, position_index: int, blocking_variation: int):
        bitboard_moves = 0

        # Do all upper moves
        for i in range(position_index + 8, self.UPPEAR_LIMIT, +8):
            bitboard_moves = bitboard_moves | (1 << i)
            if self._is_occupied(blocking_variation, i):
                break

        # Do all lower moves
        for i in range(position_index - 8, self.LOWER_LIMIT, -8):
            bitboard_moves = bitboard_moves | (1 << i)
            if self._is_occupied(blocking_variation, i):
                break

        # Do all right moves
        if not self._is_on_right_edge(position_index):
            i = 1
            while True:
                bitboard_moves = bitboard_moves | (1 << position_index + i)
                if self._is_occupied(blocking_variation, position_index + i) or self._is_on_right_edge(position_index + i):
                    break
                i = i + 1

        # Do all left moves
        if not self._is_on_left_edge(position_index):
            i = 1
            while True:
                bitboard_moves = bitboard_moves | (1 << position_index - i)
                if self._is_occupied(blocking_variation, position_index - i) or self._is_on_left_edge(position_index - i):
                    break
                i = i + 1

        return bitboard_moves

    def _is_occupied(self, blocking_variation, position_index: int):
        if (blocking_variation >> position_index & 1) > 0:
            return True
        return False

    def get_bitboard_mapper(self, bitboard):
        index_count = 0
        n_count = 0
        mapper = {}

        while bitboard != 0:
            if (bitboard & 1) > 0:
                mapper[index_count] = 2 ** n_count
                index_count = index_count + 1
            bitboard = bitboard >> 1
            n_count = n_count + 1

        return mapper

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

# board = main().get_all_bishop_moves(47)
# print_board(board)


# index = 27

# all_moves = main().get_all_king_moves(index)
# print_board(all_moves)
#
# blocking_variations = main().get_all_blocking_variations(all_moves)
# pm = main().get_possible_moves_with_blockers(index, blocking_variations[0])
# print_board(pm)
#
m = main()


for i in range(64):
    all_moves = m.get_all_bishop_moves(i)

    with open(f"{i}.txt", "w") as f:

        f.write(f"0: {all_moves}\n")


# for i in range(64):
#     all_moves = m.get_all_plus_moves(i)
#     blocking_variations = m.get_all_blocking_variations(all_moves)
#
#     with open(f"{i}.txt", "w") as f:
#         for variation in blocking_variations:
#             print(f"[{i}] Blocking variation: {variation}", end=" ")
#             possible_moves = m.get_possible_moves_with_blockers(i, variation)
#             print(f"Possible moves: {possible_moves}")
#
#             f.write(f"{variation}: {possible_moves}\n")