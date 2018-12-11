#!/usr/bin/env python
# -*- coding: utf-8 -*-

from constants import *


def eval_trick(trick):
	assert(len(trick) == NUM_PLAYERS)

	force_suit = trick[0]//NUM_RANKS
	winner = 0
	winning_card = trick[0]

	for i in range(1, NUM_PLAYERS):
		if trick[i]//NUM_RANKS == force_suit and trick[i] > winning_card:
			winner = i
			winning_card = trick[i]

	trick_value = sum(map(lambda c: VALUE_DICT[c], trick))

	return winner, trick_value



class Player:
	def __init__(self, name):
		self.name = name

		self.reset()

		#self.ai = BetaZero(self.state_space, self.action_space)

	def reset(self):
		self.value = 0
		self.cards = []
		self.played = []

	def sort(self):
		sorted(self.cards)

	def play(self, force_suit=None):
		#return self.cards.pop(0)
		legal_moves = [CARDS.index(c) for c in self.cards]
		if force_suit:
			if force_suit == trumpf_suit:
				legal_moves = [CARDS.index(c) for c in self.cards if c[0] in [u"U", u"O"] or c[1] == force_suit]
			else:
				legal_moves = [CARDS.index(c) for c in self.cards if c[0] not in [u"U", u"O"] and c[1] == force_suit]

		if not legal_moves:
			legal_moves = [CARDS.index(c) for c in self.cards]

		#calc reward since last move and update Q-function
		if self.last_state != None:
			reward = self.value-self.last_value
			self.ai.updateQ(self.last_state, self.state, self.last_action, reward)

		# choose action
		self.action = np.zeros(32)
		if random() < exploit:
			i = choice(legal_moves)
		else:
			best_moves = self.ai.get_best_action(state)
			best_legal_moves = [i for i in best_moves if i in legal_moves]
			i = choice(best_legal_moves)	
		self.action[CARDS.index(self.cards[i])] = 1

		self.last_state = self.state.copy()
		self.last_action = self.action.copy()
		self.last_value = self.value

		return self.cards.pop(i)

	def __str__(self):
		return self.name + ":\t" + str(self.value) + "\t|\t{" + " ".join([CARDS[c] for c in self.cards]) + "}\t|\t" + " ".join([CARDS[c] for c in self.played])
