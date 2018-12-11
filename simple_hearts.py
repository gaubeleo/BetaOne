#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np

from random import shuffle, choice, random

from beta_one import BetaZero
#from tree import Node, Leaf


class Node:
	def __init__(self, state, values=None, i=0, p=0, trick=[]):
		self.state = state
		if not values:
			self.values = [0]*len(PLAYERS)
		else:
			self.values = values

		self.i = i
		self.p = p
		self.trick = trick

		self.player_offset = self.p*len(CARDS)
		self.iter_offset = (len(PLAYERS) + self.i) * len(CARDS)

		self.cards = [c for c in range(len(CARDS)) if self.state[self.player_offset+c] == 1]
		#print self.cards
		self.legal_cards = [c for c in self.cards if trick == [] or c//len(RANKS) == trick[0]//len(RANKS)] 
		if self.legal_cards == []:
			self.legal_cards = self.cards

		self.children = []
		self.children_values = []
		self.player_values = []
		self.best_actions = None

	def solve(self):
		global CARDS

		for c in self.legal_cards:
			sim_state, next_values, next_i, next_p, next_trick = self.sim_action(c)

			if next_i == len(CARDS):
				assert(len(self.cards) == 1 and len(self.legal_cards) == 1)

				self.best_actions = [0]
				return next_values, 0
			else:
				child = Node(sim_state, values=next_values, i=next_i, p=next_p, trick=next_trick)

			self.children.append(child)

			# recursive!!
			child_values, _best_actions = child.solve()
			self.children_values.append(child_values)
			self.player_values.append(child_values[self.p])

		#return the outcome of the game if every player plays (the first) nash equilibrium
		self.best_actions = [a for a in range(len(self.legal_cards)) if self.player_values[a] == min(self.player_values)]
		return self.children_values[self.best_actions[0]], self.best_actions

	def sim_action(self, c):
		global PLAYERS

		assert(self.state[self.player_offset+c] == 1)

		sim_state = self.state.copy()
		sim_state[self.player_offset+c] = 0

		sim_state[self.iter_offset+c] = 1

		next_values = list(self.values)
		next_trick = list(self.trick)
		next_trick.append(c)
		next_p = (self.p+1) % len(PLAYERS)

		# after {#players} cards evaluate trick - determine winner - value
		if len(self.trick)+1 == len(PLAYERS):
			p_offset, trick_value = eval_trick(next_trick)
			next_p = (next_p+p_offset) % len(PLAYERS)
			next_values[next_p] += trick_value
			next_trick = []

		return sim_state, next_values, self.i+1, next_p, next_trick

	def __str__(self):
		s = "Player %i:\t%i"%(self.p, self.values[self.p]) 
		s += "\t|\t{" + " ".join([CARDS[c] for c in self.cards]) + "}"

		if self.legal_cards:
			s += "\t|\t" + CARDS[self.legal_cards[self.best_actions[0]]]

		if self.children:
			s += "\n"+str(self.children[self.best_actions[0]])
		return s


#class Leaf(Node):
#	def __init__(self, state, values, i, p, trick):
#		Node.__init__(self, state, values=values, i=i, p=p, trick=trick)
#
#		assert(len(self.cards) == 1 and len(self.legal_cards) == 1)
#
#	def solve(self):
#		self.sim_action
#
#		return self.children_values


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
		return self.cards.pop(0)
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


def eval_trick(trick):
	assert(len(trick) == len(PLAYERS))

	force_suit = trick[0]//len(RANKS)
	winner = 0
	winning_card = trick[0]

	for i in range(1, len(PLAYERS)):
		if trick[i]//len(RANKS) == force_suit and trick[i] > winning_card:
			winner = i
			winning_card = trick[i]

	trick_value = sum(map(lambda c: VALUE_DICT[c], trick))

	return winner, trick_value




#AI = BetaZero()
PLAYERS = map(Player, ["Flo", "Tim", "Leo"])
#num_players = 3

SUITS = ("♣", "♠", "♥") #, "♦"
RANKS = ("1", "J", "Q", "K", "A") #"J", 

CARDS = []
VALUE_DICT = []
for suit in SUITS:
	for rank in RANKS:
		CARDS.append(rank+suit)

		if suit == "♥":
			VALUE_DICT.append(1)
		elif suit == "♠" and rank == "Q":
			VALUE_DICT.append(len(RANKS))
		else:
			VALUE_DICT.append(0)

DECK = range(len(CARDS))

POS_POS = (len(PLAYERS) + len(CARDS))
GAME_STATE = np.zeros(len(CARDS) * POS_POS)


def setup():
	for game in range(1):
		print "NEW GAME: "

		deal()
		play()
		#eval_game()

		reset()

		print 
		print "#########################################"
		print 


def deal():
	shuffle(DECK)

	p = 0
	for c in DECK:
		PLAYERS[p].cards.append(c)
		GAME_STATE[p*len(CARDS)+c] = 1
		p = p+1 if p < len(PLAYERS)-1 else 0

	for p in PLAYERS:
		p.sort()

	#assert same output
	print_state(GAME_STATE)

def play():
	p = 0
	solve(GAME_STATE, 0, p)

	return

	for i in range(len(DECK)):
		c = PLAYERS[p].play(GAME_STATE)
		GAME_STATE[p*len(CARDS)+c] = 0
		GAME_STATE[(len(PLAYERS)+i)*len(CARDS)+c] = 1

		if (i+1)%len(PLAYERS) == 0:
			collect_tick()
			p = "winner"
		else:
			p = p+1 if p < len(PLAYERS)-1 else 0

def solve(s, i, p):
	r = Node(s.copy(), i=i, p=p)
	print r.solve()


def reset():
	for p in PLAYERS:
		p.reset()

	PLAYERS.append(PLAYERS.pop(0))


def print_state(s):
	for p in PLAYERS:
		print p

	#print
	#for p in range(len(PLAYERS)):
	#	for c in DECK:
	#		if s[p*len(CARDS)+c] == 1:
	#			sys.stdout.write(CARDS[c])
	#	print


if __name__ == "__main__":
	setup()
	#print eval_trick(map(lambda c: CARDS.index(c), ["K♣", "J♠", "A♠"]))
