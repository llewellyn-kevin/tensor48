from interface import Interface

import tensorflow as tf
import numpy as np

from tf_agents.environments import py_environment
from tf_agents.environments import time_step as ts
from tf_agents.environments import utils
from tf_agents.specs import array_spec

class T48Env(py_environment.PyEnvironment):

    def __init__(self):
        self._action_spec = array_spec.BoundedArraySpec(
                shape=(), dtype=np.int32, minimum=0, maximum=3, name='action')
        self._observation_spec = array_spec.BoundedArraySpec(
                shape=(4,4), dtype=np.uint8, minimum=0, name='observation')
        self._state = 0
        self._episode_ended = False

        self._game = Interface()

        # Define Actions
        self._UP = 0
        self._DOWN = 1
        self._LEFT = 2
        self._RIGHT = 3

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self._game.restart()
        self._state = self._game.get_board()
        self._episode_ended = False
        return ts.restart(self._state)

    def _step(self, action):

        if self._episode_ended:
            # The last action ended the episode. Ignore the current action and start
            # a new episode.
            return self.reset()

        iscore = self._game.get_score()

        # Input agent action
        if action == self._UP:
            self._game.move_up()
        elif action == self._DOWN:
            self._game.move_down()
        elif action == self._LEFT:
            self._game.move_left()
        elif action == self._RIGHT:
            self._game.move_right()
        else:
            raise ValueError('`action` should be between 0 and 3 (inclusive).')

        # Get state after the agent action is taken
        self._state = self._game.get_board()
        self._episode_ended = self._game.is_game_over()
        delta_score = self._game.get_score() - iscore
        
        # Set rewards
        if self._episode_ended:
            # return with a reward of 0
            return ts.termination(self._state, 0.0)
        else:
            return ts.transition(self._state, reward=delta_score, discount=1.0)

# environment = T48Env()
# utils.validate_py_environment(environment, episodes=5)
