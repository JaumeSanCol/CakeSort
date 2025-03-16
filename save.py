import json
from conf import *

import json
from objects.cake import Cake  # Asegúrate de importar la clase Cake

def save_game_state(board, index, score, rows, cols):
    with open("docfiles/savefile.txt", 'w') as file:
        json.dump({
            'board': board,
            'index': index,
            'score': score,
            'rows': rows,
            'cols': cols
        }, file, default=lambda obj: obj.__dict__)  # Convierte objetos a diccionarios

def load_game_state():
    try:
        with open("docfiles/savefile.txt", 'r') as file:
            data = json.load(file)

        board = []
        for row in data['board']:
            new_row = []
            for cell in row:
                if isinstance(cell, dict) and "numbers" in cell:  # Verifica si es un Cake
                    new_row.append(Cake(numbers=cell["numbers"]))  # Crea un Cake correctamente
                else:
                    new_row.append(cell)  # Si es un 0, simplemente se añade
            board.append(new_row)

        return board, data['index'], data['score'], data['rows'], data['cols']

    except Exception as e:
        print(f"Error loading game: {e}")
        return False

def save_statistics(algorithm, solution, nodes, score, time, level):
    with open("docfiles/stats.txt", 'a') as file:  # 'a' para añadir sin sobrescribir
        file.write(f"{algorithm}:{solution} N: {nodes}\tSCORE: {score}\tTime: {time:.2f}\tLEVEL {level}\tROWS: {ROWS}\tCOLS: {COLS}\n")
