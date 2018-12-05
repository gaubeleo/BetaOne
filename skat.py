#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import shuffle
import numpy as np

class Player:
	def __init__(self, name):
		self.name = name
		self.cards = []

		self.ai = BetaOne()


suits = ("♣", "♠", "♥", "♦")
ranks = ("7", "8", "9", "0", "J", "D", "K", "A")
deck = []
for suit in suits:
	for rank in ranks:
		deck.append(rank+suit)

players = map(Player, ("Tim", "Flo", "Leo"))


def setup():
	shuffle(deck)
	deal()
	player = bid()
	player.isPlayer = True
	play()

def deal():
	for i in range(len(players)):
		players[i].cards = deck[(i)*10:(i+1)*10]

	skat = deck[-2:]

def bid():
	return random.choice(players)

if __name__ == "__main__":
	setup()
