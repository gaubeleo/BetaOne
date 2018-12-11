#!/usr/bin/env python
# -*- coding: utf-8 -*-


import random
import numpy as np
#import keras


class BetaOne:
	def __init__(self, state_size, action_size):
		pass

	def evaluate(self, state, actions):
		return random.choice(action)


class BetaZero:
	def __init__(self, state_size, action_size, lr=0.1, df=0.9): 
		self.lr = lr
		self.df = df
		self.state_size = state_size
		self.N = np.zeros(state_size)					# #_visited_states (only temporal difference?)
		self.Q = np.zeros((state_size, action_size))	#expected reward

		self.action_size = action_size

	def updateQ(self, state, new_state, action, reward):	
		self.Q[state][action] = (1.-self.lr)*self.Q[state][action] + self.lr*(reward + self.df*max(self.Q[new_state]))

	def get_best_action(self, state):
		m = max(self.Q[state])
		return [i for i, j in enumerate(self.Q[state]) if j == m]
