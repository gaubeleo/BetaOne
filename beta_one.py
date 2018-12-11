#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')

from keras.models import Sequential
from keras.layers import Dense

sys.stderr = stderr


import random
import numpy as np

from constants import *


class BetaOne:
	def __init__(self):
		self.build_layers()
		self.build_models()

	def build_layers(self):
		#convolutional layers?! chess paper?
		self.PI_gs_layer = Dense(NUM_CARDS * (NUM_CARDS + NUM_PLAYERS))
		self.II_gs_layer = Dense(NUM_CARDS * (NUM_CARDS + 1))

		#TODO --> intermediate layer
		self.PI_int_layer = Dense(NUM_CARDS * (NUM_CARDS + NUM_PLAYERS)*2)

		self.feature_layer = Dense(NUM_FEATURES)
		self.action_layer = Dense(NUM_CARDS)

	def build_models(self):
		self.PI_model = Sequential()
		self.II_model = Sequential()
		
		self.PI_model.add(self.PI_gs_layer)
		self.II_model.add(self.II_gs_layer)

		#TODO --> intermediate layer
		#self.PI_model.add(self.PI_int_layer)

		self.PI_model.add(self.feature_layer)
		self.II_model.add(self.feature_layer)

		self.PI_model.add(self.action_layer)
		self.II_model.add(self.action_layer)

		self.PI_model.compile(loss='mean_squared_error', optimizer='sgd')
		self.II_model.compile(loss='mean_squared_error', optimizer='sgd')

	def train_PI(self, X, Y):
		train_results = train(self.PI_model, X, Y)

		return train_results

	def test_PI(self, X, Y):
		test_results = test(self.PI_model, X, Y)

		return test_results

	def feed_PI(self, X, Y, val_share=0.2):
		split = int(X.shape[0]*val_share)

		train_X, test_X = np.split(X, [split])
		train_Y, test_Y = np.split(Y, [split])

		before_results = test(self.PI_model, test_X, test_Y)
		train_results = train(self.PI_model, train_X, train_Y)
		after_results = test(self.PI_model, test_X, test_Y)


def train(model, X, Y):
	return model.fit(X, Y, verbose=0)


def test(model, X, Y):
	return model.evaluate(X, Y, verbose=0)


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
