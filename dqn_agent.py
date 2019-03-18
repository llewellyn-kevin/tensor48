from dqn_env import T48Env

import tensorflow as tf

from tf_agents.environments import tf_py_environment
from tf_agents.environments import tf_environment
from tf_agents.agents.dqn import q_network
from tf_agents.agents.dqn import dqn_agent

# from tf_agents.drivers import dynamic_step_driver
# from tf_agents.environments import trajectory
# from tf_agents.metrics import metric_utils
# from tf_agents.metrics import tf_metrics
# from tf_agents.policies import random_tf_policy
# from tf_agents.replay_buffers import tf_uniform_replay_buffer
# from tf_agents.utils import common

tf.compat.v1.enable_resource_variables()

# Hyperparameters

fc_layer_params = (100,)
learning_rate = 1e-3


# Function Definitions
def log_step(step):
    print('')
    print(step)
    print("====================================================")

def compute_avg_return(environment, policy, num_episodes=10):

    total_return = 0.0
    for _ in range(num_episodes):

        time_step = environment.reset()
        episode_return = 0.0

        while not time_step.is_last():
            action_step = policy.action(time_step)
            time_step = environment.step(action_step.action)
            episode_return += time_step.reward
        total_return += episode_return

    avg_return = total_return / num_episodes
    return avg_return.numpy()[0]

# Set up Environment
env = T48Env()
tf_env = tf_py_environment.TFPyEnvironment(env)

log_step("Environment Information")
print("Confirm tf_env:", isinstance(tf_env, tf_environment.TFEnvironment))
print("TimeStep Specs:", tf_env.time_step_spec())
print("Action Specs:", tf_env.action_spec())

# Establish Network
log_step('Establishing Q Network')
q_net = q_network.QNetwork(
    tf_env.observation_spec(),
    tf_env.action_spec(),
    fc_layer_params=fc_layer_params)

# Instantiate optimizer, step_counter, and agent
# optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate)
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)

# train_step_counter = tf.compat.v2.Variable(0)
train_step_counter = tf.Variable(0)

log_step('Establishing DQN Agent')
tf_agent = dqn_agent.DqnAgent(
    tf_env.time_step_spec(),
    tf_env.action_spec(),
    q_network=q_net,
    optimizer=optimizer,
    td_errors_loss_fn=dqn_agent.element_wise_squared_loss,
    train_step_counter=train_step_counter)
tf_agent.initialize()

# Using default policies
log_step('Choosing Policies')
eval_policy = tf_agent.policy
collect_policy = tf_agent.collect_policy


