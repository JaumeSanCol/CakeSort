import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import heapq
from CLI.board import *
from conf import *
from actions import *
from collections import Counter, deque
from objects.state import *
from heuristics.heuristics import *
import copy

def greedy_best_first(board,i, h):
    initial_state = State(copy.deepcopy(board), i)

    path, count, total_score = greedy_best_first_search(initial_state, h)

    return path, count, total_score

def greedy_best_first_search(initial_state, heu):
    priority_queue = []
    heapq.heappush(priority_queue, (0, 0, initial_state, []))  # (Heurística h(n), Puntuación total, Estado, Camino)
    nodes_visited = 0
    visited_states = set()  # Conjunto para rastrear estados visitados

    while priority_queue:
        h_cost, total_score, state, path = heapq.heappop(priority_queue)
        nodes_visited += 1
        try:
            # Convertir el tablero en un formato hashable (tuplas inmutables) para compararlo
            board_tuple = tuple(tuple(row) for row in state.board)
            if board_tuple in visited_states:
                continue  # Evitar reexplorar el mismo estado
        except:
            return [], nodes_visited, 0
        visited_states.add(board_tuple)

        if state.index_cake == len(LIST_CAKES) - 1:  # Verificar si se colocó la última tarta
            for move in state.moves:
                new_board = copy.deepcopy(state.board)
                new_board, score = place_cake(new_board, state.next_cake, move[0], move[1])
                final_path = path + [move]
                final_score = total_score + score
                return final_path, nodes_visited, final_score

        for move in state.moves:
            new_board = copy.deepcopy(state.board)
            new_board, score = place_cake(new_board, state.next_cake, move[0], move[1])

            # 🔹 Verificar si new_board es un diccionario (lo que causaría el error)
            if isinstance(new_board, dict):
                print(f"Error: new_board es un diccionario en el movimiento {move}")
                continue  # Saltar este movimiento inválido

            child = State(new_board, state.index_cake + 1)
            
            if not child.moves and child.index_cake < len(LIST_CAKES):
                continue  # Evitar estados sin movimientos válidos si faltan tartas por colocar

            h = h1(new_board) if heu == 1 else h2(new_board) if heu == 2 else h3(new_board)

            new_total_score = total_score + score  # Acumular la puntuación obtenida

            heapq.heappush(priority_queue, (h, new_total_score, child, path + [move]))

    print("No solution found.")
    return [], nodes_visited, 0  # Devolver lista vacía en lugar de False


#board= [[{"numbers": [2, 3, 2, 1, 1, 4], "main": [2, 1], "empty": 0}, 0, 0], [{"numbers": [3, 5, 2, 5, 0, 5], "main": [5], "empty": 1}, 0, 0], [{"numbers": [1, 4, 4, 1, 3, 1], "main": [1], "empty": 0}, 0, {"numbers": [4, 4, 1, 2, 1, 0], "main": [4, 1], "empty": 1}]]
#greedy_best_first(board,2, 1)