from spinup import ddpg, ppo
from spinup.utils.test_policy import load_policy, run_policy
import tensorflow as tf
import gym
import os

# env_fn = lambda :  gym.make('gym_snake:snake-v0')
#
# ac_kwargs = dict(hidden_sizes=[128, 64, 32],
#                  activation=tf.keras.activations.relu)
#
# logger_kwargs = dict(output_dir=os.getcwd(),
#                      exp_name='SnakeRLAgent')
#
# ppo(env_fn=env_fn,
#     ac_kwargs=ac_kwargs,
#     steps_per_epoch=500,
#     max_ep_len=1000,
#     epochs=20,
#     logger_kwargs=logger_kwargs)
#
#
_, get_action = load_policy(os.getcwd())
env = gym.make('gym_snake:snake-v0')
run_policy(env, get_action)