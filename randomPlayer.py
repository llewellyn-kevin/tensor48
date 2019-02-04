import interface
import random
import time

# Player Type
RANDOM = 1
HEURISTIC = 2

class RandomPlayer:
    def __init__(self):
        self.interface = interface.Interface()
        self.choices = [self.interface.move_right,
                        self.interface.move_left,
                        self.interface.move_up,
                        self.interface.move_down]

        self.choices3 = [self.interface.move_right,
                        self.interface.move_left,
                        self.interface.move_down]

        self.player_type = 0
        self.changeType(HEURISTIC)


    def changeType(self, player_type):
        if player_type == RANDOM:
            self.interface.check_for_change = False
            self.player_type = RANDOM
            return
        elif player_type == HEURISTIC:
            self.interface.check_for_change = True
            self.player_type = HEURISTIC 
            return

    def makeChoice(self):
        # self.interface.board.print_raw_board()
        if self.player_type == RANDOM: 
            random.choice(self.choices)()
            return
        elif self.player_type == HEURISTIC:
            random.choice(self.choices3)()
            if (not self.interface.has_changed) & (self.interface.board.board_full() | (random.random() > 0.9)):
                self.interface.move_up()
            return


    def play(self):
        if not self.interface.is_game_over():
            self.makeChoice()
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

