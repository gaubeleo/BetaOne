#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from beta_one import BetaOne, BetaZero

from random import shuffle, choice, random
from useful_tools import *
from schafkopf_helpers import *

class Player:
	def __init__(self, name):
		self.name = name

		self.state_space = 32*33
		self.action_space = 32
		self.ai = BetaZero(self.state_space, self.action_space)

	def deal(self, cards):
		self.value = 0
		self.last_state = None

		self.cards = cards

		self.state = np.zeros(self.state_space) # --> Binary?! (player-values for DQN)
		for c in self.cards:
			self.state[COMPLETE_DECK.index(c)*33] = 1

	def sort(self):
		self.cards.sort(key=lambda c: SUIT_DICT[c[1]], reverse=True)
		self.cards.sort(key=get_major_strength, reverse=True)

	def play(self, state, force_suit=None, exploit=0.5):
		legal_moves = [COMPLETE_DECK.index(c) for c in self.cards]
		if force_suit:
			if force_suit == trumpf_suit:
				legal_moves = [COMPLETE_DECK.index(c) for c in self.cards if c[0] in [u"U", u"O"] or c[1] == force_suit]
			else:
				legal_moves = [COMPLETE_DECK.index(c) for c in self.cards if c[0] not in [u"U", u"O"] and c[1] == force_suit]

		if not legal_moves:
			legal_moves = [COMPLETE_DECK.index(c) for c in self.cards]

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
		self.action[COMPLETE_DECK.index(self.cards[i])] = 1

		self.last_state = self.state.copy()
		self.last_action = self.action.copy()
		self.last_value = self.value

		return self.cards.pop(i)

	def collect_trick(self, value):
		self.value += value

	def encode_trick(trick):
		states = np.zeros()
		for c in COMPLETE_DECK:
			print c

	def __str__(self):
		return self.name + ":\t" + list2str(self.cards) + "\t" + str(self.value)


class Trick:
	def __init__(self, i, cards):
		self.i = i
		self.cards = cards

	def evaluate(self, turn):
		winner = 0
		for i in range(1, len(self.cards)):
			if get_strength(self.cards[i], trumpf_suit, self.cards[0][1]) > get_strength(self.cards[winner], trumpf_suit, self.cards[0][1]):
				winner = i

		self.winner = (turn+winner)%len(players)
		self.value = sum(map(lambda c: VALUE_DICT[c[0]], self.cards))

		return self.winner, self.value

	def __str__(self):
		return "T" + str(self.i) + ":\t\t" + list2str(self.cards) + "\t" + str(self.value) + "\t" + players[self.winner].name



suits = (u"♣", u"♠", u"♥", u"♦")
ranks = (u"7", u"8", u"9", u"U", u"O", u"K", u"1", u"A")
trumpf_suit = suits[2]

COMPLETE_DECK = []
for suit in suits:
	for rank in ranks:
		COMPLETE_DECK.append(rank+suit)

deck = list(COMPLETE_DECK)

players = map(Player, ("David", "Stefan", "Leo", "Alex"))
team = []
played_cards = []

def setup():
	for game in range(1):
		print "NEW GAME: "

		deal()
		if len(team) == 2:
			play()
			eval_game()
		else:
			print "GESPERRT"
		reset()
		print

def deal():
	global team 

	shuffle(deck)

	for i in range(len(players)):
		players[i].deal(deck[(i)*8:(i+1)*8])

	team = []
	for p in players:
		if u"A♣" in p.cards or u"O♦" in p.cards:
			team.append(p)

def play():
	global played_cards
	#assert(len(deck) == 32)

	for p in players:
		p.sort()
		print p
	print

	turn = 0
	played_cards = []

	for i in range(1, len(deck)+1):
		force_suit = None
		if len(played_cards)%len(players) != 0:
			first_card = played_cards[len(played_cards)/len(players)*len(players)]
			force_suit = first_card[1]
			if first_card[0] in [u"U", u"O"]:
				force_suit = trumpf_suit

		card = players[turn].play(None, force_suit=force_suit)
		played_cards.append(card)

		#remove card from players hand
		players[turn].state[COMPLETE_DECK.index(card)*33] = 0
		for p in players:
			#add card for everyone to see
			p.state[COMPLETE_DECK.index(card)*33+i] = 1
		
		turn = (turn + 1) % len(players)
		if len(played_cards)%len(players) == 0:
			trick = Trick(len(played_cards)/len(players), played_cards[-4:])
			winner, value = trick.evaluate(turn)
			players[winner].collect_trick(value)
			turn = winner

			print trick

def eval_game():
	print
	for p in players:
		print p
	print

	result = sum(map(lambda p: p.value, team))
	print team[0].name + " & " + team[1].name + (" lost " if result < 60 else " won ") + "(%d:%d)"%(result, 120-result)



def reset():
	players.append(players.pop(0))

	print 
	print "#########################################"
	print 


if __name__ == "__main__":
	setup()
	#print get_strength(u"8♥", trumpf_suit, u"♥")
	#print get_strength(u"K♦", trumpf_suit, u"♥")