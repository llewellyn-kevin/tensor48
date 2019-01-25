import game
import curses

def main(stdscr):

    stdscr.keypad(True)
    stdscr.nodelay(True)

    stdscr.clear()
    write_template(stdscr)
    stdscr.refresh()
    
    while True:
        char = stdscr.getch()
        if char == ord('q'):
            break
        if not char == -1:
            stdscr.clear()
            write_template(stdscr)
            stdscr.refresh()

def write_template(stdscr):
    stdscr.move(2, 9)
    stdscr.addstr('2048 in Python')
    stdscr.move(4, 6)
    # TODO: Make this display the actual score
    stdscr.addstr('Current Score: 000000')
    write_board(stdscr)
    stdscr.move(24, 2)
    stdscr.addstr('Press "q" to quit at any time')
    stdscr.move(0, 0)

# Writes the board to the screen
# TODO: Make this code scalable with changing board sizes and actually 
# display numbers
def write_board(stdscr):
    for i in range(0, 4):
        stdscr.move(4 * i + 6, 2)
        write_border(stdscr)
        stdscr.move(4 * i + 7, 2)
        write_line(stdscr)
        stdscr.move(4 * i + 8, 2)
        write_line(stdscr)
        stdscr.move(4 * i + 9, 2)
        write_line(stdscr)
    stdscr.move(22, 2)
    write_border(stdscr)
def write_line(stdscr):
    stdscr.addstr('|      |      |      |      |')
def write_border(stdscr):
    stdscr.addstr('+------+------+------+------+')


curses.wrapper(main)
