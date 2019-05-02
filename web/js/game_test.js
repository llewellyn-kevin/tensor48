var game_record = {
  replay_speed: 2, // Updates per second
  start_tiles: [{x: 0, y: 0, val: 4}, {x: 1, y: 0, val: 2}],
  moves: [
    {
      direction: 1,
      new_tile: {x: 0, y: 0, val: 4}
    },
    {
      direction: 1,
      new_tile: {x: 0, y: 1, val: 2}
    },
    {
      direction: 1,
      new_tile: null
    },
    {
      direction: 2,
      new_tile: {x: 0, y: 2, val: 2}
    }
  ]
};
