#!/usr/bin/env python3
# Copyright (c) 2018 Wei-Kai Lee. All rights reserved

# coding=utf-8
# -*- coding: utf8 -*-
### python module
import sys
import os

ReaderPath = os.path.dirname(os.path.abspath(__file__))
RWPath = os.path.dirname(ReaderPath)
srcPath = os.path.dirname(RWPath)

from .readfile import ColFileRead

if srcPath not in sys.path:
    sys.path.append(srcPath)
from Help.myXYClass import myXYClass
from Help.myXYClass import myXYClass_FixedArea


def myXYfileReader(fpath, filename, TagGroup, unitBool = True, mysep = " \t", maxsplit = -1, IsFixedArea=False):
    TagGroupList = [TagGroup]
    validFile, dataDict, TagDict, unitDict, groupNumber = ColFileRead(fpath, filename, TagGroupList, unitBool = unitBool, mysep = mysep, maxsplit = maxsplit)
    if not validFile:
        return validFile,None
    if IsFixedArea:
        xy = myXYClass_FixedArea(dataDict[TagGroup[0]],[ [dataDict[tag][ii] for tag in TagGroup[1::]] for ii in range(len(dataDict[TagGroup[0]]))])
    else:
        xy = myXYClass(dataDict[TagGroup[0]],[ [dataDict[tag][ii] for tag in TagGroup[1::]] for ii in range(len(dataDict[TagGroup[0]]))])
    return True, xy    
