import time
from .clean import clean_screen
from .board import generate_board
from conf import *
from save import load_game_state

SPACE = 20  # Space padding for menu formatting

def print_menu(title, options):
    """
    Prints a formatted menu with a title and a list of options.
    
    Args:
        title (str): The title of the menu.
        options (list): A list of menu options to display.
    """
    border = "=" * (len(title) + SPACE * 2)  # Create a border based on title length
    print(f"\n{border}")
    jump = " " * SPACE  # Space padding for title alignment
    print(jump + title + jump)  # Print the title with padding
    print(f"{border}")
    print("\n")
    for i, option in enumerate(options, 1):  # Enumerate options starting from 1
        print(f"  {i}. {option}")  # Print each option with its index
    print("\n")
    print(f"{border}\n")

def ask_choice(prompt, min_choice, max_choice):
    """
    Prompts the user to enter a choice within a specified range.
    
    Args:
        prompt (str): The prompt message to display.
        min_choice (int): The minimum valid choice.
        max_choice (int): The maximum valid choice.
    
    Returns:
        int: The user's valid choice.
    """
    while True:
        try:
            choice = int(input(prompt))  # Get user input as an integer
            if min_choice <= choice <= max_choice:  # Check if choice is within range
                return choice
            else:
                print(f"Please enter a number between {min_choice} and {max_choice}.")
        except ValueError:
            print("Invalid input. Please enter a number.")  # Handle non-integer input

def main_menu():
    """
    Displays the main menu and handles user choices for board options.
    """
    clean_screen()
    # Main menu: Player or Algorithms
    print_menu("CAKE SORT PUZZLE", ["Player", "Algorithms"])
    choice = ask_choice("Who will play? (1-2): ", 1, 2)
    if choice==2:
        clean_screen()
        print_menu("Algorithms", ["Depth First Search", "Breadth First Search", "A* heurstic 1","A* heuristic 2","GS heuristic 1","GS heuristic 2"])
        choice = ask_choice("Which Algorithm? (1-6): ", 1, 6)
        if choice==1:player_type = "Depth First Search" 
        elif choice==2: player_type="Breadth First Search"
        elif choice==3: player_type="A* heuristic 1"
        elif choice==4: player_type="A* heuristic 2"
        elif choice==5: player_type="GS heuristic 1"
        elif choice==6: player_type="GS heuristic 2"
    else:
        player_type = "Player" 
    clean_screen()

    # Secondary menu: Load or Generate Board
    print_menu("Board Options", ["Generate Board","Load Board"])
    choice = ask_choice("Choose an option (1-2): ", 1, 2)
    clean_screen()

    if choice == 2:
        # Load Board
        print("\nLoading board...")
        time.sleep(1)  # Simulate loading time
        # Logic to load a board from a file or database would go here.
        if load_game_state():
            board,index,score,r,c=load_game_state()
            if r!=ROWS or c!=COLS:
                print("ERROR: Inconsistent board Size")
                return False
        else:
            print("ERROR: No saved file")
            return False
        difficulty=0
        print("Board loaded successfully!")
        time.sleep(1)
    else:
        # Generate Board
        print_menu("Difficulty Level", ["Easy (1)", "Medium (2)", "Hard (3)"])
        difficulty = ask_choice("Choose the difficulty (1-3): ", 1, 3)
        clean_screen()
        print(f"\nGenerating a board with difficulty level {difficulty}...")
        board=generate_board(difficulty)
        index=0
        score=0
        time.sleep(1)  # Simulate board generation time
        # Logic to generate a board based on difficulty would go here.
        print("Board generated successfully!")
        time.sleep(1)

    # Final message
    clean_screen()
    print(f"\n{"=" * (10 + SPACE * 2)}")
    print(f"  {player_type} will play on the board!  ")  # Display who will play
    print(f"{"=" * (10 + SPACE * 2)}\n")
    time.sleep(2)
    return player_type,board,difficulty,index,score

def ask_save_board():
    clean_screen()
    print_menu("Do you want to save your progress?", ["Yes","No"])
    return ask_choice("Save progress? (1-2): ", 1, 2)

def print_stats_al(score,sol,count,time_cost):

    print(f"\n{"=" * (10 + SPACE * 2)}")
    print(f"{" "*SPACE}RESULT  ")  # Display who will play
    print(f"{"=" * (10 + SPACE * 2)}\n")
    if sol!=[]:
        print(f"    SCORE:       {score}")
        print(f"    Solution:    {sol}")
        print(f"    Spatil Cost: {count}")
        print(f"    Time Cost:   {time_cost}\n")
    else:
        print(f"    No solution found\n")
    print(f"{"=" * (10 + SPACE * 2)}\n")

def print_stats_pl(score):
    print(f"\n{"=" * (10 + SPACE * 2)}")
    print(f"{" "*SPACE}RESULT  ")  # Display who will play
    print(f"{"=" * (10 + SPACE * 2)}\n")
    print(f"    SCORE:       {score}\n")
    print(f"{"=" * (10 + SPACE * 2)}\n")