#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

SUITS = ("♣", "♠", "♥") #, "♦"
#RANKS = ("J", "Q", "K", "A")  
#RANKS = ("7", "8", "9", "1", "J", "Q", "K", "A")  
RANKS = ("2", "3", "4", "5", "6", "7", "8", "9", "1", "J", "Q", "K", "A")  

CARDS = []
VALUE_DICT = []
MAX_VALUE = 0
for suit in SUITS:
	for rank in RANKS:
		CARDS.append(rank+suit)

		if suit == "♥":
			VALUE_DICT.append(1)
			MAX_VALUE += 1
		elif suit == "♠" and rank == "Q":
			VALUE_DICT.append(len(RANKS))
			MAX_VALUE += len(RANKS)
		else:
			VALUE_DICT.append(0)

del rank
del suit


NUM_SUITS = len(SUITS)
NUM_RANKS = len(RANKS)
NUM_CARDS = len(CARDS)

NUM_PLAYERS = 3
PLAYER_NAMES = ["Flo", "Tim", "Leo", "Max", "Ami", "Philipp", "Freddi"]

GAME_STATE_SIZE = NUM_CARDS * (NUM_PLAYERS + NUM_CARDS)

II_MASKS = []
for p in range(NUM_PLAYERS):
	mask = np.full(GAME_STATE_SIZE, True, dtype=bool)
	mask[:p*NUM_CARDS] = False
	mask[(p+1)*NUM_CARDS:NUM_PLAYERS*NUM_CARDS] = False

	II_MASKS.append(mask)

mask = None
del mask

assert(NUM_PLAYERS <= len(PLAYER_NAMES))

NUM_FEATURES = NUM_CARDS * (NUM_CARDS + NUM_PLAYERS) // NUM_RANKS #TODO --> AUTO_ML
