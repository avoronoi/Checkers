# 0 - empty, 1 - white man, 2 - black man, 3 - white king, 4 - black king
board = [
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 2, 0, 2, 0, 2],
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1]
]

# board = [
#     [2, 0, 2, 0, 2, 0, 2, 0],
#     [0, 2, 0, 2, 0, 2, 0, 2],
#     [2, 0, 2, 0, 0, 0, 2, 0],
#     [0, 0, 0, 2, 0, 0, 0, 0],
#     [0, 0, 1, 0, 0, 0, 0, 0],
#     [0, 1, 0, 0, 0, 1, 0, 1],
#     [1, 0, 1, 0, 1, 0, 1, 0],
#     [0, 1, 0, 1, 0, 1, 0, 1]
# ]
# print(can)

# maps colors to opponent's colors
opponent = {
    1: (2, 4),
    2: (1, 3),
    3: (2, 4),
    4: (1, 3)
}


class Man:
    def is_opponent(self, row, col):
        pass

    def must_capture(self):
        pass

    def can_move(self, row, col):
        pass

    def available_moves(self):
        pass


class King:
    def is_opponent(self, row, col):
        pass

    def must_capture(self):
        pass

    def can_move(self, row, col):
        pass

    def available_moves(self):
        pass


def in_bounds(row, col):
    return row >= 0 and row < len(board) and col >= 0 and col < len(board)


def must_capture(row, col):
    opp = opponent[board[row][col]]
    for dir_row, dir_col in (-1, -1), (-1, 1):
        if not in_bounds(row + 2 * dir_row, col + 2 * dir_col):
            continue
        if (board[row + dir_row][col + dir_col] in opp and 
                board[row + 2 * dir_row][col + 2 * dir_col] == 0):
            return True
    return False


def can_move(row_from, col_from, row_to, col_to):
    """Returns whether a move can be made, no matter if a piece must capture or not.
    """
    if abs(row_from - row_to) == 1:
        return board[row_to][col_to] == 0
    opp = opponent[board[row_from][col_from]] 
    return (board[(row_from + row_to) / 2][(col_from + col_to) / 2] in opp 
        and board[row_to][col_to] == 0)


def possible_moves(row, col):
    only_capture = must_capture(row, col)
    