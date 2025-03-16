from CLI.board import *
from conf import *
from actions import *
from collections import Counter, deque
from objects.state import *
import copy

def breadth_first(board,i):
    initial_state = State(copy.deepcopy(board), i)
    horizon = [initial_state]  # Agregar el estado inicial a la frontera
    found, max_score, count, solution = breadth_first_search(horizon, 0, 0)
    sol = []
    if found:
        node = solution
        while node.parent is not None:
            sol.append(node.child_move)
            node = node.parent
        sol.reverse()
        print(f"Solution: {sol}")
        print(f"Nodes visited: {count}")
        print(f"Max Score: {max_score}")
    else:
        print(f"No solution found")
        print(f"Nodes visited: {count}")
    return sol,count,max_score

def breadth_first_search(horizon, nodes_visited, max_score):
    solution = None

    for state in horizon:
        nodes_visited += 1
        if state.parent!=None and state.parent.index_cake==len(LIST_CAKES)-1 and state.score > max_score:
            max_score = state.score
            solution = state

    if solution:  # Si encontramos solución, retornamos inmediatamente
        return True, max_score, nodes_visited, solution

    new_horizon = []
    for state in horizon:
        for movement in state.moves:
            new_board = copy.deepcopy(state.board)
            new_board, points = place_cake(new_board, state.next_cake, movement[0], movement[1])
            if state.index_cake==len(LIST_CAKES)-1:
                child= State(new_board, state.index_cake)
            else:
                child= State(new_board, state.index_cake + 1)
            child.parent = state  # Relación padre-hijo
            child.child_move = movement
            child.score = state.score + points
            #print(state.index_cake)
            new_horizon.append(child)

    if new_horizon:
        return breadth_first_search(new_horizon, nodes_visited, max_score)

    return False, max_score, nodes_visited, None