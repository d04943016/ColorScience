#!/usr/bin/env python3
# Copyright (c) 2017 Wei-Kai Lee. All rights reserved

# coding=utf-8
# -*- coding: utf8 -*-



### python module
import sys
import os
import collections
import numpy as np

### my module
MaterialPath = os.path.dirname(os.path.abspath(__file__))
srcPath = os.path.dirname(MaterialPath)

from .SpectrumClass import SpectrumClass
if srcPath not in sys.path:
    sys.path.append(srcPath)
from ReaderWriter import Reader

def SpectrumReader(fpath,filename, printInformationBool=True, FilenameExtension = 'spc'):
    """

    >>> fpath = './Example'
    >>> fname = 'cbp_irppy2acac'
    >>> validFile, spec = SpectrumReader(fpath,fname)
    >>> print(spec.printInformation())
    >>> print(spec.AvergePhotonIntensity())
    2.28419073431
    >>> wv = np.array([520,530,540], dtype=np.float64)
    >>> print(spec.Intensity(wv))
    [ 0.98584  0.88297  0.72379]
    """
    TagGroupList = [['wavelength', 'Intensity']]
    if printInformationBool:
        print('Now reading spectrum file ({0}.{1})'.format(os.path.join(fpath,filename), FilenameExtension) )
    validFile, dataDict, TagDict, unitDict, groupNumber = Reader.readfile.ColFileRead(fpath, filename+'.'+FilenameExtension, TagGroupList)
    if not validFile:
        return validFile, None
    if unitDict == None or len(unitDict["wavelength"])==0:
        unitDict = collections.defaultdict(list)
        unitDict["wavelength"] = "nm"
    spec = SpectrumClass(np.array(dataDict["wavelength"],dtype=np.float64),np.array(dataDict["Intensity"],dtype=np.float64),wavelengthunitstr=unitDict["wavelength"])
    spec.NoteDict["PATH"] = fpath
    spec.NoteDict["FILENAME"] = filename
    return validFile, spec
def SpectrumreadInformation(lines):
    if len(lines)==2:
        fpath = ""
        fname = ""
        for line in lines:
            TagList, StrList=Reader.lineProcess.LineTagSpliter(line,preStr='[',postStr=']',colNum=1)
            if TagList[0].upper()=="PATH":
                fpath = StrList
            elif TagList[0].upper()=="FILENAME": 
                fname = StrList
        if fpath == "" or fname == "":
            return False, None
        return SpectrumReader(fpath,fname)        
    else: 
        return False, None
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # test_fun()











