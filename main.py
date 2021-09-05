import logic
import tkinter as tk

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
WHITE_PIECE = '#f9f9f9'
BLACK_PIECE = '#595451'
WHITE_OUTLINE = '#585451'
BLACK_OUTLINE = '#3a3a31'
WHITE_CELL_MOVE = '#d6d6bd'
BLACK_CELL_MOVE = '#69874e'

selected_moves = []


class CnvCell(tk.Canvas):
    def __init__(self, piece, row, col, **kwargs):
        super().__init__(**kwargs)
        self.row, self.col = row, col
        self.initUI(piece)

    def initUI(self, piece):
        if piece:
            self.create_oval(
                CELL_SIZE * 0.1, CELL_SIZE * 0.1, 
                CELL_SIZE * 0.9, CELL_SIZE * 0.9,
                fill=WHITE_PIECE if piece.color == 1 else BLACK_PIECE,
                outline=WHITE_OUTLINE if piece.color == 1 else BLACK_OUTLINE, width=3)
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
                    bg=WHITE_CELL if (i + j) % 2 == 0 else BLACK_CELL)
                cnv_cell.bind('<Button-1>', cell_click)
                cnv_cell.place(x=j*CELL_SIZE, y=i*CELL_SIZE)


def cell_click(event):
    row, col = event.widget.row, event.widget.col
    print('Cell Clicked: ', row, col)


def redraw():
    global frm_board
    frm_board.destroy()
    frm_board = FrmBoard()


window = tk.Tk()
frm_board = FrmBoard()
window.bind('<Key>', lambda _: redraw())
window.mainloop()