import tkinter as tk
from tkinter import messagebox, simpledialog
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from objects.cake import *
from CLI.board import *
from CLI.print_menu import *
from actions import *
from save import *
from conf import *
from search.depth import *
from search.heuS import *
from search.breadth import *
from search.greedy import *

from tkinter import simpledialog

def ask_for_algorithm():
    """Ask the user which algorithm to use."""
    algorithms = [
        "Player",
        "Depth First Search",
        "Breadth First Search",
        "A* heuristic 1",
        "A* heuristic 2",
        "GS heuristic 1",
        "GS heuristic 2",
        
    ]

    choice = None
    while choice is None or choice not in range(1, 7):  # Asegura que sea una opción válida (1-6)
        choice = simpledialog.askinteger(
            "Algorithm Selection",
            "Choose an algorithm:\n\n"
            "1. Player\n"
            "2. Depth First Search\n"
            "3. Breadth First Search\n"
            "4. A* heuristic 1\n"
            "5. A* heuristic 2\n"
            "6. GS heuristic 1\n"
            "7. GS heuristic 2\n\n"
            "Enter a number (1-6):",
            minvalue=1,
            maxvalue=7
        )

    return algorithms[choice - 1]  # Devuelve el nombre del algoritmo según la opción elegida
def ask_to_gen():
    choice=messagebox.askquestion(
            "Board Selection",
            "Do you want to load ad previous game?"
        )
    if choice=="yes":
        print("loading board")
        if load_game_state():
            board,index,score,r,c=load_game_state()
            
            if r!=ROWS or c!=COLS:
                print("ERROR: Inconsistent board Size")
                return False
        else:
            print("ERROR: No saved file")
            return False
        level=0
        
    else:
        level = ask_for_level()
        board=generate_board(level)
        index=0
        score=0
        
    return board,index,score,level

def ask_for_level():
    """Ask the user for the game difficulty level."""
    level = None
    while level is None or level not in range(1, 6):  # Assuming levels 1-5
        level = simpledialog.askinteger("Level Selection", "Choose a difficulty level (1-3):", minvalue=1, maxvalue=3)
    return level

def show_final_stats(score, nodes_explored, time_cost, algorithm):
    """Displays a summary window with game statistics."""
    summary_window = tk.Toplevel(root)
    summary_window.title("Game Summary")
    summary_window.geometry("300x200")

    tk.Label(summary_window, text="WINNER", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(summary_window, text=f"Final Score: {score}", font=("Arial", 12)).pack(pady=5)
    tk.Label(summary_window, text=f"Nodes Explored: {nodes_explored}", font=("Arial", 12)).pack(pady=5)
    tk.Label(summary_window, text=f"Execution Time: {time_cost:.2f} sec", font=("Arial", 12)).pack(pady=5)
    tk.Label(summary_window, text=f"Algorithm Used: {algorithm}", font=("Arial", 12)).pack(pady=5)

    tk.Button(summary_window, text="OK", command=summary_window.destroy).pack(pady=10)

def show_gameover():
    """Displays a summary window with game statistics."""
    summary_window = tk.Toplevel(root)
    summary_window.title("Game Over")
    summary_window.geometry("300x200")
    tk.Label(summary_window, text="Game Over", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(summary_window, text=f"There are no more free cells", font=("Arial", 12)).pack(pady=5)
    tk.Button(summary_window, text="OK", command=summary_window.destroy).pack(pady=10)

def draw_squares(canvas, x, y, cell_size, numbers, rows: int = 3, cols: int = 2):
    """Draws rounded squares inside a cell based on the provided list of numbers."""
    color_map = {1: "#FF5733", 2: "#337BFF", 3: "#33FF57", 4: "#FFD700", 5: "#A633FF"}
    
    num_squares = min(len(numbers), rows * cols)
    size = 20  
    padding = 5  
    total_width = (cols * size) + ((cols - 1) * padding)
    total_height = (rows * size) + ((rows - 1) * padding)
    start_x = x + (cell_size - total_width) // 2  
    start_y = y + (cell_size - total_height) // 2  
    
    for i in range(num_squares):
        if numbers[i] != 0:
            offset_x = (i % cols) * (size + padding)
            offset_y = (i // cols) * (size + padding)
            color = color_map.get(numbers[i], "#888888")
            create_rounded_rectangle(canvas, start_x + offset_x, start_y + offset_y, 
                                     start_x + offset_x + size, start_y + offset_y + size, 
                                     radius=5, fill=color, outline="black")

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=10, **kwargs):
    """Creates a rounded rectangle on a Tkinter canvas."""
    points = [x1+radius, y1,
              x2-radius, y1, x2, y1,
              x2, y1+radius, x2, y2-radius,
              x2, y2, x2-radius, y2,
              x1+radius, y2, x1, y2,
              x1, y2-radius, x1, y1+radius,
              x1, y1]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def create_board(canvas, board_data):
    """Creates a board based on a matrix of objects."""
    cell_size = 100  
    
    for row in range(ROWS):
        for col in range(COLS):
            x, y = col * cell_size, row * cell_size
            canvas.create_rectangle(x, y, x + cell_size, y + cell_size, outline="black")
            cell_data = board_data[row][col]
            if isinstance(cell_data, Cake):
                draw_squares(canvas, x, y, cell_size, cell_data.numbers)

def update_next_cake(next_cake_canvas, cake):
    """Draws the next cake without continuously updating."""
    next_cake_canvas.delete("all")
    draw_squares(next_cake_canvas, 10, 10, 80, cake.numbers, rows=3, cols=2)

def update_board(canvas, board_data):
    """Updates the board with new data."""
    canvas.delete("all")
    create_board(canvas, board_data)

def get_cell_from_click(event):
    """Determina en qué celda se ha hecho clic en el tablero."""
    col = event.x // 100  # Tamaño de celda fijo en 100px
    row = event.y // 100
    
    if 0 <= row < ROWS and 0 <= col < COLS:
        print(f"Clicked on cell: ({row}, {col})")
        global selected_cell
        selected_cell = (row, col)
    else:
        print("Click fuera del tablero")
        selected_cell = None



def highlight_cell(board, i):
    """Resalta una celda específica en el tablero."""
    sol, count, new_score = depth_first(board, i)  # No deepcopy
    
    if sol:  
        row, col = sol[0]  # Ensure correct row-col order
    else:
        possible_moves = obtain_pos_movs(board)
        if possible_moves:
            row, col = possible_moves[0]  # Get first available move
        else:
            print("No available moves to highlight")
            return

    canvas.delete("highlight")  # Remove previous highlight
    x, y = col * 100, row * 100  # Convert to pixel position
    canvas.create_rectangle(x, y, x + 100, y + 100, outline="red", width=3, tag="highlight")

def save_game(board,i,score):
    save_game_state(board, i, score,ROWS,COLS)
    save_window = tk.Toplevel(root)
    save_window.title("Game Saved")
    save_window.geometry("300x200")
    tk.Label(save_window, text="Game Saved", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Button(save_window, text="OK", command=save_window.destroy).pack(pady=10)

def on_close():
    print("Closing game...")
    root.quit()  # Detiene mainloop()
    root.destroy()  # Destruye la ventana

#-----------------------------------------------------------------------------------------------------------
# Window setup
root = tk.Tk()
root.withdraw()  # Hide main window until setup is done

# Ask for algorithm and level
player_type = ask_for_algorithm()
try:
    if os.path.exists("docfiles/savefile.txt"):
        board,i,score,level=ask_to_gen()
    else:
        level=ask_for_level()
        board=generate_board(level)
        i=0
        score=0
except:
    loadError = tk.Toplevel(root)
    loadError.title("Game Saved")
    loadError.geometry("400x200")
    tk.Label(loadError, text="The saved board is from a different board size,\n please restart with appropiate config.py settings. \nGenerateing level 1", font=("Arial", 12)).pack(pady=10)
    tk.Button(loadError, text="OK", command=loadError.destroy).pack(pady=10)
    level=1
    board=generate_board(level)
    i=0
    score=0
 
root.deiconify()  # Show the main window now

# Main game setup
root.title("Cake Sort Puzzle")
#root.geometry("400x600")
root.geometry(f"{COLS*100+100}x{ROWS*100+300}")

root.protocol("WM_DELETE_WINDOW", on_close)

score_label = tk.Label(root, text="Score: 0", font=("Arial", 14))
score_label.pack()

canvas = tk.Canvas(root, width=COLS*100, height=ROWS*100, bg="white")
canvas.pack()
canvas.bind("<Button-1>", get_cell_from_click)  # Detecta clics en el tablero

tk.Label(root, text="Next Cake:").pack()
next_cake_canvas = tk.Canvas(root, width=100, height=100, bg="white")
next_cake_canvas.pack()


save_button = tk.Button(root, text="Save", command=lambda: save_game(board, i, score))
save_button.pack(side=tk.LEFT, padx=10, pady=10)
highlight_button = tk.Button(root, text="Hint", command=lambda: highlight_cell(board, i))
highlight_button.pack(side=tk.LEFT, padx=10, pady=10)
create_board(canvas, board)
selected_cell = None
key = f"{player_type}/{level}/{ROWS}/{COLS}"
start = time.perf_counter()
root.update_idletasks()
root.update()
time_hitosry=f"{player_type}/{level}/{ROWS}/{COLS}"
print(f"\n   Loading ... (estimated: {history.get(time_hitosry, 'Unknown')}s)")

if player_type == "Player":
    sol=[]
    while root.winfo_exists():  # Solo sigue si la ventana sigue abierta
        root.update_idletasks()
        root.update()
        if i < len(LIST_CAKES):
            update_next_cake(next_cake_canvas, LIST_CAKES[i])
        else:
            end = time.perf_counter()
            time_cost = end - start
            nodes_explored=len(sol)
            show_final_stats(score, nodes_explored, time_cost, player_type)
            break

        print(f"POSSIBLE MOVES: {obtain_pos_movs(board)}")
        print(f"CAKES LEFT: {len(LIST_CAKES) - i}")
        print(f"SCORE: {score}")

        selected_cell = None  # Resetear selección
        while selected_cell is None:
            root.update_idletasks()
            root.update()  # Esperar a que el usuario haga clic

        row, col = selected_cell
        if selected_cell in obtain_pos_movs(board):
            sol.append(selected_cell)
            board, points = place_cake(board, LIST_CAKES[i], row, col)
            score += points
            i += 1
            score_label.config(text=f"Score: {score}")
            update_board(canvas, board)
            if not obtain_pos_movs(board) and i < len(LIST_CAKES):
                print("RUN OUT OF SPACE")
                show_gameover()
                break


else:
    if player_type == "Depth First Search":
        sol, nodes_explored, new_score = depth_first(board, i)
    elif player_type == "Breadth First Search":
        sol, nodes_explored, new_score = breadth_first(board, i)
    elif player_type == "A* heuristic 1":
        sol, nodes_explored, new_score = heuristic_search(board, i, 1)
    elif player_type == "A* heuristic 2":
        sol, nodes_explored, new_score = heuristic_search(board, i, 2)
    elif player_type == "GS heuristic 1":
        sol, nodes_explored, new_score = greedy_best_first(board, i, 1)
    elif player_type == "GS heuristic 2":
        sol, nodes_explored, new_score = greedy_best_first(board, i, 2)

    end = time.perf_counter()
    time_cost = end - start
    score += new_score
    print(sol)
    if sol:
        for i in range(len(sol)):
            update_board(canvas, board)
            root.update_idletasks()
            try:
                update_next_cake(next_cake_canvas, LIST_CAKES[i])
            except IndexError:
                break
            row, col = map(int, sol[i])
            board, points = place_cake(board, LIST_CAKES[i], row, col)
            score += points
            score_label.config(text=f"Score: {score}")
            root.update_idletasks()
            time.sleep(0.5)
        show_final_stats(score, nodes_explored, time_cost, player_type)
    else:
        show_final_stats("Solution Not Found", nodes_explored, time_cost, player_type)
save_stats = tk.Button(root, text="Save Results", command=lambda: save_statistics(player_type, sol, nodes_explored, score, time_cost, level))
save_stats.pack(side=tk.LEFT, padx=10, pady=10)
root.mainloop()
