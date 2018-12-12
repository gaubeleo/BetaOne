#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')

from keras.models import Model
from keras.layers import Dense, Input, concatenate

sys.stderr = stderr


import random
import numpy as np

from constants import *


class BetaOne:
	def __init__(self):
		self.build_models()

	def build_models(self):
		#batch_size=...
		II_input_dim = NUM_CARDS * (NUM_CARDS + 1)
		PI_input_dim = NUM_CARDS * (NUM_PLAYERS-1)

		#print II_input_dim, PI_input_dim

		II_input_layer = Input(shape=(II_input_dim,), name="II_inputs")
		PI_input_layer = Input(shape=(PI_input_dim,), name="PI_inputs")
		
		#TODO --> intermediate layer

		II_feature_layer = Dense(NUM_FEATURES, activation="tanh", name="II_features")(II_input_layer)
		PI_feature_layer = Dense(NUM_FEATURES, activation="tanh", name="PI_features")(PI_input_layer)


		#merge_features = concatenate([II_input_layer, PI_input_layer])
		merge_features = concatenate([II_feature_layer, PI_feature_layer])

		II_action_layer = Dense(NUM_CARDS, activation="relu", name="II_actions")(II_feature_layer)
		PI_action_layer = Dense(NUM_CARDS, activation="relu", name="PI_actions")(merge_features)


		self.II_model = Model(inputs=II_input_layer, outputs=II_action_layer)
		self.PI_model = Model(inputs=[II_input_layer, PI_input_layer], outputs=PI_action_layer)

		self.II_model.compile(loss='mean_squared_error', optimizer='sgd')
		self.PI_model.compile(loss='mean_squared_error', optimizer='sgd')

	def train_PI(self, X_II, X_PI, Y):
		train_results = train(self.PI_model, [X_II, X_PI], Y)

		return train_results

	def test_PI(self, X_II, X_PI, Y):
		test_results = test(self.PI_model, [X_II, X_PI], Y)

		return test_results

	def predict_PI(self, X_II, X_PI, Y):
		prediction_results = predict(self.PI_model, [X_II, X_PI], Y)

		return prediction_results

	def train_II(self, X, Y):
		train_results = train(self.II_model, X, Y)

		return train_results

	def test_II(self, X, Y):
		test_results = test(self.II_model, X, Y)

		return test_results

	def predict_II(self, X, Y):
		prediction_results = predict(self.II_model, X, Y)

		return prediction_results

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

def predict(model, X, Y):
	predictions = model.predict(X)

	correct_predictions = 0
	for prediction, gt in zip(predictions, Y):
		if gt[np.argmax(prediction)] == 1:
			correct_predictions += 1

	return correct_predictions/float(len(Y))


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
