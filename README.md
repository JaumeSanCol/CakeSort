# Cake Sort Puzzle Solver

This program is designed to solve the **1D Cake Sort Puzzle** from **Assignment 1** in **L.EIC029 - Artificial Intelligence**.

## Overview
The program offers two interfaces:
- **Command Line Interface (CLI)**
- **Graphical User Interface (GUI)** (based on Tkinter)

### Configuration
Before running the program, configure the `conf.py` file, which defines the sequence of cakes and the board size.

- **Default settings**: A sequence of **10 cakes** and a **3x3 board**.
- **Performance considerations**: Due to the time complexity of exhaustive search, increasing the board size will significantly impact execution time:
  - **BFS with 8 empty cells** in the initial state: ~30s
  - **BFS with 9 empty cells** in the initial state: ~300s
- The board **size can be increased** (but not decreased), and the number of cakes can be modified, provided it is greater than 1.

### Running the Program
After configuring `conf.py`, choose the interface to run:
- **CLI**: Execute `main.py`
- **GUI**: Execute `app.py` inside the `GUI` folder


---

## Command Line Interface (CLI)
Upon execution, the program prompts you to either:
1. **Play the game manually**, or
2. **Let an algorithm solve the puzzle**

If you choose an algorithm, a list of available algorithms will be displayed for selection.

You must then choose whether to:
- **Generate a new board**, selecting a difficulty level, or
- **Load a previously saved board** (found in `docfiles/savefile.txt`)
> **Note**: If you want to load a previously saved board, ensure that the board size in `conf.py` matches the saved board's size.

### Gameplay & Solution Process
- If an **algorithm** is solving the puzzle, it will:
  - Execute the solution
  - Display the moves
  - Print the results
  - Store statistics in `docfiles/stats.txt`
- If **you are playing manually**, enter the coordinates `(row,column)` of the cell where you want to place the next cake, e.g., `0,1`.
  - Type `"hint"` to receive a suggested move.
  - Type `"esc"` to exit the game. Upon exiting, you will be asked whether to save the board in `savefile.txt`.

---

## Graphical User Interface (GUI)
When launched, the GUI will first prompt you to:
1. **Select a player (human or algorithm)**
2. **Load a saved board (if available) or start a new game by selecting a difficulty level**
> **Note**: If you want to load a previously saved board, ensure that the board size in `conf.py` matches the saved board's size.

### Gameplay Features
- The interface displays:
  - The board
  - The next cake to be placed
  - The current score
- Available buttons:
  - **Hint** → Suggests a move
  - **Save** → Saves the current board to `savefile.txt`
- Once the game ends (whether played manually or solved by an algorithm), a **"Save Results"** button appears, allowing you to store the results in `docfiles/stats.txt`.
