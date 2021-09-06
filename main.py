import tkinter as tk
import logic


# 0 - empty, 1 - white, 2 - black
BOARD_NUM = [
    [0, 2, 0, 2, 0, 2, 0, 2],
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 2, 0, 2, 0, 2],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0]
]
logic.init_board(BOARD_NUM)


BOARD_SIZE = len(BOARD_NUM)
CELL_SIZE = 80
WHITE_CELL = '#ececd0'
BLACK_CELL = '#779557'
SELECTED_CELL = '#Bab867'
# the first value is for a non-captured piece, the second value is for captured
WHITE_PIECE = ('#f9f9f9', '#CAD5BE')
BLACK_PIECE = ('#595451', '#697754')
WHITE_OUTLINE = '#585451'
BLACK_OUTLINE = '#3a3a31'
WHITE_CELL_MOVE = '#d6d6bd'
BLACK_CELL_MOVE = '#69874e'


selected_moves = []
selected_cell = None
# 1 if white has to make the move else 2
turn = 1
captured_pieces = []
# None if the move is over otherwise the coordinates of a cell to continue the move
piece_to_continue = None


class CnvCell(tk.Canvas):
    def __init__(self, piece, row, col, **kwargs):
        super().__init__(**kwargs)
        self.row, self.col = row, col
        self.initUI(piece)

    def initUI(self, piece):
        if piece:
            captured = (self.row, self.col) in captured_pieces
            self.create_oval(
                CELL_SIZE * 0.1, CELL_SIZE * 0.1, 
                CELL_SIZE * 0.9, CELL_SIZE * 0.9,
                fill=(WHITE_PIECE[captured] if piece.color == 1
                      else BLACK_PIECE[captured]),
                outline=WHITE_OUTLINE if piece.color == 1 else BLACK_OUTLINE,
                width=3,
)
        if (self.row, self.col) in selected_moves:
            self.create_oval(
                CELL_SIZE * 0.33, CELL_SIZE * 0.33,
                CELL_SIZE * 0.67, CELL_SIZE * 0.67,
                fill=(WHITE_CELL_MOVE if (self.row + self.col) % 2 == 0 
                      else BLACK_CELL_MOVE),
                outline='')


class FrmBoard(tk.Frame):
    def __init__(self):
        super().__init__(master=window, width=BOARD_SIZE*CELL_SIZE,
                         height=BOARD_SIZE*CELL_SIZE)
        self.pack()
        self.draw()

    def draw(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                cnv_cell = CnvCell(
                    logic.board[i][j], i, j, master=self,
                    width=CELL_SIZE, height=CELL_SIZE, highlightthickness=0,
                    bg=(SELECTED_CELL if selected_cell == (i, j) 
                        else WHITE_CELL if (i + j) % 2 == 0 else BLACK_CELL))
                cnv_cell.bind('<Button-1>', click_cell)
                cnv_cell.place(x=j*CELL_SIZE, y=i*CELL_SIZE)


def deselect():
    if piece_to_continue is not None:
        return
    global selected_cell
    global selected_moves
    selected_cell = None
    selected_moves = []
    redraw()


def select(row, col):
    if piece_to_continue is not None and piece_to_continue != (row, col):
        return
    global selected_cell
    global selected_moves
    selected_cell = (row, col)
    selected_moves = logic.board[row][col].available_moves()
    redraw()


def move(row_from, col_from, row_to, col_to):
    captured_piece, change_turn = logic.board[row_from][col_from].move_to(row_to, col_to)
    global turn
    global piece_to_continue
    global captured_pieces
    if captured_piece is not None:
        captured_pieces.append(captured_piece)
        redraw()
    print(captured_pieces)
    if change_turn:
        for x, y in captured_pieces:
            logic.board[x][y] = None
        redraw()
        turn = 3 - turn
        piece_to_continue = None
        captured_pieces = []
    else:
        piece_to_continue = (row_to, col_to)
        select(row_to, col_to)


def click_cell(event):
    row, col = event.widget.row, event.widget.col
    if (row + col) % 2 == 0:
        deselect()
        return
    
    if logic.board[row][col] is None:
        if (row, col) in selected_moves:
            move(selected_cell[0], selected_cell[1], row, col)
        deselect()
        return
    
    if logic.board[row][col].color == turn:
        select(row, col)
    else:
        deselect()


def redraw():
    global frm_board
    frm_board.destroy()
    frm_board = FrmBoard()


window = tk.Tk()
frm_board = FrmBoard()
window.mainloop()