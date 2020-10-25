#!/usr/bin/env python3
# Copyright (c) 2018 Wei-Kai Lee. All rights reserved

# coding=utf-8
# -*- coding: utf8 -*-


import numpy as np

def dx(x):
    return x[1:]-x[0:x.size-1]
def yave(y):
    xszie = y.shape[-1]
    return ( y[...,1::]+y[...,0:(xszie-1):] )/2
def myNumericalIntegration(x,y):
    """
    myNumericalIntegration is a function to calculate the area of 
    a y = function(x) by trapezoid method.
    x must be ascending.

    >>> x = np.linspace(0,1,100, dtype=np.float64) 
    >>> y = x**2
    >>> value = myNumericalIntegration(x,y)
    >>> print(value)
    0.33335033840084355
    >>> x = np.linspace(0,1,1000, dtype=np.float64) 
    >>> y = x**2
    >>> value = myNumericalIntegration(x,y)
    >>> print(value)
    0.3333335003338339
    >>> x = np.linspace(0,1,10000, dtype=np.float64)  
    >>> y = x**2
    >>> value = myNumericalIntegration(x,y)
    >>> print(value)
    0.3333333350003337
    """
    x = np.array(x)
    y = np.array(y)
    return np.einsum('...i,i->...',yave(y),dx(x))
def yave2(y):
    xszie = y.shape[0]
    return ( y[1::,...]+y[0:(xszie-1):,...] )/2
def myNumericalIntegration2(x,y):
    x = np.array(x)
    y = np.array(y)
    return np.einsum('i...,i->...',yave2(y),dx(x))
def myTRAPEZOIDAL(fun,x0,x1,xPts=200):
    """
    myTRAPEZOIDAL is a function to calclate the integration of function f from 
    x0 to x1 with equal spacing. (xPts: points of x)

    >>> import numpy as np
    >>> f = lambda x: [np.sin(x), np.cos(x)]
    >>> Int, xList, yListList = myTRAPEZOIDAL(f,0,np.pi)
    >>> print(Int)
    [1.99995846e+00 9.02056208e-17]
    >>> Int, xList, yListList = myTRAPEZOIDAL(f,0,np.pi,xPts=300)
    >>> print(Int)
    [1.99998160e+00 2.68882139e-16]
    >>> Int, xList, yListList = myTRAPEZOIDAL(f,0,np.pi,xPts=400)
    >>> print(Int)
    [1.99998967e+00 1.02348685e-16]
    >>> Int, xList, yListList = myTRAPEZOIDAL(f,0,np.pi,xPts=1000)
    >>> print(Int)
    [ 1.99999835e+00 -8.96418356e-16]
    """
    xList = np.linspace(x0, x1, num=int(xPts) )
    data = np.array(fun(xList))
    Int = myNumericalIntegration(xList,data)
    return Int, xList, data
def myFunIntegration(f, x0, x1, tol=1e-5, recursiveLim=1e4, xCountStart=100, intfun=myTRAPEZOIDAL):
    """
    >>> import numpy as np
    >>> f = lambda x: [np.sin(x), np.cos(x)]
    >>> Sn, err, nodes, count =  myFunIntegration(f, 0, np.pi, tol=1e-5)
    >>> print(Sn)
    [1.99999934e+00 2.22044605e-16]
    >>> print(err)
    2.781470994472901e-06
    >>> print(nodes.size)
    17
    >>> print(count)
    8
    >>> f = lambda x: [ x**2, x**3]
    >>> Sn, err, nodes, count =  myFunIntegration(f, -2, 2, tol=1e-5)
    >>> print(Sn)
    [5.333334 0.      ]
    >>> print(err)
    4.433938502017287e-06
    >>> print(count)
    24
    >>> print(nodes.size)
    49
    >>> f = lambda x: [ np.exp(x), np.exp(x**2)]
    >>> Sn, err, nodes, count =  myFunIntegration(f, -2, 2, tol=1e-5)
    >>> print(Sn)
    [ 7.25372109 32.90525734]
    >>> print(err)
    5.414152568605779e-06
    >>> print(count)
    68
    >>> print(nodes.size)
    137
    """
    S, xList, yListList = intfun(f, x0, x1, xPts=xCountStart)
    Sn, err, nodes, count = recursive_integration1(f, x0, x1, S, tol=tol, recursiveLim=recursiveLim, xCountStart=xCountStart, intfun=intfun)
    return Sn, err, nodes, count
    
    # S, xList, yListList = intfun(f, x0, x1, xPts=xCountStart)
    # Sn, err, xList, count = recursive_integration2(f, x0, x1, S, xList, tol=tol, recursiveLim=recursiveLim)
    # return Sn, err, count

    # S, xList, yListList = intfun(f, x0, x1, xPts=xCountStart)
    # Sn, err, xListNew, yListListNew, count, dxmin = recursive_integration3(f, S, xList, yListList, tol=tol, recursiveLim=recursiveLim, xCountStart=xCountStart, dxMin=dxMin)
    # return Sn, err, xListNew, count
def recursive_integration1(f, x0, x1, S, tol=1e-3, recursiveLim=1e4, xCountStart=100, intfun=myTRAPEZOIDAL):
    """ 
    f: function of f(x)
    [a,b] : the interval of integration
    S : the previous integration result
    tol : the tolerance
    
    This is a subfunction of adapt_simpson.
    """
    xc = float(x0+x1)/2
    SL, xListL, dataL = intfun(f,x0,xc,xPts=xCountStart)
    SR, xListR, dataR = intfun(f,xc,x1,xPts=xCountStart)
    Sn = SL+SR
    err = max( np.abs(Sn-S) )
    if err <= tol or recursiveLim==1:
        nodes = np.array([x0,xc,x1])
        count = 1
        return Sn, err, nodes, count
    fac = 0.5
    SL, err1, nodes1, countL = recursive_integration1(f, x0, xc, SL, tol=tol*fac, recursiveLim=recursiveLim-1, xCountStart=xCountStart, intfun=intfun)
    SR, err2, nodes2, countR = recursive_integration1(f, xc, x1, SR, tol=tol*(1-fac), recursiveLim=recursiveLim-1, xCountStart=xCountStart, intfun=intfun)
    err = err1 + err2
    nodes = np.append(nodes1, nodes2[1::])
    count = countL+1 if countL>=countR else countR+1 # countL+countR # countL+1 if countL>=countR else countR+1
    Sn = SL+SR
    return Sn, err, nodes, count
def myMidpointList_Integration2(f, xList, S):
    # Mid point
    xList = np.array(xList)
    xList2 = (xList[0:xList.size-1]+xList[1:xList.size])/2
    data = f(xList2)
    # Sum
    temptsum = np.einsum('...i,i->...', data, dx(xList) ) 
    Sn = (S+temptsum)/2
    # Merge List
    xListNew = np.zeros( xList.size+xList2.size, dtype=xList.dtype )
    xListNew[0::2] = xList
    xListNew[1::2] = xList2
    return Sn, xListNew
def recursive_integration2(f, x0, x1, S, xList, tol=1e-5, recursiveLim=1e4):
    """ 
    f: function of f(x)
    [a,b] : the interval of integration
    S : the previous integration result
    tol : the tolerance
    
    This is a subfunction of adapt_simpson.
    """
    Sn, xListNew = myMidpointList_Integration2(f, xList, S)
    err = max( np.abs(Sn-S) )
    if err <= tol or recursiveLim==1:
        count = 1
        return Sn, err, xListNew, count
    Sn, err, xListNew, count = recursive_integration2(f, x0, x1, Sn, xList=xListNew, tol=tol, recursiveLim=recursiveLim-1)
    count = count + 1
    return Sn, err, xListNew, count
def myMidpointList_Integration3(f, xList, yListList):
    # Mid point
    xList = np.array(xList)
    xList2 = (xList[0:xList.size-1]+xList[1:xList.size])/2
    data = f(xList2)
    # Sum
    temptsum = np.einsum('...i,i->...', data, dx(xList) ) 
    # Merge x List
    xListNew = np.zeros( xList.size+xList2.size, dtype=xList.dtype )
    xListNew[0::2] = xList
    xListNew[1::2] = xList2
    # Merge y List
    yListListNew = np.zeros( (yListList.shape[0], xListNew.size) , dtype=yListList.dtype)
    yListListNew[:,0::2] = yListList
    yListListNew[:,1::2] = data
    # Sum
    Sn = myNumericalIntegration(xListNew,yListListNew)
    return Sn, xListNew, yListListNew
def recursive_integration3(f, S, xList, yListList, tol=1e-5, recursiveLim=1e4, xCountStart=100, dxMin=None):
    """ 
    f: function of f(x)
    [a,b] : the interval of integration
    S : the previous integration result
    tol : the tolerance
    
    This is a subfunction of adapt_simpson.
    """
    indMid = int(len(xList)/2)
    SL, xListL, yListListL = myMidpointList_Integration3(f, xList[:indMid+1:], yListList[:,:indMid+1:] )
    SR, xListR, yListListR = myMidpointList_Integration3(f, xList[indMid::],   yListList[:,indMid::] )
    Sn = SL+SR
    err = max( np.abs(Sn-S) )
    # End Case
    xListNew = np.append( xListL, xListR[1::] )
    dxmin = min(dx(xListNew))
    if err <= tol or recursiveLim==1 or dxMin==None or dxmin<dxMin:
        count = 1
        yListListNew = np.append( yListListL, yListListR[:,1::] ) 
        return Sn, err, xListNew, yListListNew, count, dxmin
    # Iterative Case
    sL, sR = np.sum(SL), np.sum(SR)
    fac = sL/(sL+sR) if (sL+sR)!=0 else 0.5
    SL, errL, xListL, yListListL, countL, dxL = recursive_integration3(f, SL, xList=xListL, yListList=yListListL, tol=tol*fac, recursiveLim=recursiveLim-1, dxMin=dxMin)
    SR, errR, xListR, yListListR, countR, dxR = recursive_integration3(f, SR, xList=xListR, yListList=yListListR, tol=tol*(1-fac), recursiveLim=recursiveLim-1, dxMin=dxMin)
    Sn = SL+SR
    err = errL + errR
    count = countL+1 if countL>countR else countR+1 #countL+countR # countL+1 if countL>countR else countR+1
    xListNew = np.append( xListL, xListR[1::] )
    dxmin = dxL if dxL<dxR else dxR
    yListListNew = np.append( yListListL, yListListR[:,1::] ) 
    return Sn, err, xListNew, yListListNew, count, dxmin

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    """
    x = []
    y = []
    value = myNumericalIntegration(x,y)
    """









