#include some helper libraries
import numpy as np

#define some useful constants
LEFT    = 0
UP      = 1
RIGHT   = 2
DOWN    = 3
UNKNOWN = -1

#define the game data structure and some helper functions
class Board:
    def __init__(self):
        self.board = self._demo_board2()
        self.get_rotated_board(2)

        self.rotation_cache = UNKNOWN

    def clear_board(self):
        return np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])

    #these boards will not be used in the game but will be useful for development purposes
    def _demo_board(self):
        return np.array([[0,0,0,0],[1,1,1,1],[2,2,2,2],[3,3,3,3]])
    def _demo_board2(self):
        return np.array([[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]])


    def get_rotated_board(self, magnitude):
        return np.rot90(self.board, magnitude)

    def print_raw_board(self):
        print(self.board)

board = Board()
board.print_raw_board()
