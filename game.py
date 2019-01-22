#include some helper libraries
import numpy as np

#define some useful constants
LEFT    = 0
UP      = 1
RIGHT   = 2
DOWN    = 3
UNKNOWN = -1

WIDTH  = 4
HEIGHT = 4

#define the game data structure and some helper functions
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rotation_cache = UNKNOWN
        self.score = 0
        self.board = self._demo_board2()
        self.collapse_board()

    def clear_board(self):
        return np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
        # TODO: Replace this method, and maybe the demo ones to be able to dymically create 
        # an empty board of the proper size

    # these boards will not be used in the game but will be useful for development purposes
    def _demo_board(self):
        return np.array([[0,0,1,1],[1,1,1,1],[2,2,2,2],[3,3,3,3]])
    def _demo_board2(self):
        return np.array([[0,1,1,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]])

    # to input player actions, we will rotate the board, so we only have to slide the numbers to 
    # the left. So if the tiles are pushed up, we will orient the board to have the top side as 
    # the left side, and then we will collapse the board, then rotate the board back
    def rotate_board(self, magnitude):
        self.board = np.rot90(self.board, magnitude)
        self.rotation_cache = magnitude
    def undo_rotation(self):
        if self.rotation_cache == UNKNOWN:
            raise AssertionError('''Assertion of Board.undo_rotation is that Board.rotate_board has 
                been called since this method was last called. This failed. Board.undo_rotation was 
                either called twice or was called before Board.rotation was ever called''')
            # this error should only be raised internally by the class, never by external code

        self.board = np.rot90(self.board, self.rotation_cache * -1)
        self.rotation_cache = UNKNOWN

    # performs collapse_row on every row of the board
    def collapse_board(self):
        self.board = np.array([self.collapse_row(row) for row in self.board])
    
    # "slides" all numbers to the left and combines like terms once
    def collapse_row(self, row):
        reduced_row = row[np.where(row > 0)] # remove all zeros
        for i in range(0, reduced_row.size - 1):
            # because array shrinks in loop we need to check out of bounds errors
            if i > reduced_row.shape[0] - 2: 
                break
            # if two side by side numbers are the same, increment the first, delete the second
            if reduced_row[i] == reduced_row[i + 1]:
                reduced_row[i] += 1
                self.score += pow(2, row[i])
                reduced_row = np.delete(reduced_row, i + 1)
        # figure out how many elements were removed then append that many zeros onto the end
        zeros = np.zeros(self.width - reduced_row.size)
        return np.concatenate((reduced_row, zeros), axis=None)
        # TODO: make this not return doubles

    def print_raw_board(self):
        print(self.board)
    def print_game_board(self):
        for i in range(0, self.width):
            for j in range(0, self.height):
                scored_val = '' if (self.board[i][j] == 0) else pow(2, self.board[i][j])
                print('[{:>4}]'.format(scored_val)),
            print('') # Line break at the end of each row

board = Board(WIDTH, HEIGHT)
board.print_raw_board()
board.print_game_board()
