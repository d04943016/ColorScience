#!/usr/bin/env python3
# Copyright (c) 2017 Wei-Kai Lee. All rights reserved

# coding=utf-8
# -*- coding: utf8 -*-


### python module
import os
import sys
import collections
import numpy as np
import pandas as pd

### my module
HelpPath = os.path.dirname(os.path.abspath(__file__))
srcPath = os.path.dirname(HelpPath)
if srcPath not in sys.path:
    sys.path.append(srcPath)
from . import myPlotHelp as mPH
from ReaderWriter.Writer.colWriter import my_XYcolWriter 

class myXYClass:
    """
    myXYClass is a base class like a container, which support the getValue function. 
    This class contains two variables and one function. 
    x is the first variable playing the role of keys and y is the corresponding value
    so the length of x and y are the same.

    >>> # case 1
    >>> x = np.array([0,1,2,3,4,5,6,7,8,9,10], dtype='float64')
    >>> y = np.array([[xx**2] for xx in x], dtype='float64')
    >>> XY = myXYClass(x,y)
    >>>
    >>> print(XY.x)
    [  0.   1.   2.   3.   4.   5.   6.   7.   8.   9.  10.]
    >>> print(XY.y)
    [[   0.]
     [   1.]
     [   4.]
     [   9.]
     [  16.]
     [  25.]
     [  36.]
     [  49.]
     [  64.]
     [  81.]
     [ 100.]]
    >>>
    >>> x0 = np.array([0,0.5,1,1.2,2,100], dtype='float64')
    >>> value = XY.getValue(x0)
    >>> print(value)
    [[ 0. ]
     [ 0.5]
     [ 1. ]
     [ 1.6]
     [ 4. ]
     [ nan]]
    >>>
    >>> # case 2
    >>> y = np.array([[xx,xx**2] for xx in x], dtype='float64')
    >>> XY = myXYClass(x,y,tags=['x','x^2'])
    >>> print(XY.dataframe)
             x    x^2
    0.0    0.0    0.0
    1.0    1.0    1.0
    2.0    2.0    4.0
    3.0    3.0    9.0
    4.0    4.0   16.0
    5.0    5.0   25.0
    6.0    6.0   36.0
    7.0    7.0   49.0
    8.0    8.0   64.0
    9.0    9.0   81.0
    10.0  10.0  100.0
    >>> print(XY.x)
    [  0.   1.   2.   3.   4.   5.   6.   7.   8.   9.  10.]
    >>> print(XY.y)
    [[   0.    0.]
     [   1.    1.]
     [   2.    4.]
     [   3.    9.]
     [   4.   16.]
     [   5.   25.]
     [   6.   36.]
     [   7.   49.]
     [   8.   64.]
     [   9.   81.]
     [  10.  100.]]
    >>> value = XY.getValue(x0)
    >>> print(value)
    [[ 0.   0. ]
     [ 0.5  0.5]
     [ 1.   1. ]
     [ 1.2  1.6]
     [ 2.   4. ]
     [ nan  nan]]
    >>> # case 3
    >>> XY = myXYClass(x,np.array([3.0]))
    >>> print(XY.dataframe)
            0
    0.0   3.0
    1.0   3.0
    2.0   3.0
    3.0   3.0
    4.0   3.0
    5.0   3.0
    6.0   3.0
    7.0   3.0
    8.0   3.0
    9.0   3.0
    10.0  3.0
    """
    def __init__(self, x, y, xStr=None, tags=None, xdtype=np.float64, ydtype=np.complex128):
        x = np.array(x, dtype=xdtype)
        y = np.array(y, dtype=ydtype)
        if y.shape[0] != x.size:
            y2 = np.zeros((x.size, y.size), dtype=ydtype)
            for ii,yy in enumerate(y):
                y2[:,ii] = yy
            y = y2
        if tags == None:
            self._dataframe = pd.DataFrame( y, index = x)
        else:
            self._dataframe = pd.DataFrame( y, columns = tags, index = x)
        self._dataframe.sort_index()
        self._xStr = xStr
        self._tags = tags
        self.NoteDict = collections.defaultdict(list)
    def getValue(self, x0, OutofRangeAssertBool = True, OutofRangeValue = np.nan):
        x0 = np.array(x0, dtype=self._dataframe.index.values.dtype)
        ndim = x0.ndim
        if ndim==0:
            x0 = np.array([x0], dtype=self._dataframe.index.values.dtype)
        index = np.searchsorted(self._dataframe.index, x0, side='right')
        # Boundary Process
        x = self._dataframe.index.values
        y = self._dataframe.values
        mask = (x0<x[0]) | ( (index>=x.size) & (x0!=x[x.size-1]) )
        index[index>=x.size] = x.size-1
        ratio = np.transpose((x0-x[index-1])/(x[index]-x[index-1])[np.newaxis])
        values = y[index-1, :] + (y[index,:]-y[index-1,:])*ratio
        if np.any(mask):
            assert OutofRangeAssertBool
        values[mask,:] = OutofRangeValue
        if ndim==0:
            return values[0]
        return values
    def saveData(self, fpath, fname, fnameExtenstion='.txt', xStrspacingStr='20s', dataStrspacingStr='20s',xspacingStr='20.5f',dataspacingStr='20.5f',openType='w',file=None,fcloseBool=True):
        if self._xStr == None or self._tags == None:
            xStr, dataStr = [], []
        else:
            xStr, dataStr = self._xStr, self._tags
        my_XYcolWriter(fpath,fname+fnameExtenstion,[self.x], np.transpose(self.y), xStr=[xStr], dataStr=dataStr,
                       xStrspacingStr=xStrspacingStr,dataStrspacingStr=dataStrspacingStr,xspacingStr=xspacingStr,
                       dataspacingStr=dataspacingStr,openType=openType,file=file,fcloseBool=fcloseBool)
    def plotData(self, fpath=None, fname=None, axis=None, figshowBool=True, closeBool=True, SeparateBool=False):
        xLabel = '' if self._xStr == None else self._xStr
        if not SeparateBool:
            legend = '' if self._tags == None else self._tags
            s = mPH.setting_generator(xLable=xLabel,legend=legend)
            mPH.x_yList_plot(self.x, np.transpose(self.y), fpath=fpath, fname=fname, axis=axis, figshowBool=figshowBool, closeBool=closeBool, setting=s)
        else:
            y = np.transpose(self.y)
            for ii in np.arange( len(y) ):
                fname2 = None if fname==None else fname+'_'+self._tags[ii]
                yLable = '' if self._tags == None else self._tags[ii]
                s = mPH.setting_generator(xLable=xLabel,yLable=yLable)
                mPH.x_yList_plot(self.x, [y[ii]], fpath=fpath, fname=fname2, axis=axis, figshowBool=figshowBool, closeBool=closeBool, setting=s)
   # data member
    @property
    def x(self):
        return self._dataframe.index.values
    @property
    def y(self):
        return self._dataframe.values
    @property
    def dataframe(self):
        return self._dataframe
    @property
    def tags(self):
        return self._tags

class myXYClass_FixedArea(myXYClass):
    """
    >>> # case 1
    >>> x = np.linspace(0,np.pi,500)
    >>> y = np.array( [np.sin(x), np.cos(x) ]).transpose()
    >>> XY = myXYClass_FixedArea(x,y,tags=['sin(x)','cos(x)'])
    >>> print(XY.Area)
    [  1.99999339e+00   1.11022302e-16]
    """
    def __init__(self, x, y, xStr=None, tags=None, xdtype=np.complex128, ydtype=np.complex128):
        super().__init__(x, y, xStr=xStr, tags=tags, xdtype=xdtype, ydtype=ydtype)
        self.__Area = self.calArea(self._dataframe)
    def _xScaling(self,factor):
        self._dataframe.index = self._dataframe.index.values*factor
        self._dataframe = self._dataframe/factor
        return self
    def calArea(self,dataframe):
        x = dataframe.index.values
        y = dataframe.values
        dx = np.transpose( (x[1:]-x[0:(x.size-1)])[np.newaxis] )
        ymean = (y[1:,:]+y[0:(x.size-1),:])
        return np.sum( ymean*dx, axis=0 )/2
    @property
    def Area(self):
        return self.__Area 
if __name__ == '__main__':
    import doctest
    doctest.testmod()




