
from objects.cake import *
from conf import *
from .clean import clean_screen

from copy import deepcopy

def generate_board(level):
    # Initialize the board with empty values (0)
    board = [[0] * COLS for _ in range(ROWS)]
    # Add a cake at the top-left corner
    board[0][0] = deepcopy(LIST_CAKES[4])

    if 2<= level <=3:
        # Add a cake at the bottom-right corner
        board[ROWS - 1][COLS - 1] = deepcopy(LIST_CAKES[5])
       
    
    if level == 3:
        # Add a cake to the left of the center position
         # Add a cake at the center of the board
        board[ROWS // 2][COLS // 2] = deepcopy(LIST_CAKES[2])
        board[ROWS // 2 + 1][COLS // 2 - 1] = deepcopy(LIST_CAKES[3])
    
    return board

def obtain_pos_movs(board):
    pos_movs = []
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == 0:
                pos_movs.append((r, c))
    return pos_movs

def print_board(board):
    clean_screen()
    rows, cols = len(board), len(board[0])
    border = "+" + "-----+" * cols
    print(border)
    for r in range(rows):
        top_border = "|"  # Línea superior dentro de la celda
        top_row = "|"
        middle_row = "|"
        bottom_row = "|"
        for c in range(cols):
            if isinstance(board[r][c], Cake):
                nums = board[r][c].numbers
                top_border += "+-+-+|"
                top_row += f"|{' ' if nums[0] == 0 else nums[0]}|{' ' if nums[1] == 0 else nums[1]}||"
                middle_row += f"|{' ' if nums[2] == 0 else nums[2]}|{' ' if nums[3] == 0 else nums[3]}||"
                bottom_row += f"|{' ' if nums[4] == 0 else nums[4]}|{' ' if nums[5] == 0 else nums[5]}||"
            else:
                top_border += "     |"
                top_row += "     |"
                middle_row += "     |"
                bottom_row += "     |"
        print(top_border)
        print(top_row)
        print(middle_row)
        print(bottom_row)
        print(top_border)
        print(border)

def print_next_cake(index):
    print(f'''
       +-+-+
       |{' ' if LIST_CAKES[index].numbers[0] == 0 else LIST_CAKES[index].numbers[0]}|{' ' if LIST_CAKES[index].numbers[1] == 0 else LIST_CAKES[index].numbers[1]}|
       |{' ' if LIST_CAKES[index].numbers[2] == 0 else LIST_CAKES[index].numbers[2]}|{' ' if LIST_CAKES[index].numbers[3] == 0 else LIST_CAKES[index].numbers[3]}|
       |{' ' if LIST_CAKES[index].numbers[4] == 0 else LIST_CAKES[index].numbers[4]}|{' ' if LIST_CAKES[index].numbers[5] == 0 else LIST_CAKES[index].numbers[5]}|
       +-+-+
''')
    



