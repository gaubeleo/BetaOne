#!/usr/bin/env python
# -*- coding: utf-8 -*-

SUITS = ("♣", "♠", "♥") #, "♦"
RANKS = ("J", "Q", "K", "A") #"1",  

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

NUM_SUITS = len(SUITS)
NUM_RANKS = len(RANKS)
NUM_CARDS = len(CARDS)

NUM_PLAYERS = 3
PLAYER_NAMES = ["Flo", "Tim", "Leo", "Max", "Ami", "Philipp", "Freddi"]

assert(NUM_PLAYERS <= len(PLAYER_NAMES))