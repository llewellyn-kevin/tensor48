# Get clear replay buffer 
def new_replay_buffer(starting_tiles, speed = 8):
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
        replay_buffer += '      new_tile: null },\r\n'
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

