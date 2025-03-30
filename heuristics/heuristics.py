
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from CLI.board import *
from conf import *
from objects.cake import Cake
import time
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



# Calculate execution time to extract it from the total execution of the program.

# num_tests = 10  # Número de pruebas por nivel
# levels = [1, 2, 3]  # Niveles a probar

# total_time_h1 = 0
# total_time_h2 = 0
# total_tests = 0

# for level in levels:
#     level_time_h1 = 0
#     level_time_h2 = 0

#     for _ in range(num_tests):
#         board = generate_board(level)

#         start = time.perf_counter()
#         h1(board)
#         end = time.perf_counter()
#         level_time_h1 += (end - start)

#         start = time.perf_counter()
#         h2(board)
#         end = time.perf_counter()
#         level_time_h2 += (end - start)

#     avg_h1 = level_time_h1 / num_tests
#     avg_h2 = level_time_h2 / num_tests

#     print(f"Level {level} - Average TIME h1: {avg_h1:.10f} sec")
#     print(f"Level {level} - Average TIME h2: {avg_h2:.10f} sec")

#     total_time_h1 += level_time_h1
#     total_time_h2 += level_time_h2
#     total_tests += num_tests

# # Cálculo de la media global
# global_avg_h1 = total_time_h1 / total_tests
# global_avg_h2 = total_time_h2 / total_tests

# print(f"Global Average TIME h1: {global_avg_h1:.10f} sec")
# print(f"Global Average TIME h2: {global_avg_h2:.10f} sec")