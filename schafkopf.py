#!/usr/bin/env python
# -*- coding: utf-8 -*-

from beta_one import BetaOne

from random import shuffle, choice
from useful_tools import *
from schafkopf_helpers import *

class Player:
	def __init__(self, name):
		self.name = name
		self.ai = BetaOne()

		self.reset()

	def deal(self, cards):
		self.cards += cards

	def sort(self):
		self.cards.sort(key=lambda c: SUIT_DICT[c[1]], reverse=True)
		self.cards.sort(key=get_major_strength, reverse=True)

	def reset(self):
		self.value = 0
		self.cards = []

	def play(self, state, force_suit=None):
		legal_moves = range(len(self.cards))
		if force_suit:
			if force_suit == trumpf_suit:
				legal_moves = [i for i in range(len(self.cards)) if self.cards[i][0] in [u"U", u"O"] or self.cards[i][1] == force_suit]
			else:
				legal_moves = [i for i in range(len(self.cards)) if self.cards[i][0] not in [u"U", u"O"] and self.cards[i][1] == force_suit]

		if not legal_moves:
			legal_moves = range(len(self.cards))

		return self.cards.pop(choice(legal_moves))

	def collect_trick(self, value):
		self.value += value

	def encode_state():
		pass


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

deck = []
for suit in suits:
	for rank in ranks:
		deck.append(rank+suit)

players = map(Player, ("David", "Stefan", "Leo", "Alex"))
team = []

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
	#assert(len(deck) == 32)

	for p in players:
		p.sort()
		print p
	print

	turn = 0
	played_cards = []

	for i in range(len(deck)):
		force_suit = None
		if len(played_cards)%len(players) != 0:
			first_card = played_cards[len(played_cards)/len(players)*len(players)]
			force_suit = first_card[1]
			if first_card[0] in [u"U", u"O"]:
				force_suit = trumpf_suit

		card = players[turn].play(None, force_suit=force_suit)
		played_cards.append(card)
		
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

	for p in players:
		p.reset()

	print 
	print "#########################################"
	print 


if __name__ == "__main__":
	setup()
	#print get_strength(u"8♥", trumpf_suit, u"♥")
	#print get_strength(u"K♦", trumpf_suit, u"♥")