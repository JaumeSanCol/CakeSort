import time
from conf import *
from CLI.board import *
from objects.cake import *
import copy

# Function to update the board after placing a Cake
def update_board(board, row, col):
    board = copy.deepcopy(board)  # Ensure modifications do not affect the original board
    score=0
    cake = board[row][col]
    adjacent_positions = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    # Try to give to your neighbours
    for r, c in adjacent_positions:
        if 0 <= r < ROWS and 0 <= c < COLS and isinstance(board[r][c], Cake):
            neighbor = board[r][c]
            if r==1 and c==0 and row==2 and col==0:  # Specific condition, consider explaining
                pass
            # Try to donate or receive values between cakes
            if neighbor.empty>0:
                for i in range(6):
                    
                        # Check if the neighbour cake wants our number
                        if cake.numbers[i] in neighbor.main:
                            # Give all our numbers
                            for j in range(6):
                                # Ensure there is still room
                                #if neighbor.empty>0:
                                    if neighbor.numbers[j]==0:
                                        neighbor.numbers[j]=cake.numbers[i]
                                        cake.numbers[i]=0
                                        # update the number of empty spaces
                                        neighbor.check_empty()
                                        cake.check_empty()
                                        # Check if any of the two need to be erased
                                        board,points=check_removal(board, row, col)
                                        score+=points
                                        board,points=check_removal(board, r, c)
                                        score+=points
                                        #time.sleep(1)  # Uncomment if visualization delay is needed
                                        
                                        break
                            # After giving out, update main but only if the cake is not empty
                            if cake.empty!=6: cake.check_main()
    # Try to receive from the neighbours
    if 0<cake.empty<6:
        for r, c in adjacent_positions:
            if 0 <= r < ROWS and 0 <= c < COLS and isinstance(board[r][c], Cake):
                neighbor = board[r][c]
                for i in range(6):
                    if neighbor.numbers[i] in cake.main:
                        for j in range(6):
                                if cake.numbers[j]==0:
                                    cake.numbers[j]=neighbor.numbers[i]
                                    neighbor.numbers[i]=0
                                    # update the number of empty spaces
                                    neighbor.check_empty()
                                    cake.check_empty()
                                    # Check if any of the two need to be erased
                                    board,points=check_removal(board, row, col)
                                    score+=points
                                    board,points=check_removal(board, r, c)
                                    score+=points
                                    #time.sleep(1)  # Uncomment if visualization delay is needed
                                    break
                        cake.check_main()
    return board,score

def check_removal(board, row, col):
    """
    Function to check if a Cake should be removed based on its state.
    """
    cake = board[row][col]
    
    if isinstance(cake, Cake):  # Ensure there is a cake in the cell
        if cake.numbers.count(cake.numbers[0]) == 6:
            board[row][col] = 0  # Remove full Cake
            return board,1
        if cake.numbers.count(0) == 6:
            board[row][col] = 0  # Remove empty Cake

    return board,0

# Function to place a Cake in an empty cell
def place_cake(board, cake, row, col):
    board = copy.deepcopy(board)  # Ensure modifications do not affect the original board
    if board[row][col] == 0:  # Check if the cell is empty
        board[row][col] = cake
        board,score=update_board(board, row, col)  # Check if it can donate or receive numbers
    else:
        raise ValueError(f"Not possible {row}x{col}")
        
    return board,score
