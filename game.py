#include some helper libraries
import numpy as np
import random as rand
import json

# read the settings
with open('settings.json') as settings_file:
    settings = json.load(settings_file)

# define some useful constants
LEFT    = 0
UP      = 1
RIGHT   = 2
DOWN    = 3
UNKNOWN = -1

# define the game data structure and some helper functions
class Board:
    def __init__(self):
        self.width = int(settings["board_size"]["width"])
        self.height = int(settings["board_size"]["height"])
        self.rotation_cache = UNKNOWN
        self.score = 0
        self.board = self.clear_board()

        for i in range(int(settings["starting_tile_count"])):
            self.gen_random_tile()
    
    # returns a clear board of width and height specified by the settings.json
    def clear_board(self):
        return np.zeros((self.width, self.height), dtype=np.uint8)
        # return np.array([np.zeros(self.width) for i in range(0, self.height)])

    # these boards will not be used in the game but will be useful for development purposes
    def _demo_board(self):
        return np.array([[0,0,1,1],[1,1,1,1],[2,2,2,2],[3,3,3,3]])
    def _demo_board2(self):
        return np.array([[0,1,1,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]])

    def _demo_not_over_board(self):
        return np.array([[1,1,1,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]])
    def _demo_over_board(self):
        return np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])

    # void function that takes input into the board, determines if a change has been made, and
    # generates a new piece if it has
    def input_direction(self, direction):
        board_copy = np.copy(self.board) # create a deep copy of the array
        self.rotate_board(direction)
        self.collapse_board()
        self.undo_rotation()
        if not np.array_equal(board_copy, self.board):
            self.gen_random_tile()
        #TODO: Add a function to check for a game over
        if self.is_game_over():
            pass

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
    
    # "slides" all numbers to the left and combines like terms once, also increments self.score
    def collapse_row(self, row):
        reduced_row = row[np.where(row > 0)] # remove all zeros
        for i in range(0, reduced_row.size - 1):
            # because array shrinks in loop we need to check out of bounds errors
            if i > reduced_row.shape[0] - 2: 
                break
            # if two side by side numbers are the same, increment the first, delete the second
            if reduced_row[i] == reduced_row[i + 1]:
                reduced_row[i] += 1
                self.score += pow(2, row[i]) # TODO: fix score calculation
                reduced_row = np.delete(reduced_row, i + 1)
        # figure out how many elements were removed then append that many zeros onto the end
        zeros = np.zeros(self.width - reduced_row.size)
        return np.concatenate((reduced_row, zeros), axis=None)

    # inserts a new tile into board at a random 0 location
    def gen_random_tile(self):
        new_tile = 1 if rand.randint(1, 100) <= int(settings["chance_of_two"]) else 2
        zero_indices = np.where(self.board == 0)
        random_spot = rand.randint(0, zero_indices[0].size - 1)
        self.board[zero_indices[0][random_spot]][zero_indices[1][random_spot]] = new_tile

    # tests to see if a tile at board[x][y]
    # has neighbors with similar values at
    # [ ][+][ ]
    # [+][ ][+]
    # [ ][+][ ]
    #
    def has_similar_neighbor(self, x, y):
        for i in range(2):
            x_pos = x - 1 + i
            if (x_pos < 0) | (x_pos >= self.width):
                continue
            for j in range(2):
                y_pos = y - 1 + j
                if (y_pos < 0) | (y_pos >= self.height) | ((x_pos == x) & (y_pos == y)):
                    continue
                if self.board[x_pos, y_pos] == self.board[x,y]:
                    return True
        return False

    # tests to see if the game is over
    # first test is to see if the board is full
    # -if not, reutrn False, game is not over o.O
    #   then goes through the board to see if any neighbor tiles have same value
    #       if so return False
    #   game is over if no tiles have similar neighbors
    # 
    # @pre board.shape = (self.width, self.height)
    # @post board'[i] = board[i] 
    def is_game_over(self):
        if self.board_full():
            for x in range(self.width):
                for y in range(self.height):
                    if self.has_similar_neighbor(x, y):
                        return False
            return True
        return False

    # returns whether or not the board is full
    # returns True if there are no zeroes on the board, False otherwise
    def board_full(self):
        return np.where(self.board == 0)[0].size == 0

    # prints self.board
    def print_raw_board(self):
        print(self.board)

    # prints formatted board, as one might think of a 2048 game
    # translate the numbers to their power of two
    def print_game_board(self):
        print('')
        print('Score: {}'.format(self.score))
        for i in range(0, self.height):
            for j in range(0, self.width):
                val = self.board[i][j]
                scored_val = '' if (val == 0) else 2**val
                print('[{:>4}]'.format(scored_val)),
            print('') # Line break at the end of each row
        print('')

