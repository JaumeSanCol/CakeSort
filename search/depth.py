from CLI.board import *
from conf import *
from actions import *
from objects.state import *
import copy

def depth_first(board,i):
    initial_state=State(copy.deepcopy(board),i)
    nodes_visited = 0
    score=0
    sol=[]
    found,count=depth_first_search(initial_state,nodes_visited)
    if found:
        sol = []
        node = initial_state
        while node.child is not None:
            sol.append(node.child_move)
            node = node.child

        if node.child_move:  # Asegurar que el último movimiento también se agrega
            sol.append(node.child_move)
        score=node.score

    return sol,count,score

        
# Función para realizar búsqueda en profundidad (DFS)
def depth_first_search(state,nodes_visited): # Se agrega el nivel de profundidad
    
    for movement in state.moves:
        nodes_visited+=1
        if state.index_cake==len(LIST_CAKES)-1:
            state.child_move=movement
            new_board = copy.deepcopy(state.board)  
            new_board, points= place_cake(new_board, state.next_cake, movement[0], movement[1])
            child=State(new_board,state.index_cake)
            state.child=child
            state.child_move=movement
            state.score=points
            return True, nodes_visited
        else: # Crear una copia antes de modificarla
            new_board = copy.deepcopy(state.board)  
            new_board, points = place_cake(new_board, state.next_cake, movement[0], movement[1])

            child=State(new_board,state.index_cake+1)
            state.child=child
            state.child_move=movement
            found,nodes_visited=depth_first_search(child,nodes_visited)
            if found:
                #print(state.child_move)
                #print(state.moves)
                #print_board(state.board)
                
                return True,nodes_visited
    state.child=None
    return False, nodes_visited
