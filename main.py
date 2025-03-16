from objects.cake import *
from CLI.board import *
from CLI.print_menu import *
from actions import *
from save import *
import time

from search.depth import *
from search.heuS import *
from search.breadth import *
from search.greedy import *





def ask_for_hint(board,i):
    #its fast in all levels and even though it will not give the best move, it won't make the user lose.
    sol,count,new_score=depth_first(deepcopy(board),i)
    if sol==[]:print(f"HINT: It's too late my friend")
    else:
        print(f"HINT:{sol[0]}")






try:
    player_type,board,level,i,score=main_menu()
except:
    player_type=False

if not player_type:
    print("bye")

elif player_type=="Player":
    while True:
        
        print_board(board)
        if i<len(LIST_CAKES):
            print_next_cake(i)
        else:
            print("WINNER")
            break
        print(f"POSSIBLE MOVES: {obtain_pos_movs(board)}")
        print(f"CAKES LEFT:{len(LIST_CAKES)-i}")
        print(f"SCORE: {score}")
        selection = input("row,col >").strip().lower()
        if selection=="esc": 
            save=ask_save_board()
            if save==1:
                save_game_state(board, i, score,ROWS,COLS)
            break
        if selection =="hint": 
            ask_for_hint(board,i)
            selection = input("row,col >").strip().lower()
        try:
            row,col=selection.split(",")
            row,col=int(row),int(col)
            board,points=place_cake(board,LIST_CAKES[i],int(row),int(col))
            score+=points
            i=i+1
        except:
            pass
        
        moves=obtain_pos_movs(board)
        if moves==[] and i<len(LIST_CAKES):
            print("RUN OUT OF SPACE")
            break

    print_stats_pl(score)
else:
    key=f"{player_type}/{level}/{ROWS}/{COLS}"
    start = time.perf_counter()
    if key in history:print(f"\n   Loading ... (estimated: {history[key]}s)")
    else: print(f"\n   Loading ...\n")
    if player_type=="Depth First Search":
        sol,count,new_score=depth_first(board,i)
    elif player_type=="Breadth First Search":
        sol,count,new_score=breadth_first(board,i)
    elif player_type=="A* heurstic 1":
        sol,count,new_score=heuristic_search(board,i,1)
    elif player_type=="A* heuristic 2":
        sol,count,new_score=heuristic_search(board,i,2)
    elif player_type=="GS heuristic 1":
        sol,count,new_score=greedy_best_first(board,i,1)
    elif player_type=="GS heuristic 2":
        sol,count,new_score=greedy_best_first(board,i,2)
    end = time.perf_counter() 
    time_cost=end-start
    score=score+new_score

    if sol!=[]:
        #print(f"Nodos explorados con DFS: {nodes_explored}")
        tuplas = sol
        # Convertir cada tupla en una cadena "fila, columna"
        comb = [f"{fila}, {columna}" for fila, columna in tuplas]
        while True:
            print_board(board)
            try:
                print_next_cake(i)
            except:
                print("WINNER")
                break
            print(obtain_pos_movs(board))
            print(f"CAKES LEFT:{len(LIST_CAKES)-i}")
            selection=comb[i]
            if selection=="esc": break
            row,col=selection.split(",")
            row,col=int(row),int(col)
            board,points=place_cake(board,LIST_CAKES[i],int(row),int(col))
            time.sleep(0.5)
            score+=points
            i=i+1
            moves=obtain_pos_movs(board)
            if moves==[] and i<len(LIST_CAKES):
                print("RUN OUT OF SPACE")
                break
        

    print_stats_al(score,sol,count,time_cost)
    save_statistics(player_type, sol, count, score, time_cost, level)


