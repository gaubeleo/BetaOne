#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from hearts_helpers import eval_trick
from constants import *

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
		#print self.cards
		self.legal_cards = [c for c in self.cards if trick == [] or c//NUM_RANKS == trick[0]//NUM_RANKS] 
		if self.legal_cards == []:
			self.legal_cards = self.cards

		self.children = []
		self.children_values = []
		self.player_values = []
		self.best_actions = None

		self.X = None
		self.Y_actions = None
		self.Y_values = None

		self.solved = False
		self.training_samples = False

	def solve(self):
		for c in self.legal_cards:
			sim_state, next_values, next_i, next_p, next_trick = self.sim_action(c)

			if next_i == NUM_CARDS:
				assert(len(self.cards) == 1 and len(self.legal_cards) == 1)

				self.best_actions = [0]

				self.solved = True
				return next_values, 0
			else:
				child = Node(sim_state, values=next_values, i=next_i, p=next_p, trick=next_trick)

			self.children.append(child)

			# recursive!!
			child_values, _best_actions = child.solve()
			self.children_values.append(child_values)
			self.player_values.append(child_values[self.p])


		#TODO: train AI to predict the right actions


		#return the outcome of the game if every player plays (the first) nash equilibrium
		self.best_actions = [a for a in range(len(self.legal_cards)) if self.player_values[a] == min(self.player_values)]

		self.solved = True
		return self.children_values[self.best_actions[0]], self.best_actions


	def sim_action(self, c):
		global PLAYERS

		assert(self.state[self.player_offset+c] == 1)

		sim_state = self.state.copy()
		sim_state[self.player_offset+c] = 0

		sim_state[self.iter_offset+c] = 1

		next_values = self.values[:]
		next_trick = self.trick[:]
		next_trick.append(c)
		next_p = (self.p+1) % NUM_PLAYERS

		# after {#players} cards evaluate trick - determine winner - value
		if len(self.trick)+1 == NUM_PLAYERS:
			p_offset, trick_value = eval_trick(next_trick)
			next_p = (next_p+p_offset) % NUM_PLAYERS
			next_values[next_p] += trick_value
			#"Durchmarsch"
			if next_values[next_p] == MAX_VALUE:
				for i in range(len(next_values)):
					next_values[i] = MAX_VALUE
				next_values[next_p] = 0
			next_trick = []

		return sim_state, next_values, self.i+1, next_p, next_trick

	def build_training_samples(self):
		assert(self.solved)

		if (not self.training_samples):
			X = self.state.reshape(1, self.state.shape[0])
			
			# illeagal move --> 0 | legal move --> 0.5 | best moves --> 1.
			Y_actions = np.zeros((1, NUM_CARDS))
			for c in self.legal_cards:
				Y_actions[0, c] = 0.5
			for a in self.best_actions:
				Y_actions[0, self.legal_cards[a]] = 1.

			Y_values = np.array([[self.values[self.p]]])

			#accumulate training samples recursively
			for child in self.children:
				x, y_actions, y_values = child.build_training_samples()
				X = np.concatenate((X, x), axis=0)
				Y_actions = np.concatenate((Y_actions, y_actions), axis=0)
				Y_values = np.concatenate((Y_values, y_values), axis=0)

			self.X = X
			self.Y_actions = Y_actions
			self.Y_values = Y_values

			self.training_samples = True

		return self.X, self.Y_actions, self.Y_values

	def __str__(self):
		s = "P%i:\t%i"%(self.p, self.values[self.p]) 
		s += "\t|\t{" + " ".join([CARDS[c] for c in self.cards]) + "}"

		#if self.legal_cards:
		s += "\t|\t" + CARDS[self.legal_cards[self.best_actions[0]]]

		if self.children:
			s += "\n"+str(self.children[self.best_actions[0]])
		return s
