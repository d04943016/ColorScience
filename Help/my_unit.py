#!/usr/bin/env python3
# Copyright (c) 2017 Wei-Kai Lee. All rights reserved

# coding=utf-8
# -*- coding: utf8 -*-

"""
my_unit provides a function to change the standard unit to another standard unit

>>> unit1str = "cm"
>>> unit2str = "m"
>>> unit2unit(unit1str[0:(len(unit1str)-1)], unit2str[0:(len(unit2str)-1)]) 
0.01
>>> unit2unit("c","")
0.01
>>> unit2unit("k","c")
100000.0

"""

import collections

unitdict = collections.defaultdict(list)
unitdict['G'] = 1e9
unitdict['Giga'] = 1e9
unitdict['M'] = 1e6
unitdict['Mega'] = 1e6
unitdict['k'] = 1e3
unitdict['kilo'] = 1e3
unitdict['c'] = 1e-2
unitdict['centi'] = 1e-2
unitdict['m'] = 1e-3
unitdict['mili'] = 1e-3
unitdict['u'] = 1e-6
unitdict['miro'] = 1e-6
unitdict['n'] = 1e-9
unitdict['nano'] = 1e-9
unitdict['p'] = 1e-12
unitdict['pico'] = 1e-12
unitdict['f'] = 1e-15
unitdict['femto'] = 1e-15
unitdict['ONE'] = 1


def unit2unit(unit1str, unit2str):
    unit1str = unit1str if unit1str in unitdict.keys() else "ONE"
    unit2str = unit2str if unit2str in unitdict.keys() else "ONE"
    return unitdict[unit1str]/unitdict[unit2str]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
