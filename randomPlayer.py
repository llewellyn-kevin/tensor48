import interface
import random
import matplotlib.pyplot as plt

class RandomPlayer:
    def __init__(self):
        self.interface = interface.Interface()
        self.choices = [self.interface.move_right,
                        self.interface.move_left,
                        self.interface.move_up,
                        self.interface.move_down]
        self.scores = []


    def play(self):
        if not self.interface.is_game_over():
            random.choice(self.choices)()
            return True
        else:
            return False


    def run(self):
        run_times = 100
        total_score = 0
        for i in range(run_times):
            while(self.play()):
                pass
            score = self.interface.get_score()
            self.scores.append(score)
            total_score += score 
            # print( score )
            self.interface.restart()
        print
        print("average")
        print(total_score // run_times)
        plt.plot(range(run_times), self.scores)
        plt.show()
