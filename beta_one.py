#!/usr/bin/env python
# -*- coding: utf-8 -*-


import random
import numpy as np

from keras.models import Sequential
from keras.layers import Dense


class BetaOne:
	def __init__(self, state_size, action_size):
		self.build_layers()
		self.build_models()

	def build_layers(self):
		self.PI_gs_layer = Dense(len(CARDS) * POS_POS)
		self.II_gs_layer = Dense(len(CARDS) * (len(CARDS) + 1))

		self.feature_layer = Dense(len(CARDS) * POS_POS / len(RANKS))
		self.action_layer = Dense(len(CARDS))

	def build_models(self):
		self.PI_model = Sequential()
		self.II_model = Sequential()
		
		self.PI_model.add(self.PI_gs_layer)
		self.II_model.add(self.II_gs_layer)

		self.PI_model.add(self.feature_layer)
		self.II_model.add(self.feature_layer)

		self.PI_model.add(self.action_layer)
		self.II_model.add(self.action_layer)

		self.PI_model.compile()
		self.II_model.compile()

	def feed(self):
		pass

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
