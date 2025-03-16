import heapq
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from CLI.board import *
from conf import *
from actions import *
from collections import Counter, deque
from objects.state import *
from heuristics.heuristics import *
import copy


def heuristic_search(board,i, h):
    initial_state = State(copy.deepcopy(board), i)
    path, count, total_score = a_star_search(initial_state, h)

    return path, count, total_score

def a_star_search(initial_state, heu):
    priority_queue = []
    heapq.heappush(priority_queue, (0, 0, 0, initial_state, []))  # (Costo total, Costo g(n), Puntuación total, Estado, Camino)
    nodes_visited = 0
    visited_states = {}  # Diccionario para guardar el costo mínimo de cada estado

    while priority_queue:
        total_cost, g_cost, total_score, state, path = heapq.heappop(priority_queue)
        nodes_visited += 1
        try:
            # Convertir el tablero en un formato hashable (tuplas inmutables) para compararlo
            board_tuple = tuple(tuple(row) for row in state.board)
            if board_tuple in visited_states and visited_states[board_tuple] <= total_cost:
                continue  # Si ya visitamos este estado con un costo menor o igual, lo ignoramos
        except:
            return [], nodes_visited, 0
        visited_states[board_tuple] = total_cost  # Guardar el costo del estado actual

        if state.index_cake == len(LIST_CAKES) - 1:  # Asegurar que se coloca la última tarta
            for move in state.moves:
                new_board = copy.deepcopy(state.board)
                new_board, score = place_cake(new_board, state.next_cake, move[0], move[1])
                final_path = path + [move]
                final_score = total_score + score
                return final_path, nodes_visited, final_score

        for move in state.moves:
            new_board = copy.deepcopy(state.board)
            new_board, score = place_cake(new_board, state.next_cake, move[0], move[1])
            child = State(new_board, state.index_cake + 1)
            if not child.moves and child.index_cake < len(LIST_CAKES):
                continue  # Evitar estados sin movimientos válidos si faltan tartas por colocar
            h = h1(new_board) if heu == 1 else h2(new_board) if heu == 2 else h3(new_board)
            new_g_cost = g_cost + score  # Costo acumulado g(n)
            new_f_cost = new_g_cost + h  # f(n) = g(n) + h(n)
            new_total_score = total_score + score  # Acumular la puntuación obtenida

            heapq.heappush(priority_queue, (new_f_cost, new_g_cost, new_total_score, child, path + [move]))

    return [], nodes_visited, 0