#!/usr/bin/env python3
# Copyright (c) 2018 Wei-Kai Lee. All rights reserved

# coding=utf-8
# -*- coding: utf8 -*-

"""
my_tagline is a module to process tag line. (read/write)
1. readTagColNum(tagTokens, tagstrList): 
    is a function to judge whether the tag in tagTokens is in tagstrList
    and retrun three dict.(validDict, invalidDict, unitDict)
2. GroupCheckBool(TagDict, TagGroupList):
    is a function to check whether the Tag in TagGroupList is in TagDict
    and retutn a ListCheckBool with the same size of TagGroupList
3. GroupSelect(GroupCheckBool):
    is a function to select the group number

>>>
>>>
>>> # check readTagColNum(tagTokens, tagstrList)
>>> tagTokens = ["wavelength(nm)", "PL", "n", "k", "I(A)", "V(v)"]
>>> tagstrList = ["wavelength","n","k","na"]
>>> validTagDict, invalidTagDict, unitDict = readTagColNum(tagTokens, tagstrList)
>>> print(validTagDict)
defaultdict(<class 'list'>, {'wavelength': 0, 'n': 2, 'k': 3, 'na': -1})
>>> print(invalidTagDict)
defaultdict(<class 'list'>, {'PL': 1, 'I': 4, 'V': 5})
>>> print(unitDict)
defaultdict(<class 'list'>, {'wavelength': 'nm', 'PL': '', 'n': '', 'k': '', 'I': 'A', 'V': 'v'})
>>> 
>>> 
>>> # check GroupCheckBool(TagDict, TagGroupList)
>>> tagTokens = ["wavelength(nm)", "PL", "n", "k", "I(A)", "V(v)"]
>>> TagGroupList = [ ["wavelength","n","k"], ["wavelength","no","ko","ne","ke"], ["wavelength","nx","kx","ny","ky","nz","kz"]]
>>> tagstrList = []
>>> tagstrList = list( set(TagGroupList[0]+TagGroupList[1]+TagGroupList[2]))
>>> validTagDict, invalidTagDict, unitDict = readTagColNum(tagTokens, tagstrList)
>>> ListCheckBool = GroupCheckBool(validTagDict, TagGroupList)
>>> print(ListCheckBool)  
[[True, True, True], [True, False, False, False, False], [True, False, False, False, False, False, False]]
>>>
>>> 
>>> # check GroupSelect(GroupCheckBool)
>>> groupNumber = GroupSelect(ListCheckBool)
>>> print(groupNumber)
0
>>> 
>>> 
>>> tagTokens = ["wavelength(nm)", "PL", "n", "k", "I(A)", "V(v)"]
>>> TagGroupList = [ ["wavelength","n","k"], ["wavelength","n","k","I","V"], ["wavelength","nx","kx","ny","ky","nz","kz"]]
>>> tagstrList = []
>>> tagstrList = list( set(TagGroupList[0]+TagGroupList[1]+TagGroupList[2]))
>>> validTagDict, invalidTagDict, unitDict = readTagColNum(tagTokens, tagstrList)
>>> ListCheckBool = GroupCheckBool(validTagDict, TagGroupList)
>>> print(ListCheckBool)  
[[True, True, True], [True, True, True, True, True], [True, False, False, False, False, False, False]]
>>> groupNumber = GroupSelect(ListCheckBool)
>>> print(groupNumber)
1
>>>
>>>

"""

import collections

def readTagColNum(tagTokens, tagstrList, unitBool = True):
    """
    readTagColNum is a function to process the tag tokens. tagTokens is a list of tag string
    and tagstrList is a list containing the expected tag string that would in the
    tag line. This function would return three dict if unitBool is True. If unitBool
    is Fasle, this function would not speparate the unit part (the string between( and
    ) ) 
    validDict:  key:    the expected tag string 
                value:  the column number if key is in tagLine else the value is -1
    invalidDict:key:    the unexcpected tag string
                value:  the column number
    unitDict:   key:    the tag in tagLine
                value:  the unit of the tag if no unit default ""
                when unitBool is True


    """ 

    # default settings
    validTagDict = collections.defaultdict(list)
    invalidTagDict = collections.defaultdict(list)
    unitDict = collections.defaultdict(list)
    for tagstr in tagstrList:
        validTagDict[tagstr] = -1
    # start processing
    for i,tagstr in enumerate(tagTokens):
        # find unit and tagstr2
        if unitBool:
            first = tagstr.find("(")
            last = tagstr.rfind(")")
            unitstr = ""
            if first != -1 and last != -1:
                unitstr = tagstr[first+1:last]
            tagstr2 = tagstr[0:first] if first != -1 else  tagstr
            unitDict[tagstr2] = unitstr
        else:
            unitstr = ""
            tagstr2 = tagstr
        # add dictionary
        if tagstr2 in tagstrList:
            validTagDict[tagstr2] = i
        else:
            invalidTagDict[tagstr2] = i
    return validTagDict, invalidTagDict, unitDict
def GroupCheckBool(TagDict, TagGroupList):
    """
    GroupCheckBool is a function to check whether the tag in TagDict.keys()
    is in the TagGroupList. The key in TagDict is the tags and the value is 
    the corresponding colNum. TagGroupList is a List of List to specify the 
    group of the tag string.

    """

    # Container Setting (List Comprehension)
    ListCheckBool = [ [False] * len(x) for x in TagGroupList ] 
    # Chech Process
    for ii,TagGroupstr in enumerate(TagGroupList):
        for jj,Tagstr in enumerate(TagGroupList[ii]):
            if Tagstr in TagDict:
                ListCheckBool[ii][jj] = True if TagDict[Tagstr] != -1 else ListCheckBool[ii][jj]
    return ListCheckBool
def GroupSelect(GroupCheckBool):
    """
    GroupSelect is a function to select the all True group in GroupCheckBool.
    If there are more than one group is all True, choose the group with more
    Trues. Or choose the first all True group if the number of True are the
    same. If there is no group is all True, return -1

    """

    groupNumber = -1
    for i,checkBool in enumerate(GroupCheckBool):
        if len(checkBool) == sum(checkBool): # check all correct
            if groupNumber == -1:
                groupNumber = i 
            elif len(checkBool) > len(GroupCheckBool[groupNumber]):
                groupNumber = i
    return groupNumber
if __name__ == '__main__':
    import doctest
    doctest.testmod()










