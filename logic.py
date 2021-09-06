board = None
def init_board(board_num):
    global board
    board = [[(None if board_num[i][j] == 0 else Man(i, j, board_num[i][j]))
              for j in range(len(board_num))]
             for i in range(len(board_num))]


def in_bounds(row, col):
    return row >= 0 and row < len(board) and col >= 0 and col < len(board)


def is_empty(row, col):
    return board[row][col] is None


def print_board():
    for row in board:
        for cell in row:
            if cell:
                print((('W' if cell.color == 1 else 'B') + 
                       ('M' if isinstance(cell, Man) else 'K')), end=' ')
            else:
                print('O ', end=' ')
        print()


class Piece:
    def __init__(self, row, col, color, captured_pieces=None):
        """Color is 1 for white pieces and 2 for black pieces.
        """
        self.row, self.col, self.color = row, col, color
        self.captured_pieces = ([] if captured_pieces is None 
                                else captured_pieces)

    def is_opponent(self, row, col):
        return not is_empty(row, col) and self.color != board[row][col].color


class Man(Piece):
    def __can_move_to(self, row_to, col_to):
        """Returns whether a move can be made, no matter if a piece must capture or not.
        """
        if (not in_bounds(row_to, col_to) or not is_empty(row_to, col_to)
                or abs(self.row - row_to) != abs(self.col - col_to)
                or abs(self.row - row_to) > 2):
            return False
        if abs(self.row - row_to) == 1:
            return ((self.color == 1 and self.row > row_to) 
                    or (self.color == 2 and self.row < row_to))  
        captured_cell = ((self.row + row_to) // 2, (self.col + col_to) // 2)
        return (self.is_opponent(*captured_cell)
                and captured_cell not in self.captured_pieces)

    def __captured_piece(self, row_to, col_to):
        if abs(self.row - row_to) == 2:
            return ((self.row + row_to) // 2, (self.col + col_to) // 2)
        return None

    def capturing_moves(self):
        moves = []
        for x, y in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            if self.__can_move_to(self.row + x, self.col + y):
                moves.append((self.row + x, self.col + y))
        return moves

    def available_moves(self):
        for row in board:
            for cell in row:
                if (cell is not None and cell.color == self.color 
                        and cell.capturing_moves()):
                    return self.capturing_moves()
        direction = -1 if self.color == 1 else 1
        return [(self.row + x, self.col + y) 
                for x, y in [(direction, -1), (direction, 1)]
                if self.__can_move_to(self.row + x, self.col + y)]

    def move_to(self, row_to, col_to):
        """Moves the piece to (row_to, col_to) and returns 1) the coordinate of the captured cell or None if no cell was captured; 2) whether the turn has to be switched after the move.
        """
        result = self.__captured_piece(row_to, col_to)
        if result:
            self.captured_pieces.append(result)
        
        if ((row_to == 0 and self.color == 1)
                or (row_to == len(board) - 1 and self.color == 2)):
            board[row_to][col_to] = King(
                row_to, col_to, self.color, self.captured_pieces)
        else:
            board[row_to][col_to] = Man(
                row_to, col_to, self.color, self.captured_pieces)
        board[self.row][self.col] = None
        if result is None or not board[row_to][col_to].capturing_moves():
            board[row_to][col_to].captured_pieces = []
            return result, True
        return result, False


class King(Piece):
    def __pieces_on_way(self, row_to, col_to):
        """Returns the number of own and opponent's pieces on the way to destination in the format of tuple. Returns (-1, -1) if one of the pieces on the way was already captured.
        """
        x = 1 if row_to - self.row > 0 else -1
        y = 1 if col_to - self.col > 0 else -1
        own_on_way, opps_on_way = 0, 0
        for i, j in zip(range(self.row + x, row_to, x), 
                        range(self.col + y, col_to, y)):
            if (i, j) in self.captured_pieces:
                return (-1, -1)
            own_on_way += not is_empty(i, j) and not self.is_opponent(i, j)
            opps_on_way += not is_empty(i, j) and self.is_opponent(i, j)
        return own_on_way, opps_on_way

    def __captured_piece(self, row_to, col_to):
        x = 1 if row_to - self.row > 0 else -1
        y = 1 if col_to - self.col > 0 else -1
        for i, j in zip(range(self.row + x, row_to, x), 
                        range(self.col + y, col_to, y)):
            if board[i][j] is not None:
                return (i, j)
        return None

    def __same_diagonal(self):
        """Returns the list of cells that share the same diagonal with the piece.
        """
        cells = []
        for x, y in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            cur_row = self.row + x
            cur_col = self.col + y
            while in_bounds(cur_row, cur_col):
                cells.append((cur_row, cur_col))
                cur_row += x
                cur_col += y
        return cells

    def capturing_moves(self):
        return [cell for cell in self.__same_diagonal()
            if self.__pieces_on_way(*cell) == (0, 1) and is_empty(*cell)]

    def available_moves(self):
        for row in board:
            for cell in row:
                if (cell is not None and cell.color == self.color 
                        and cell.capturing_moves()):
                    return self.capturing_moves()
        return [cell for cell in self.__same_diagonal()
                if self.__pieces_on_way(*cell) == (0, 0) and is_empty(*cell)]

    def move_to(self, row_to, col_to):
        """Moves the piece to (row_to, col_to) and returns 1) the coordinate of the captured cell or None if no cell was captured; 2) whether the turn has to be switched after the move.
        """
        result = self.__captured_piece(row_to, col_to)
        if result:
            self.captured_pieces.append(result)
        
        board[row_to][col_to] = King(
            row_to, col_to, self.color, self.captured_pieces)
        board[self.row][self.col] = None
        if not board[row_to][col_to].capturing_moves():
            board[row_to][col_to].captured_pieces = []
            return result, True
        return result, False
