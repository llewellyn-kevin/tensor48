import game

class Interface:
    def __init__(self):
        self.board = game.Board()
    
    # define all user inputs
    def move_up(self):
        self.board.input_direction(game.UP)


    def move_down(self):
        self.board.input_direction(game.DOWN)


    def move_left(self):
        self.board.input_direction(game.LEFT)


    def move_right(self):
        self.board.input_direction(game.RIGHT)

    def restart(self):
        self.board.reset()

    # define all of my getters
    def get_board(self):
        return self.board.board


    def get_score(self):
        return self.board.score

