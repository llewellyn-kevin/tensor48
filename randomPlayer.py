import interface
import random
import time

class RandomPlayer:
    def __init__(self):
        self.interface = interface.Interface()
        self.choices = [self.interface.move_right,
                        self.interface.move_left,
                        self.interface.move_up,
                        self.interface.move_down]


    def play(self):
        if not self.interface.is_game_over():
            random.choice(self.choices)()
            return True
        else:
            return False


    def run(self):
        begin = time.clock()
        run_times = 1000
        total_score = 0
        total_moves = 0
        for i in range(run_times):
            while(self.play()):
                total_moves += 1
            score = self.interface.get_score()
            total_score += score 
            # print( score )
            self.interface.restart()
        print("time")
        print(time.clock() - begin)
        print("")
        print("average # moves")
        print(total_moves // run_times)
        print("")
        print("average score")
        print(total_score // run_times)
