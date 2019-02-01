import game

board = game.Board()
print ("is over")
print (board.game_over())

board.board = board._demo_not_over_board()

print ("new board")
board.print_raw_board()

print ("is over")
print (board.game_over())
print ("is over")
board.board = board._demo_over_board()
board.print_raw_board()
print (board.game_over())
