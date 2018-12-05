#!/usr/bin/env python
# -*- coding: utf-8 -*-


def list2str(list):
	list_str = ""
	for e in list:
		list_str += " "+e.encode("utf-8")
	return "["+list_str+" ]"