#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np

from random import shuffle, choice, random

from tree import Node
from beta_one import BetaZero, BetaOne
from hearts_helpers import *

from constants import *


AI = BetaOne()
PLAYERS = map(Player, PLAYER_NAMES[:NUM_PLAYERS])
#num_players = 3

DECK = range(NUM_CARDS)

GAME_STATE = np.zeros(GAME_STATE_SIZE)
P = 0
ITER = 0
TRICK = []
VALUES = [0]*NUM_PLAYERS

def setup():
	deal()
	play_random((NUM_RANKS-4) * NUM_PLAYERS)
	test_root = solve()
	reset()
	#test(test_root)
	predict_II(test_root)

	for game in range(1000):
		#print "NEW GAME: "

		deal()
		play_random((NUM_RANKS-4) * NUM_PLAYERS)
		root = solve()
		train_II(root)
		if game % 1 == 0:
			#test(test_root)
			predict_II(test_root)

		reset()

		#print 
		#print "#########################################"
		#print 


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
	#print_state(GAME_STATE)

def solve():
	root = Node(GAME_STATE.copy(), i=ITER, p=P)
	root.solve()

	return root

def train_PI(root):
	X_II, X_PI, Y_actions, Y_values = root.build_training_samples()
	AI.train_PI(X_II, X_PI, Y_actions)

def test_PI(test_root):
	X_II_test, X_PI_test, Y_actions_test, Y_values_test = test_root.build_training_samples()
	print AI.test_PI(X_II_test, X_PI_test, Y_actions_test)

def predict_PI(test_root):
	X_II_test, X_PI_test, Y_actions_test, Y_values_test = test_root.build_training_samples()
	print AI.predict_PI(X_II_test, X_PI_test, Y_actions_test)


def train_II(root):
	X_II, _X_PI, Y_actions, Y_values = root.build_training_samples()
	AI.train_II(X_II, Y_actions)

def test_II(test_root):
	X_II_test, _X_PI_test, Y_actions_test, Y_values_test = test_root.build_training_samples()
	print AI.test_II(X_II_test, Y_actions_test)

def predict_II(test_root):
	X_II_test, _X_PI_test, Y_actions_test, Y_values_test = test_root.build_training_samples()
	print AI.predict_II(X_II_test, Y_actions_test)


def play_random(iterations):
	global GAME_STATE, P, ITER, TRICK, VALUES

	#ASSERT playing from the start!!
	iter_offset = (NUM_PLAYERS) * NUM_CARDS
	assert(not np.any(GAME_STATE[iter_offset:]))

	for ITER in range(1, iterations+1, 1):
		c = PLAYERS[P].play_random(TRICK)
		GAME_STATE = play_action(GAME_STATE, P, c, ITER)
		TRICK, VALUES, P = eval_action(TRICK, VALUES, P, c)

	#print_state()

def play(exploitation=1.):
	p = 0

	for i in range(len(DECK)):
		if random() < exploitation:
			#PI_features = AI.predict_features(augmented_game_state)
			#predicted_features = AI.predict_features(augmented_game_state)
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
	global GAME_STATE, P, ITER, TRICK, VALUES, PLAYERS

	for p in PLAYERS:
		p.reset()

	PLAYERS.append(PLAYERS.pop(0))

	GAME_STATE = np.zeros(NUM_CARDS * (NUM_PLAYERS + NUM_CARDS))
	P = 0
	ITER = 0
	TRICK = []
	VALUES = [0]*NUM_PLAYERS

def print_state(s=None):
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
