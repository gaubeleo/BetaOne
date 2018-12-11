#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np

from random import shuffle, choice, random

from tree import Node#, Leaf
from beta_one import BetaZero, BetaOne
from hearts_helpers import eval_trick, Player

from constants import *



#AI = BetaZero()
PLAYERS = map(Player, PLAYER_NAMES[:NUM_PLAYERS])
#num_players = 3

DECK = range(NUM_CARDS)

GAME_STATE = np.zeros(NUM_CARDS *  (NUM_PLAYERS + NUM_CARDS))


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
		GAME_STATE[p*NUM_CARDS+c] = 1
		p = p+1 if p < NUM_PLAYERS-1 else 0

	for p in PLAYERS:
		p.sort()

	#assert same output
	print_state(GAME_STATE)

def play(exploitation=0.25):
	p = 0
	r = Node(GAME_STATE.copy(), i=0, p=p)
	r.solve()

	for i in range(len(DECK)):
		augmented_game_state = GAME_STATE[p*NUM_CARDS:(p+1)*NUM_CARDS]
		if random() < exploitation:
			PI_features = AI.predict_features(augmented_game_state)
			predicted_features = AI.predict_features(augmented_game_state)
			AI.feed(predicted_game_state)

		c = PLAYERS[p].play(GAME_STATE)
		GAME_STATE[p*NUM_CARDS+c] = 0
		GAME_STATE[(NUM_PLAYERS+i)*NUM_CARDS+c] = 1

		if (i+1)%NUM_PLAYERS == 0:
			collect_tick()
			p = "winner"
		else:
			p = p+1 if p < len(PLAYERS)-1 else 0


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
	#		if s[p*NUM_CARDS+c] == 1:
	#			sys.stdout.write(CARDS[c])
	#	print


if __name__ == "__main__":
	setup()
	#print eval_trick(map(lambda c: CARDS.index(c), ["K♣", "J♠", "A♠"]))
