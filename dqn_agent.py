from dqn_env import T48Env

import tensorflow as tf

from tf_agents.environments import tf_py_environment
from tf_agents.environments import tf_environment
from tf_agents.agents.dqn import q_network
from tf_agents.agents.dqn import dqn_agent
from tf_agents.environments import trajectory
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.utils import common
from tf_agents.policies import random_tf_policy

# from tf_agents.drivers import dynamic_step_driver
# from tf_agents.metrics import metric_utils
# from tf_agents.metrics import tf_metrics

tf.compat.v1.enable_resource_variables()
tf.enable_eager_execution()

# Hyperparameters

fc_layer_params = (100,)
learning_rate = 1e-3
replay_buffer_capacity = 100000
batch_size = 64

num_eval_episodes = 10
num_iterations = 20000
collect_steps_per_iteration = 1
initial_collect_steps = 1000

log_interval = 200
eval_interval = 1000

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

def collect_step(environment, policy):
    time_step = environment.current_time_step()
    action_step = policy.action(time_step)
    next_time_step = environment.step(action_step.action)
    traj = trajectory.from_transition(time_step, action_step, next_time_step)

    # Add trajectory to the replay buffer
    replay_buffer.add_batch(traj)

# Set up Environment
train_env = T48Env()
env = T48Env()
train_tf_env = tf_py_environment.TFPyEnvironment(train_env)
tf_env = tf_py_environment.TFPyEnvironment(env)

log_step("Environment Information")
print("Confirm tf_env:", isinstance(tf_env, tf_environment.TFEnvironment))
print("TimeStep Specs:", tf_env.time_step_spec())
print("Action Specs:", tf_env.action_spec())

# Establish Network
log_step('Establishing Q Network')
q_net = q_network.QNetwork(
    train_tf_env.observation_spec(),
    train_tf_env.action_spec(),
    fc_layer_params=fc_layer_params)

# Instantiate optimizer, step_counter, and agent
# optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate)
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)

# train_step_counter = tf.compat.v2.Variable(0)
train_step_counter = tf.Variable(0)

log_step('Establishing DQN Agent')
tf_agent = dqn_agent.DqnAgent(
    train_tf_env.time_step_spec(),
    train_tf_env.action_spec(),
    q_network=q_net,
    optimizer=optimizer,
    td_errors_loss_fn=dqn_agent.element_wise_squared_loss,
    train_step_counter=train_step_counter)
tf_agent.initialize()

# Using default policies
log_step('Choosing Policies')
eval_policy = tf_agent.policy
collect_policy = tf_agent.collect_policy

random_policy = random_tf_policy.RandomTFPolicy(train_tf_env.time_step_spec(),
                                                train_tf_env.action_spec())

# Setting a replay buffer to store progress of net through steps
log_step('Starting Replay Buffer')
replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
    data_spec=tf_agent.collect_data_spec,
    batch_size=train_tf_env.batch_size,
    max_length=replay_buffer_capacity)

for _ in range(initial_collect_steps):
    collect_step(train_tf_env, random_policy)

dataset = replay_buffer.as_dataset(
    num_parallel_calls=3, sample_batch_size=batch_size, num_steps=2).prefetch(3)

iterator = iter(dataset)

# Running the agent
log_step('Initializing Training')

tf_agent.train = common.function(tf_agent.train)

# Reset the train step
tf_agent.train_step_counter.assign(0)

# Evaluate the agent's policy once before training.
avg_return = compute_avg_return(tf_env, tf_agent.policy, num_eval_episodes)
returns = [avg_return]

# Start train
for _ in range(num_iterations):

  # Collect a few steps using collect_policy and save to the replay buffer.
  for _ in range(collect_steps_per_iteration):
    collect_step(train_tf_env, tf_agent.collect_policy)

  # Sample a batch of data from the buffer and update the agent's network.
  experience, unused_info = next(iterator)
  train_loss = tf_agent.train(experience)

  step = tf_agent.train_step_counter.numpy()

  if step % log_interval == 0:
    print('step = {0}: loss = {1}'.format(step, train_loss.loss))

  if step % eval_interval == 0:
    avg_return = compute_avg_return(tf_env, tf_agent.policy, num_eval_episodes)
    print('step = {0}: Average Return = {1}'.format(step, avg_return))
    returns.append(avg_return)
