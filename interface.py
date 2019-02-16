import game
import numpy as np

class Interface:
    def __init__(self):
        self.board = game.Board()
        self.check_for_change = False
        self.has_changed = False        

    # define all user inputs
    def move(self, direction):
        if self.check_for_change:
            copy = np.copy(self.board.board)
        self.board.input_direction(direction)
        if self.check_for_change:
            self.has_changed = not ((copy == self.board.board).all())

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

