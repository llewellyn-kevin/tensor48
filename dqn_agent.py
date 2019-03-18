from dqn_env import T48Env

import tensorflow as tf

from tf_agents.environments import tf_py_environment
from tf_agents.environments import tf_environment

# from tf_agents.agents.dqn import dqn_agent
# from tf_agents.agents.dqn import q_network
# from tf_agents.drivers import dynamic_step_driver
# from tf_agents.environments import trajectory
# from tf_agents.metrics import metric_utils
# from tf_agents.metrics import tf_metrics
# from tf_agents.policies import random_tf_policy
# from tf_agents.replay_buffers import tf_uniform_replay_buffer
# from tf_agents.utils import common

# Hyperparameters




# Set up Environment
env = T48Env()
tf_env = tf_py_environment.TFPyEnvironment(env)

print(isinstance(tf_env, tf_environment.TFEnvironment))
print("TimeStep Specs:", tf_env.time_step_spec())
print("Action Specs:", tf_env.action_spec())
