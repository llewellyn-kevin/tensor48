import game
import numpy as np

class Interface:
    def __init__(self):
        self.board = game.Board()
        self.has_changed = False        

    # define all user inputs
    def move(self, direction):
        self.board.input_direction(direction)
        self.has_changed = self.board.has_changed

    def move_up(self):
        self.move(game.UP)


    def move_down(self):
        self.move(game.DOWN)


    def move_left(self):
        self.move(game.LEFT)


    def move_right(self):
        self.move(game.RIGHT)


    def restart(self):
        self.board.reset()
        self.has_changed = False

    # define all of my getters
    def get_board(self):
        return self.board.board


    def get_score(self):
        return self.board.score

    
    def is_game_over(self):
        return self.board.is_game_over

    def _print(self):
        self.board.print_raw_board()

