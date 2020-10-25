#!/usr/bin/env python3
# Copyright (c) 2017 Wei-Kai Lee. All rights reserved

# coding=utf-8
# -*- coding: utf8 -*-

import sys
import os
import collections
import numpy as np
import time
import matplotlib
import matplotlib.pyplot as plt


__xLable, __yLable, __zLable,__title ='', '', '', '' 
__legend=[]
__fontsize = 15
__xfontsize, __yfontsize, __zfontsize, __titlefontsize, __legfontsize = __fontsize, __fontsize, __fontsize, __fontsize, __fontsize
__xtickfontsize, __ytickfontsize, __ztickfontsize = __fontsize, __fontsize, __fontsize
__xtickdirection, __ytickdirection, __ztickdirection = 'horizontal', 'horizontal', 'horizontal'
__legloc, __legshadow = 0, True
__lnstyle = []
__clim = []
__sleeptime = 0.5
__xaxis = None
__yaxis = None

SETTING = collections.namedtuple('SETTING', 'xLable yLable zlabel title legend xfontsize yfontsize zfontsize titlefontsize legfontsize legloc legshadow lnstyle clim sleeptime xaxis yaxis xtickfontsize ytickfontsize xtickdirection ytickdirection')
def setting_generator(xLable=__xLable,yLable=__yLable,zlabel=__zLable,title=__title,
                      xfontsize=__xfontsize, yfontsize=__yfontsize, zfontsize=__zfontsize,titlefontsize=__titlefontsize, 
                      legend=__legend,legfontsize=__legfontsize,legloc=__legloc, legshadow=__legshadow, 
                      lnstyle=__lnstyle, clim=__clim, sleeptime=__sleeptime, 
                      xaxis=__xaxis, xtickfontsize=__xtickfontsize, xtickdirection=__xtickdirection,
                      yaxis=__yaxis, ytickfontsize=__ytickfontsize, ytickdirection=__ytickdirection):
    return SETTING(xLable,yLable,zlabel,title,legend,xfontsize, yfontsize, zfontsize, titlefontsize, legfontsize, legloc, legshadow, lnstyle, clim, sleeptime, xaxis, yaxis, xtickfontsize, ytickfontsize, xtickdirection, ytickdirection)
__defaultsetting = setting_generator()
def figure_save(fig,sfpath=None,sfname=None):
    if sfpath!=None and sfname!=None:
        if not os.path.isdir(sfpath):
            os.makedirs(sfpath)
        fig.savefig(  os.path.join(sfpath,sfname) )
def figure_end_control(fig, figshowBool, closeBool, sleeptime=__sleeptime):
    # show picture
    if figshowBool:
        plt.show(block=False)
        time.sleep(sleeptime)
    # Close
    if closeBool:
        plt.close(fig)
def x_yList_plot(x, yList, fpath=None, fname=None, axis=None, figshowBool=True, closeBool=True, setting=__defaultsetting):
    """
    >>> x = [  (ii-50)/25 for ii in range(100)]
    >>> yList = [ x, [xx**2 for xx in x] ]
    >>> s=setting_generator(xLable='x',yLable='y',title='Test',legend=['y=x','$y=x^2$'])
    >>> x_yList_plot(x, yList, fpath='./Example',fname='x_yList_plot',setting=s)

    """
    s = setting
    # axis setting
    if axis == None:
        fig,axis  = plt.subplots()
    else:
        fig = axis.figure
    # line plot
    LineList = []
    for ii,y in enumerate(yList):
        if len(s.legend)!=0:
            ln = axis.plot(x, y, label=s.legend[ii])
        else:
            ln = axis.plot(x, y)
        LineList += ln
    # Set Scale
    if s.xaxis!=None and len(s.xaxis)==2:
        axis.set_xlim(s.xaxis[0],s.xaxis[1])
    if s.yaxis!=None and len(s.yaxis)==2:
        axis.set_ylim(s.yaxis[0],s.yaxis[1])
    # Set Controls
    axis.set_xlabel(s.xLable, fontsize=s.xfontsize)
    axis.set_ylabel(s.yLable, fontsize=s.yfontsize)
    axis.set_title (s.title,  fontsize=s.titlefontsize)
    for tick in axis.xaxis.get_major_ticks():            
        tick.label.set_fontsize(s.xtickfontsize) 
        tick.label.set_rotation(s.xtickdirection)
    for tick in axis.yaxis.get_major_ticks():            
        tick.label.set_fontsize(s.ytickfontsize) 
        tick.label.set_rotation(s.ytickdirection)
    # legend Setting
    if len(s.legend) != 0:
        axis.legend(LineList, [l.get_label() for l in LineList], loc=s.legloc, shadow=s.legshadow, fontsize=s.legfontsize)
    # Output and Show
    fig.tight_layout()
    figure_save(fig,sfpath=fpath,sfname=fname)
    figure_end_control(fig, figshowBool, closeBool, sleeptime=s.sleeptime)
    return axis, LineList
def xList_yList_plot(xList, yList, fpath=None, fname=None, axis=None, figshowBool=True, closeBool=True, setting=__defaultsetting):
    s = setting
    # axis setting
    if axis == None:
        fig,axis  = plt.subplots()
    else:
        fig = axis.figure
    # line plot
    LineList = []
    for ii,y in enumerate(yList):
        if len(s.legend)!=0:
            ln = axis.plot(xList[ii], y, label=s.legend[ii])
        else:
            ln = axis.plot(xList[ii], y)
        LineList += ln
    # Set Scale
    if s.xaxis!=None and len(s.xaxis)==2:
        axis.set_xlim(s.xaxis[0],s.xaxis[1])
    if s.yaxis!=None and len(s.yaxis)==2:
        axis.set_ylim(s.yaxis[0],s.yaxis[1])
    # Set Controls
    axis.set_xlabel(s.xLable, fontsize=s.xfontsize)
    axis.set_ylabel(s.yLable, fontsize=s.yfontsize)
    axis.set_title (s.title,  fontsize=s.titlefontsize)
    for tick in axis.xaxis.get_major_ticks():            
        tick.label.set_fontsize(s.xtickfontsize) 
        tick.label.set_rotation(s.xtickdirection)
    for tick in axis.yaxis.get_major_ticks():            
        tick.label.set_fontsize(s.ytickfontsize) 
        tick.label.set_rotation(s.ytickdirection)
    # legend Setting
    if len(s.legend) != 0:
        axis.legend(LineList, [l.get_label() for l in LineList], loc=s.legloc, shadow=s.legshadow, fontsize=s.legfontsize)
    # Output and Show
    fig.tight_layout()
    figure_save(fig,sfpath=fpath,sfname=fname)
    figure_end_control(fig, figshowBool, closeBool, sleeptime=s.sleeptime)
    return axis, LineList
def xy_contour_plot(x, y, z, fpath=None, fname=None, axis=None, figshowBool=True, closeBool=True, setting=__defaultsetting):
    """
    >>> x, y = np.meshgrid( np.linspace(-1,1,20), np.linspace(-1,1,20))
    >>> cZ = np.exp(x+y)
    >>> AXList = xy_contour_plot(x,y,cZ,fpath='./Example', fname='xy_contour_plot')
    """
    s = setting
    # axis setting
    if axis == None:
        fig,axis  = plt.subplots()
    else:
        fig = axis.figure
    # plot
    cmap = plt.get_cmap('jet')
    if len(s.clim)!=0 and s.clim[0]!=None and s.clim[1]!=None:
        im1 = axis.contourf(x, y, z, 20, cmap=cmap, vmin=s.clim[0], vmax=s.clim[1])    
    else:
        im1 = axis.contourf(x, y, z, 20, cmap=cmap)   
    # Set Controls
    axis.set_xlabel(s.xLable, fontsize=s.xfontsize)
    axis.set_ylabel(s.yLable, fontsize=s.yfontsize)
    axis.set_title (s.title,  fontsize=s.titlefontsize)
    cbar1 = fig.colorbar(im1, ax=axis)     
    # Output and Show
    fig.tight_layout()
    figure_save(fig,sfpath=fpath,sfname=fname)
    figure_end_control(fig, figshowBool, closeBool, sleeptime=s.sleeptime)
    return axis
def xy_contour_polar_plot(r, theta, z, fpath=None, fname=None, axis=None, figshowBool=True, closeBool=True, setting=__defaultsetting):
    """
    >>> theta, phi = np.meshgrid( np.linspace(0,90,91), [p*np.pi/180 for p in np.linspace(0,360,90)])
    >>> cZ = np.cos([ t*np.pi/180 for t in theta])
    >>> AXList = xy_contour_polar_plot(theta,phi,cZ,fpath='./Example', fname='xy_contour_polar_plot')
    """
    s = setting
    # axis setting
    if axis == None:
        fig,axis  = plt.subplots(subplot_kw=dict(projection='polar'))
    else:
        fig = axis.figure
    # plot
    cmap = plt.get_cmap('jet')
    if len(s.clim)!=0 and s.clim[0]!=None and s.clim[1]!=None:
        im1 = axis.contourf(theta,r,z, 20, cmap=cmap, vmin=s.clim[0], vmax=s.clim[1])    
    else:
        im1 = axis.contourf(theta,r,z, 20, cmap=cmap)  
    # Set Controls
    axis.set_xlabel(s.xLable, fontsize=s.xfontsize)
    axis.set_ylabel(s.yLable, fontsize=s.yfontsize)
    axis.set_title (s.title,  fontsize=s.titlefontsize)
    cbar1 = fig.colorbar(im1, ax=axis)     
    # Output and Show
    fig.tight_layout()
    figure_save(fig,sfpath=fpath,sfname=fname)
    figure_end_control(fig, figshowBool, closeBool, sleeptime=s.sleeptime)
    return axis
if __name__ == '__main__':
    import doctest
    doctest.testmod()
