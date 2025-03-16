from CLI.board import obtain_pos_movs
from conf import *
from objects.cake import Cake
# heuristic based on the number of filled cells
def h1(board):
    return ROWS*COLS-len(obtain_pos_movs(board))

# heuristic based on the number of cakes that are surrounded/blocked
def h2(board):
    isolated_cakes = 0

    for i in range(ROWS):
        for j in range(COLS):
            cell=board[i][j]
            if isinstance(cell, Cake):
                # Revisar si hay un 0 en las posiciones adyacentes
                neighbors = [
                    (i-1, j), (i+1, j),  # Arriba y abajo
                    (i, j-1), (i, j+1)   # Izquierda y derecha
                ]
                if any(0 <= x < ROWS and 0 <= y < COLS and board[x][y] == 0 for x, y in neighbors):
                    continue  # No es un cake aislado
                isolated_cakes += 1

    return isolated_cakes

def h3(board):
    return len(obtain_pos_movs(board))