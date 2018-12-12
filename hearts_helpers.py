#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from random import choice

from constants import *


def play_action(state, p, c, i):
	player_offset = p*NUM_CARDS
	iter_offset = (NUM_PLAYERS + i) * NUM_CARDS

	assert(state[player_offset+c] == 1)

	sim_state = state.copy()
	sim_state[player_offset+c] = 0

	sim_state[iter_offset+c] = 1

	return sim_state

def sim_action(state, p, c, i):
	return play_action(state.copy(), p, c, i)


def eval_action(trick, values, p, c):
	next_values = values[:]
	next_trick = trick[:]
	next_trick.append(c)
	next_p = (p+1) % NUM_PLAYERS

	# after {#players} cards evaluate trick - determine winner - value
	if len(next_trick) == NUM_PLAYERS:
		p_offset, trick_value = eval_trick(next_trick)
		next_p = (next_p+p_offset) % NUM_PLAYERS
		next_values[next_p] += trick_value
		#"Durchmarsch"
		if next_values[next_p] == MAX_VALUE:
			for i in range(len(next_values)):
				next_values[i] = MAX_VALUE
			next_values[next_p] = 0
		next_trick = []

	return next_trick, next_values, next_p


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


def conceal_state(s, p):
	return np.concatenate((s[p*NUM_CARDS:(p+1)*NUM_CARDS], s[NUM_PLAYERS*NUM_CARDS:]), axis=0)


class Player:
	def __init__(self, name):
		self.name = name

		self.reset()

		#self.ai = BetaZero(self.state_space, self.action_space)

	def reset(self):
		self.value = 0
		self.cards = []
		self.played_cards = []

	def sort(self):
		sorted(self.cards)

	def play_random(self, trick):
		assert(self.cards != [])

		legal_cards = [c for c in self.cards if trick == [] or c//NUM_RANKS == trick[0]//NUM_RANKS] 
		if legal_cards == []:
			legal_cards = self.cards

		c = choice(legal_cards)
		self.cards.remove(c)

		self.played_cards.append(c)

		return c

	def __str__(self):
		return self.name + ":\t" + str(self.value) + "\t|\t{" + " ".join([CARDS[c] for c in self.cards]) + "}\t|\t" + " ".join([CARDS[c] for c in self.played_cards])
