# 1 if player at the top is white else 2
OPPONENT = 2


def in_bounds(row, col):
    return row >= 0 and row < len(board) and col >= 0 and col < len(board)


def is_empty(row, col):
    return board[row][col] is None


class Piece:
    def __init__(self, row, col, color):
        """Color is 1 for white pieces and 2 for black pieces
        """
        self.row, self.col, self.color = row, col, color

    def is_opponent(self, row, col):
        return not is_empty(row, col) and self.color != board[row][col].color


class Man(Piece):
    def can_move_to(self, row_to, col_to):
        """Returns whether a move can be made, no matter if a piece must capture or not.
        """
        if (not in_bounds(row_to, col_to) or not is_empty(row_to, col_to)
                or abs(self.row - row_to) != abs(self.col - col_to)
                or abs(self.row - row_to) > 2):
            return False
        if abs(self.row - row_to) == 1:
            return self.row > row_to
        return self.is_opponent(
            (self.row + row_to) // 2, (self.col + col_to) // 2)

    def must_capture(self):
        for x, y in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            if self.can_move_to(self.row + x, self.col + y):
                return True
        return False

    def available_moves(self):
        directions = (
            [(-2, -2), (-2, 2), (2, -2), (2, 2)] if self.must_capture()
            else [(-1, -1), (-1, 1)])
        return [(self.row + x, self.col + y) for x, y in directions 
            if self.can_move_to(self.row + x, self.col + y)]


class King(Piece):
    def can_move_to(self, row_to, col_to):
        """Returns whether a move can be made, no matter if a piece must capture or not.
        """
        if (not in_bounds(row_to, col_to) or not is_empty(row_to, col_to)
                or abs(self.row - row_to) != abs(self.col - col_to)):
            return False
        x = 1 if row_to - self.row > 0 else -1 
        y = 1 if col_to - self.col > 0 else -1
        own_on_way, opps_on_way = 0, 0
        for i, j in zip(range(self.row + x, row_to, x), 
                        range(self.col + y, col_to, y)):
            own_on_way += not is_empty(i, j) and not self.is_opponent(i, j)
            opps_on_way += not is_empty(i, j) and self.is_opponent(i, j)
        return own_on_way == 0 and opps_on_way <= 1

    def must_capture(self):
        pass

    def available_moves(self):
        pass


# 0 - empty, 1 - white man, 2 - black man, 3 - white king, 4 - black king
board_num = [
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 2, 0, 2, 0, 2],
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1]
]
board = []
for i, row in enumerate(board_num):
    board.append([(None if x == 0 else Man(i, j, x)) for j, x in enumerate(row)])
