#!/usr/bin/env python3
# Copyright (c) 2017 Wei-Kai Lee. All rights reserved

# coding=utf-8
# -*- coding: utf8 -*-

"""
SpectrumClass is a class to store the spectrum information, i.e. the ralation between
 wavelength and intensity.
 
 The constructor of this calss includes two necessities and one option
     
     wavelength, intensity  (necessary)
     wavelengthunitstr="nm" (optional)
     
     Once the object is constructed, wavelength and intensity do not support the modification
     but support the change in unit. (e.x. from "nm" to "m")
 This class store the information of the absolute value of intensity but provide some function
    to calculate the normalized intensity by area or by max. 
    (If the searching wavelength is not in the wavelength provided when the object is constructed,
    then all the value is calculated by interpolation. However, if the searching wavelength 
    is out of the range of, the user can definced whether to recall assertation or put the 
    other value. Default no assertation, and the value is zero if out of range.)
    
    Intensity(wavelength, OutofRangeAssertBool = True, OutofRangeValue = 0)
    Intensity_NormalizedByMax(wavelength, OutofRangeAssertBool = True, OutofRangeValue = 0)
    Intensity_NormalizedByArea(wavelength, OutofRangeAssertBool = True, OutofRangeValue = 0)

 This class can also calculate the average photon energy (eV) of the spectrum.
    AvergePhotonIntensity()


>>> wavelength = np.linspace(520, 600, 9)
>>> intensity =  np.array([1,2,3,4,5,4,3,2,1], dtype=np.float64)
>>> spec = SpectrumClass(wavelength,intensity)
>>> print(spec.Area)
[ 240.]
>>> print(spec.wavelength_store())
[ 520.  530.  540.  550.  560.  570.  580.  590.  600.]
>>> print(spec.intensity_store())
[ 1.  2.  3.  4.  5.  4.  3.  2.  1.]
>>> print(spec.wavelengthunitstr)
nm
>>> 
>>> wv = np.array([520,525,530,535,540,545,550], dtype=np.float64)
>>> value = spec.Intensity(wv)
>>> print(value)
520.0    1.0
525.0    1.5
530.0    2.0
535.0    2.5
540.0    3.0
545.0    3.5
550.0    4.0
dtype: float64
>>> value = spec.Intensity_NormalizedByMax(wv)
>>> print(value)
520.0    0.2
525.0    0.3
530.0    0.4
535.0    0.5
540.0    0.6
545.0    0.7
550.0    0.8
dtype: float64
>>> value = spec.Intensity_NormalizedByArea(wv)
>>> print(value)
520.0    0.004167
525.0    0.006250
530.0    0.008333
535.0    0.010417
540.0    0.012500
545.0    0.014583
550.0    0.016667
dtype: float64
>>>
>>> E = spec.AvergePhotonIntensity()
>>> print(E)
2.21676345446
>>> 
>>> spec.wavelengthunitstr = "um"
>>> print(spec.Area)
[ 240.]
>>> print(spec.wavelength_store())
[ 0.52  0.53  0.54  0.55  0.56  0.57  0.58  0.59  0.6 ]
>>> print(spec.intensity_store())
[ 1000.  2000.  3000.  4000.  5000.  4000.  3000.  2000.  1000.]
>>> print(spec.wavelengthunitstr)
um
>>> wv = wv/1000
>>> value = spec.Intensity(wv)
>>> print(value)
0.520    1000.0
0.525    1500.0
0.530    2000.0
0.535    2500.0
0.540    3000.0
0.545    3500.0
0.550    4000.0
dtype: float64
>>> value = spec.Intensity_NormalizedByMax(wv)
>>> print(value)
0.520    0.2
0.525    0.3
0.530    0.4
0.535    0.5
0.540    0.6
0.545    0.7
0.550    0.8
dtype: float64
>>> value = spec.Intensity_NormalizedByArea(wv)
>>> print(value)
0.520     4.166667
0.525     6.250000
0.530     8.333333
0.535    10.416667
0.540    12.500000
0.545    14.583333
0.550    16.666667
dtype: float64
>>> E = spec.AvergePhotonIntensity()
>>> print(E)
2.21676345446
"""

### python module
import sys
import os
import collections
import numpy as np
import pandas as pd
### my module
MaterialPath = os.path.dirname(os.path.abspath(__file__))
srcPath = os.path.dirname(MaterialPath)
if srcPath not in sys.path:
    sys.path.append(srcPath)
from Help.my_unit import unit2unit
from Help.myXYClass import myXYClass_FixedArea
from Help.myNumericalIntegration import myNumericalIntegration 
from ReaderWriter.Writer.colWriter import my_XYcolWriter 

# Constant variable
_IntensityDefaultValue = 0.0

class SpectrumClass(myXYClass_FixedArea):
    def __init__(self, wavelength, intensity, wavelengthunitstr="nm"):
        super().__init__(wavelength, intensity, xStr='wavelength', tags=['Intensity'], xdtype=np.float64, ydtype=np.float64)
        self.__wavelengthunitstr = wavelengthunitstr
    # intensity information
    def Intensity(self, wavelength, OutofRangeAssertBool = True, OutofRangeValue = _IntensityDefaultValue):
        tempt = np.transpose(self.getValue(wavelength, OutofRangeAssertBool, OutofRangeValue))[0]
        if tempt.ndim==0:
            tempt = np.array([tempt], dtype=np.float64)
            wavelength = np.array([wavelength], dtype=np.float64)
        return pd.Series(tempt, index=wavelength, dtype=np.float64)
    def Intensity_NormalizedByMax(self, wavelength, alpha=1.0, OutofRangeAssertBool = True, OutofRangeValue = _IntensityDefaultValue):
        intensity = self.Intensity(wavelength, OutofRangeAssertBool, OutofRangeValue)
        maxi = np.max(self.intensity_store())
        return intensity/maxi*alpha
    def Intensity_NormalizedByArea(self, wavelength, alpha=1.0, OutofRangeAssertBool = True, OutofRangeValue = _IntensityDefaultValue):
        intensity = self.Intensity(wavelength, OutofRangeAssertBool, OutofRangeValue)
        Area = self.Area[0]
        return intensity/Area*alpha if Area!=0 else intensity
    # Spectrum Information
    def AvergePhotonIntensity(self):
        factor = unit2unit('n',self.wavelengthunitstr[0:(len(self.wavelengthunitstr)-1)])
        wavelength = self.wavelength_store()
        intensity = self.Intensity_NormalizedByArea(wavelength).values
        return (1240*factor)*myNumericalIntegration(wavelength, intensity/wavelength)
    def wavelength_store(self):
        return self.x
    def intensity_store(self):
        y = self.y
        return np.transpose(y)[0]
    def printInformation(self):
        if len(self.NoteDict.keys())!=0:
            print("In Note : ")
            for key in self.NoteDict:
                print("   {0}:{1}".format(key,self.NoteDict[key]))
            print('-'*40)
        wavelength = self.wavelength_store()
        intensity = self.intensity_store()
        print('{0:>20s} {1:>20s}'.format( "Wavelength({0})".format(self.wavelengthunitstr), "Intensity"))
        for ii in range(len(wavelength)):
            print("{0:>20.5f} {1:>20.5f}".format(wavelength[ii],intensity[ii]))
        print('='*40)    
    def saveInformationstr(self):
        strr = ""
        if "PATH" in self.NoteDict and "FILENAME" in self.NoteDict:
            strr = strr + "[{0}]{1}".format("PATH",self.NoteDict["PATH"]) + "|" + "[{0}]{1}".format("FILENAME",self.NoteDict["FILENAME"])
        return strr
        """
        for key in self.NoteDict:
            strr = strr + "[{0}]{1}".format(key,self.NoteDict[key]) + "|"
        """
    # operator overloading
    def __add__(self, other):
        if isinstance(other, float):
            return SpectrumClass(self.wavelength_store(), self.intensity_store()+other, wavelengthunitstr=self.wavelengthunitstr)
        unit1, unit2 = self.wavelengthunitstr, other.wavelengthunitstr
        self.wavelengthunitstr, other.wavelengthunitstr = "nm", "nm"
        wv1, wv2 = self.wavelength_store(), other.wavelength_store()
        wv = wv1[ np.bitwise_and(wv1>=max([wv1[0], wv2[0]]), wv1<=min([wv1[-1], wv2[-1]])) ]
        Int1, Int2 = self.Intensity(wv).values, self.Intensity(wv).values
        spec3 = SpectrumClass(wv, Int1+Int2, wavelengthunitstr="nm")
        self.wavelengthunitstr = unit1
        other.wavelengthunitstr = unit2
        return spec3
    def __mul__(self, other):
        if isinstance(other, float):
            return SpectrumClass(self.wavelength_store(), self.intensity_store()*other, wavelengthunitstr=self.wavelengthunitstr)
        unit1, unit2 = self.wavelengthunitstr, other.wavelengthunitstr
        self.wavelengthunitstr, other.wavelengthunitstr = "nm", "nm"
        wv1, wv2 = self.wavelength_store(), other.wavelength_store()
        wv = wv1[ np.bitwise_and(wv1>=max([wv1[0], wv2[0]]), wv1<=min([wv1[-1], wv2[-1]])) ]
        Int1, Int2 = self.Intensity(wv).values, self.Intensity(wv).values
        spec3 = SpectrumClass(wv, Int1*Int2, wavelengthunitstr="nm")
        self.wavelengthunitstr = unit1
        other.wavelengthunitstr = unit2
        return spec3
    def __sub__(self, other):
        if isinstance(other, float):
            return SpectrumClass(self.wavelength_store(), self.intensity_store()-other, wavelengthunitstr=self.wavelengthunitstr)
        unit1, unit2 = self.wavelengthunitstr, other.wavelengthunitstr
        self.wavelengthunitstr, other.wavelengthunitstr = "nm", "nm"
        wv1, wv2 = self.wavelength_store(), other.wavelength_store()
        wv = wv1[ np.bitwise_and(wv1>=max([wv1[0], wv2[0]]), wv1<=min([wv1[-1], wv2[-1]])) ]
        Int1, Int2 = self.Intensity(wv).values, self.Intensity(wv).values
        spec3 = SpectrumClass(wv, Int1-Int2, wavelengthunitstr="nm")
        self.wavelengthunitstr = unit1
        other.wavelengthunitstr = unit2
        return spec3
    def __truediv__(self, other):
        if isinstance(other, float):
            return SpectrumClass(self.wavelength_store(), self.intensity_store()/other, wavelengthunitstr=self.wavelengthunitstr)
        unit1, unit2 = self.wavelengthunitstr, other.wavelengthunitstr
        self.wavelengthunitstr, other.wavelengthunitstr = "nm", "nm"
        wv1, wv2 = self.wavelength_store(), other.wavelength_store()
        wv = wv1[ np.bitwise_and(wv1>=max([wv1[0], wv2[0]]), wv1<=min([wv1[-1], wv2[-1]])) ]
        Int1, Int2 = self.Intensity(wv).values, self.Intensity(wv).values
        spec3 = SpectrumClass(wv, Int1/Int2, wavelengthunitstr="nm")
        self.wavelengthunitstr = unit1
        other.wavelengthunitstr = unit2
        return spec3
    # data member
    @property
    def wavelengthunitstr(self):
        return self.__wavelengthunitstr
    @wavelengthunitstr.setter
    def wavelengthunitstr(self, wavelengthunitstr):
        assert wavelengthunitstr[-1].lower() == 'm', "The unit of wavelength should be the length [e.x. m, nm]"
        factor = unit2unit(self.wavelengthunitstr[0:(len(self.wavelengthunitstr)-1)],wavelengthunitstr[0:(len(wavelengthunitstr)-1)])
        self._xScaling(factor)
        self.__wavelengthunitstr = wavelengthunitstr



if __name__ == '__main__':
    import doctest
    doctest.testmod()








