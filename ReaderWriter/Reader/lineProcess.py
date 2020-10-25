#!/usr/bin/env python3
# Copyright (c) 2018 Wei-Kai Lee. All rights reserved

# coding=utf-8
# -*- coding: utf8 -*-
import sys
import os

# my module
from .readfile import strMultiSepSplit

def LineTagSpliter(line,preStr='[',postStr=']',colNum=-1):
    """
    >>> line = "[EML][HATCN][NK]./Example/"
    >>> TagList, StrList = LineTagSpliter(line)
    >>> print(TagList)
    ['EML', 'HATCN', 'NK']
    >>> print(StrList)
    ./Example/
    >>> TagList, StrList = LineTagSpliter(line,colNum=2)
    >>> print(TagList)
    ['EML', 'HATCN']
    >>> print(StrList)
    [NK]./Example/
    """
    count = 0
    indexPre = line.find(preStr)
    indexPost = line.find(postStr)
    TagList = []
    Remain = line
    while (indexPre!=-1 and indexPost!=-1) and (colNum==-1 or count<colNum):
        TagList.append(line[indexPre+1:indexPost:])
        Remain = line[indexPost+1::]
        indexPre = line.find(preStr,indexPost+1)
        indexPost = line.find(postStr,indexPost+1)
        count +=1
    return TagList, Remain


if __name__ == '__main__':
    import doctest
    doctest.testmod()









