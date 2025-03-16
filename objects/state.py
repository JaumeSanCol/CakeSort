from CLI.board import *
import copy
class State:
    def __init__(self, board,index_cake):
        self.parent= None
        self.next_cake=copy.deepcopy(LIST_CAKES[index_cake])
        self.index_cake=index_cake
        self.board = copy.deepcopy(board)

        self.moves= []
        self.moves= obtain_pos_movs(self.board)
        self.cost=0
        self.child= None
        self.child_move=None
        self.score=0

    def __lt__(self, other):
        return self.cost < other.cost 