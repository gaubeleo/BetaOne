#!/usr/bin/env python
# -*- coding: utf-8 -*-


VALUE_DICT = {
	u"A": 11,
	u"1": 10,
	u"K": 4,
	u"O": 3,
	u"U": 2,
	u"9": 0,
	u"8": 0,
	u"7": 0
}

STRENGTH_DICT = {
	u"A": 7,
	u"1": 6,
	u"K": 5,
	u"O": 4,
	u"U": 3,
	u"9": 2,
	u"8": 1,
	u"7": 0
}

SUIT_DICT = {
	u"♣": 3, 
	u"♠": 2, 
	u"♥": 1, 
	u"♦": 0
}

def get_major_strength(c):
	if c[0] == u"O":
		return 3
	elif c[0] == u"U":
		return 2
	elif c[1] == u"♥":
		return 1
	return 0

def get_strength(c, t, s):
	major = 0
	if c[0] == u"O":
		major = 4
	elif c[0] == u"U":
		major = 3
	elif c[1] == t:
		major = 2
	elif c[1] == s:
		major = 1

	minor = 0
	if major >= 3:
		minor = SUIT_DICT[c[1]]
	else:
		minor = STRENGTH_DICT[c[0]]

	return major*10 + minor


