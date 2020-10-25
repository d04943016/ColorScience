#!/usr/bin/env python3
# Copyright (c) 2017 Wei-Kai Lee. All rights reserved

# coding=utf-8
# -*- coding: utf8 -*-

# my_colWriter is a module to write a column type file with file path, fpath, and 
#   file name, fname. xList is a list of list corresponding to the input values.
#   dataList is the corresponding results. xStr and dataStr are the tag information
#   for x and data. 
# Format:
# xStr[0]       xStr[1]       xStr[2]        dataStr[0]        dataStr[1]
# xList[0][0]   xList[1][0]   xList[2][0]    dataList[0][0]    dataList[1][0]
# xList[0][1]   xList[1][1]   xList[2][1]    dataList[0][1]    dataList[1][1] 
# xList[0][2]   xList[1][2]   xList[2][2]    dataList[0][2]    dataList[1][2] 
# xList[0][3]   xList[1][3]   xList[2][3]    dataList[0][3]    dataList[1][3] 
# xList[0][4]   xList[1][4]   xList[2][4]    dataList[0][4]    dataList[1][4]
# 

"""
>>> import sys
>>> import numpy as np
>>> WriterPath = os.path.dirname(os.path.abspath(__file__))
>>> RWPath = os.path.dirname(WriterPath)
>>> srcPath = os.path.dirname(RWPath)
>>> sys.path.append(srcPath)
>>> from Help.myMath import mySep2List
>>> fpath,fname = './Example/', 'MatixTest.txt'
>>> xList=mySep2List(0,2*np.pi,0.5)
>>> yList=mySep2List(0,2,0.2)
>>> dataList=[ [np.cos(x)*y for y in yList] for x in xList ]
>>> my_MatrixWriter(fpath,fname,xList,yList,dataList,tagStr='Y\X')

"""

import os

def my_MatrixWriter(fpath,fname,xList,yList,dataList,tagStr=' ',tagspacingStr='20s',xyspacingStr='20.5f',dataspacingStr='20.5f',openType='w',file=None,fcloseBool=True):
    if file == None:
        if not os.path.isdir(fpath):
            os.makedirs(fpath)
        file = open(os.path.join(fpath, fname),openType)
    if len(xList)!=0:
        xlinestr = ('{0:>'+tagspacingStr+'} ').format(tagStr) if len(yList)!=0 else ('{0:>'+tagspacingStr+'}').join(' ')
        for x in xList:
            xlinestr += ('{0:>'+xyspacingStr+'} ').format(x)
        file.write('{0} \n'.format(xlinestr))
    for ii in range(len(dataList[0])):
        ylinestr = ('{0:>'+xyspacingStr+'} ').format(yList[ii]) if len(yList)!=0 else ''
        datalinestr = ''
        for jj in range(len(dataList)):
            datalinestr += ('{0:>'+dataspacingStr+'} ').format(dataList[jj][ii])
        file.write('{0}{1} \n'.format(ylinestr,datalinestr))
    if fcloseBool==True:
        file.close()
    else:
        return file

if __name__ == '__main__':
    import doctest
    doctest.testmod()


