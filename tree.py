#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from hearts_helpers import *
from constants import *


I = 0

class Node:
	def __init__(self, state, values=None, i=0, p=0, trick=[]):
		self.state = state
		if not values:
			self.values = [0]*NUM_PLAYERS
		else:
			self.values = values

		self.i = i
		self.p = p
		self.trick = trick

		self.player_offset = self.p*NUM_CARDS
		self.iter_offset = (NUM_PLAYERS + self.i) * NUM_CARDS

		self.cards = [c for c in range(NUM_CARDS) if self.state[self.player_offset+c] == 1]
		self.legal_cards = [c for c in self.cards if trick == [] or c//NUM_RANKS == trick[0]//NUM_RANKS] 
		if self.legal_cards == []:
			self.legal_cards = self.cards

		self.children = []
		self.children_values = []
		self.player_values = []
		self.best_actions = None

		self.X_II = None
		self.X_PI = None
		self.Y_actions = None
		self.Y_values = None

		self.solved = False
		self.training_samples = False

	def solve(self):
		for c in self.legal_cards:
			sim_state = sim_action(self.state, self.p, c, self.i)
			next_trick, next_values, next_p = eval_action(self.trick, self.values, self.p, c)
			next_i = self.i+1

			if next_i == NUM_CARDS:
				assert(len(self.cards) == 1 and len(self.legal_cards) == 1)

				self.best_actions = [0]
				self.solved = True

				return next_values, self.best_actions
			else:
				child = Node(sim_state, values=next_values, i=next_i, p=next_p, trick=next_trick)

			self.children.append(child)

			# recursive!!
			child_values, _best_actions = child.solve()
			self.children_values.append(child_values)
			self.player_values.append(child_values[self.p])

		#TODO: train AI to predict the right actions


		#return the outcome of the game if every player plays (the first) nash equilibrium
		self.solved = True
		self.best_actions = [a for a in range(len(self.legal_cards)) if self.player_values[a] == min(self.player_values)]

		return self.children_values[self.best_actions[0]], self.best_actions

	def build_training_samples(self):
		assert(self.solved)

		if (not self.training_samples):
			II_input_state = self.state[II_MASKS[self.p]]
			PI_input_state = self.state[np.logical_not(II_MASKS[self.p])]

			X_II = II_input_state.reshape(1, II_input_state.shape[0])
			X_PI = PI_input_state.reshape(1, PI_input_state.shape[0])
			
			# illegal move --> 0 | legal move --> 0.5 | best moves --> 1.
			Y_actions = np.zeros((1, NUM_CARDS))
			for c in self.legal_cards:
				Y_actions[0, c] = 0
			for a in self.best_actions:
				Y_actions[0, self.legal_cards[a]] = 1.

			Y_values = np.array([[self.values[self.p]]])

			#accumulate training samples recursively
			for child in self.children:
				x_II, x_PI, y_actions, y_values = child.build_training_samples()

				X_II = np.concatenate((X_II, x_II), axis=0)
				X_PI = np.concatenate((X_PI, x_PI), axis=0)
				Y_actions = np.concatenate((Y_actions, y_actions), axis=0)
				Y_values = np.concatenate((Y_values, y_values), axis=0)

			self.X_II = X_II
			self.X_PI = X_PI
			self.Y_actions = Y_actions
			self.Y_values = Y_values

			self.training_samples = True

		return self.X_II, self.X_PI, self.Y_actions, self.Y_values

	def __str__(self):
		s = "P%i:\t%i"%(self.p, self.values[self.p]) 
		s += "\t|\t{" + " ".join([CARDS[c] for c in self.cards]) + "}"

		#if self.legal_cards:
		s += "\t|\t" + CARDS[self.legal_cards[self.best_actions[0]]]

		if self.children:
			s += "\n"+str(self.children[self.best_actions[0]])
		return s
