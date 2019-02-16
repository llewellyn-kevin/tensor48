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
        self.ga = GA.GA()
        self.nn = GA.NeuralNet()
        self.nn.init_rand(4 * 4, 5, 4)
        # print(nn.wi)
        # print(nn.wo)
        # self.interface._print()


    def makeChoice(self):
        # self.interface.board.print_raw_board()
        array = self.nn.feedForward(np.ndarray.flatten(self.interface.board.board))
        choice = np.where(array == np.max(array))[0][0]
        self.choices[choice]()
        # random.choice(self.choices)()


    def play(self):
        if (not self.interface.is_game_over()) & self.interface.has_changed:
            self.makeChoice()
            return True
        else:
            return False


    def run(self):
        begin = time.clock()
        run_times = 100000
        total_score = 0
        total_moves = 0
        for i in range(run_times):
            while(self.play()):
                total_moves += 1
            score = self.interface.get_score()
            total_score += score 
            self.interface.restart()
        print("time")
        print(time.clock() - begin)
        print("")
        print("average # moves")
        print(total_moves / run_times)
        print("")
        print("average score")
        print(total_score / run_times)
        print("score")
        print(total_score)

