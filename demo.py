import curses 
import game
from interface import Interface
from datetime import datetime

# This defines the main game loop. It constantly checks for inputs
# and when it recieves them contacts the Interface facade to update
# the state of the board. Then on input recieved it displays the
# board. Exits when 'q' is input by the user
def main(stdscr):
    # Set some settings for keyboard inputs
    stdscr.keypad(True)
    stdscr.nodelay(True)

    # Write the board in its starting state
    stdscr.clear()
    write_template(stdscr)
    write_nums(stdscr, interface.get_board())
    stdscr.refresh()

    # Start the replay buffer 
    replay_buffer = new_replay_buffer(interface.get_starting_tiles())
        
    # Demo game loop
    while True:
        char = stdscr.getch()
        # check for control inputs
        if char == ord('q'):
            return False
        elif char == ord('r'):
            interface.restart()
        elif char == ord('s'): 
            save_game(finish_replay_buffer(replay_buffer))
        # check for game inputs
        elif char == curses.KEY_LEFT: 
            interface.move_left()
            replay_buffer = add_move_to_buffer(replay_buffer, 
                    0, interface.get_last_tile())
        elif char == curses.KEY_UP:
            interface.move_up()
            replay_buffer = add_move_to_buffer(replay_buffer, 
                    1, interface.get_last_tile())
        elif char == curses.KEY_RIGHT:
            interface.move_right()
            replay_buffer = add_move_to_buffer(replay_buffer, 
                    2, interface.get_last_tile())
        elif char == curses.KEY_DOWN:
            interface.move_down()
            replay_buffer = add_move_to_buffer(replay_buffer, 
                    3, interface.get_last_tile())
        # if there was input, update the game board display
        if not char == -1:
            stdscr.clear()
            write_template(stdscr)
            write_nums(stdscr, interface.get_board())
            stdscr.refresh()


# Get clear replay buffer 
def new_replay_buffer(starting_tiles, speed = 2):
    replay_buffer = 'game_record = {\r\n'
    replay_buffer += '  replay_speed: {},\r\n'.format(speed)
    replay_buffer += '  start_tiles: ['
    for tile in starting_tiles:
        replay_buffer += '{{ x: {}, y: {}, val: {} }}, '.format(tile['x'], tile['y'], tile['val'])
    replay_buffer += '],\r\n'
    replay_buffer += '  moves: [\r\n'
    return replay_buffer


# Takes current buffer and a move and adds it to the replay buffer
def add_move_to_buffer(current_buffer, move, tile_spawn):
    replay_buffer = current_buffer 
    replay_buffer += '      {{ direction: {},\r\n'.format(move)
    if tile_spawn is None:
        replay_buffer += '      new_tile: null }}\r\n'
    else:
        replay_buffer += '        new_tile: {{ x: {}, y: {}, val: {} }} }},\r\n'.format(tile_spawn['x'], 
                tile_spawn['y'], tile_spawn['val'])
    return replay_buffer 


# Prints the final characters needed to round out a replay buffer
def finish_replay_buffer(current_buffer):
    replay_buffer = current_buffer 
    replay_buffer += '  ]\r\n'
    replay_buffer += '};'
    return replay_buffer


# Writes the structure for the whole game
# This includes a title, some info, instructions
def write_template(stdscr):
    stdscr.move(2, 9)
    stdscr.addstr('2048 in Python')
    stdscr.move(4, 6)
    # TODO: Make this display the actual score
    stdscr.addstr('Current Score: {:>6}'.format(int(interface.get_score())))
    if interface.is_game_over():
        stdscr.move(5, 6)
        stdscr.addstr('GAME OVER!')
    write_board(stdscr)
    stdscr.move(24, 2)
    stdscr.addstr('Press "q" to quit')
    stdscr.move(25, 2)
    stdscr.addstr('Press "r" to restart')
    stdscr.move(26, 2)
    stdscr.addstr('Press "s" to save replay')
    stdscr.move(0, 0)
    write_message(stdscr)


global_message = ''

def set_message(message):
    global global_message
    global_message = message

def write_message(stdscr):
    stdscr.move(28, 2)
    stdscr.addstr(global_message)

# Writes a blank board to the screen
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


def write_nums(stdscr, board):
    for rindex, row in enumerate(board):
        for cindex, col in enumerate(row):
            if not col == 0:
                stdscr.move(4 * rindex + 8, 7 * cindex + 4)
                stdscr.addstr('{}'.format(int(2 ** col)))
    stdscr.move(0, 0)


def save_game(record):
    fname = 'replays/demo_recording_{}.js'.format(datetime.now()).replace(' ', '_')
    f = open(fname, 'w+')
    f.write(record)
    f.close()
    
    set_message('Wrote replay file to {}'.format(fname))

# Demo driver
interface = Interface()
restart = curses.wrapper(main)
