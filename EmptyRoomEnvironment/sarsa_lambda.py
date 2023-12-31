# -*- coding: utf-8 -*-
"""Sarsa_Lambda.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AfYibGZ4oGCJ3y8ApZL2e5vlNOr6KDfZ
"""

import gym
import numpy as np
!pip install gym-minigrid
import random
import matplotlib.pyplot as plt

#env = gym.make('MiniGrid-Empty-6x6-v0',render_mode='rgb_array')
env = gym.make('MiniGrid-Empty-8x8-v0',render_mode='rgb_array')
env.reset()
E = {}
Q = {}

number_of_episodes = 150;

epsilon = 1
alpha = 0.1
gamma = 0.99;
lambda_ = 0.9
total_episodes = []
steps_required = []
def epsilon_greedy(epsilon,state_space):
  if np.random.rand() < epsilon:
    action = np.random.randint(0,3)
  else:
    action = np.argmax(Q[state_space])
  return action

for i in range(number_of_episodes+20):
  env.reset()
  truncation = False
  state = (1,1,0)
  state_space = state
  done = False
  steps = 1
  policy = []
  while not done and not truncation:
    state_space = state
    if state not in Q:
      Q[state_space] = np.zeros(3)
      E[state_space] = np.zeros(3)

    action = epsilon_greedy(epsilon,state_space)
    policy.append(action)
    nxt_obs,reward,done,truncation,info = env.step(action)
    new_state = env.agent_pos
    new_direction = env.agent_dir
    new_state_space = (new_state[0],new_state[1],new_direction)

    if new_state_space not in Q:
      Q[new_state_space] = np.zeros(3)
      E[new_state_space] = np.zeros(3)

    next_action = epsilon_greedy(epsilon,new_state_space)
    delta = reward + gamma*(Q[new_state_space][next_action]) - Q[state_space][action]
    E[state_space][action] = E[state_space][action] + 1

    for nos in Q.keys():
      for j in range(3):
        Q[nos][j] = Q[nos][j] + alpha*delta*E[nos][j]
        E[nos][j] = gamma * lambda_ * E[nos][j]

    state = new_state_space
    action = next_action
    epsilon = (-i/number_of_episodes) + 1
    steps += 1
  total_episodes.append(i+1)
  steps_required.append(steps)




# print(total_episodes)
# print(steps_required)
plt.title("MiniGrid-Empty-8x8-v0 using SARSA-Lambda")
#plt.title("MiniGrid-Empty-6x6-v0 using SARSA-Lambda")
plt.plot(total_episodes,steps_required)
plt.xlabel("Number of episodes")
plt.ylabel("Steps to reach goal")
plt.show()
print('policy :',policy)