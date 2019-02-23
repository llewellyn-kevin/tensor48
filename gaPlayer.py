import interface
import time
import random
import GA
import numpy as np


class GAPlayer:
    def __init__(self):
        self.interface = interface.Interface()
        self.interface.check_for_change = True
        self.choices = [self.interface.move_right,
                        self.interface.move_left,
                        self.interface.move_up,
                        self.interface.move_down]
        self.ga = GA.GA(4 * 4, 5, 4)
        # print(nn.wi)
        # print(nn.wo)
        # self.interface._print()


    def makeChoice(self, pos):
        # self.interface.board.print_raw_board()
        inputs = self.interface.board.board.copy()
        inputs = (inputs - 1) / float(-4)
        inputs = (2 / (1 + np.exp(inputs)) - 1) 
        array = self.ga.get_nn(pos).feedForward(np.ndarray.flatten(inputs))
        choice = np.where(array == np.max(array))[0][0]
        self.choices[choice]()
        # random.choice(self.choices)()


    def play(self, pos):
        if (not self.interface.is_game_over()) & self.interface.has_changed:
            self.makeChoice(pos)
            return True
        else:
            return False


    def run(self):
        begin = time.clock()
        run_times = 100 
       
        restart = self.interface.restart
        get_score = self.interface.get_score
        for i in range(run_times):
            length = self.ga.length
            for pos in range(length):
                self.ga.set_score(pos, 0)
                for j in range(5):
                    self.makeChoice(pos)
                    while(self.play(pos)):
                        pass
                    self.ga.add_score(pos, get_score())
                    restart()
            self.ga.next_gen()
        print("time")
        print(time.clock() - begin)
        print("")

    def _print(self):
        self.interface._print()

