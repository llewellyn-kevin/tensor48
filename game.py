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
        self.rotation_cache = UNKNOWN
        self.board = self.clear_board()

    def clear_board(self):
        return np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])

    #these boards will not be used in the game but will be useful for development purposes
    def _demo_board(self):
        return np.array([[0,0,0,0],[1,1,1,1],[2,2,2,2],[3,3,3,3]])
    def _demo_board2(self):
        return np.array([[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]])


    def rotate_board(self, magnitude):
        self.board = np.rot90(self.board, magnitude)
        self.rotation_cache = magnitude
    def undo_rotation(self):
        if self.rotation_cache == UNKNOWN:
            raise AssertionError('''Assertion of Board.undo_rotation is that Board.rotate_board has 
                been called since this method was last called. This failed. Board.undo_rotation was 
                either called twice or was called before Board.rotation was ever called''')
        self.board = np.rot90(self.board, self.rotation_cache * -1)
        self.rotation_cache = UNKNOWN
        

    def print_raw_board(self):
        print(self.board)

board = Board()
