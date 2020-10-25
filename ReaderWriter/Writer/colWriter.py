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
>>> fpath,fname = './Example/', 'ColTest.txt'
>>> xList=[ mySep2List(0,2*np.pi,0.01), mySep2List(0,2*np.pi,0.01) ]
>>> dataList= [ [np.sin(x1) for x1 in xList[0]], [np.cos(x2) for x2 in xList[1]] ]
>>> xStr=['X1','X2']
>>> dataStr=['Y1=sin(X1)','Y2=cos(X2)']
>>> my_XYcolWriter(fpath,fname,xList,dataList,xStr,dataStr)
"""

import os

def my_XYcolWriter(fpath,fname,xList,dataList,xStr=[],dataStr=[],xStrspacingStr='20s',dataStrspacingStr='20s',xspacingStr='20.5f',dataspacingStr='20.5f',openType='w',file=None,fcloseBool=True):
    if file == None:
        if not os.path.isdir(fpath):
            os.makedirs(fpath)
        file = open(os.path.join(fpath, fname),openType)
    if not(len(xStr)==0 or len(dataStr)==0):
        xlinestr = ''
        datalinestr = ''
        for x in xStr:
            temptstr = '{0:>'+xStrspacingStr+'} '
            xlinestr += temptstr.format(x)
        for data in dataStr:
            datalinestr += ('{0:>'+dataStrspacingStr+'} ').format(data)
        file.write('{0} {1} \n'.format(xlinestr,datalinestr))
    for ii in range(len(xList[0])):
        xlinestr = ''
        datalinestr = ''
        for jj in range(len(xList)):
            temptstr = '{0:>'+xspacingStr+'} '
            xlinestr += temptstr.format(xList[jj][ii])
        for jj in range(len(dataList)):
            datalinestr += ('{0:>'+dataspacingStr+'} ').format(dataList[jj][ii])
        file.write('{0} {1} \n'.format(xlinestr,datalinestr))
    if fcloseBool==True:
        file.close()
    else:
        return file
def my_colWriter(fpath,fname,tagstr,data,spacingList=[],file=None,openType='w',fcloseBool=True):
    # data[row][col]
    if file == None:
        if not os.path.isdir(fpath):
            os.makedirs(fpath)
        file = open(os.path.join(fpath, fname),openType)
    if len(spacingList)==0:
        spacingList = ['20']
    # tag
    if tagstr!=None:
        for ii,tag in enumerate(tagstr):
            spacing = spacingList[0] if len(spacingList)==1 else  spacingList[ii]
            strr = "{0:>" + str(spacing) + "} "
            file.write(strr.format(tag))
        file.write('\n')
    # write data
    for row in data:
        for ii,d in enumerate(row):
            spacing = spacingList[0] if len(spacingList)==1 else  spacingList[ii]
            strr = "{0:>" + str(spacing) + "} "
            file.write(strr.format(d))
        file.write('\n')
    if fcloseBool==True:
        file.close()
    else:
        return file
if __name__ == '__main__':
    import doctest
    doctest.testmod()







