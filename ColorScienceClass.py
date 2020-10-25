#!/usr/bin/env python3
# Copyright (c) 2019 Zih-Rou Cyue and Wei-Kai Lee. All rights reserved

# coding=utf-8
# -*- coding: utf8 -*-

# python module
import os
import sys
import collections
import numpy as np


# my module
MCPath = os.path.dirname(os.path.abspath(__file__))

from ReaderWriter.Reader.readfile import ColFileRead
from Material.SpectrumClass import SpectrumClass
from Help.myNumericalIntegration import myNumericalIntegration

import Blackbody

CIE1931XYZ = collections.namedtuple("CIE1931XYZ","X Y Z")    
CIE1931xyz = collections.namedtuple("CIE1931xyz","x y z")
CIE1931RGB = collections.namedtuple("CIE1931RGB","R G B")
CIE1931rgb = collections.namedtuple("CIE1931rgb","r g b")
CIE1960UVW = collections.namedtuple("CIE1960UVW","U V W")
CIE1960uv = collections.namedtuple("CIE1960uv","u v")
CIE1964UVW = collections.namedtuple("CIE1964UVW","U V W")
CIE1976u_v_ = collections.namedtuple("CIE1976u_v_","u_ v_")
CIE1976Luv = collections.namedtuple("CIE1976Luv","L u v")
CIE1976Lab = collections.namedtuple("CIE1976Lab","L a b")
CRI = collections.namedtuple("CRI","Ri1 Ri2 Ri3 Ri4 Ri5 Ri6 Ri7 Ri8")

path_cie1931 = os.path.join(MCPath,'Data') 
class ColorScienceClass:
    def __init__(self):
        self.ReadCIE1931ColorMatchingFunction()
        self.ReadTestingSpectrum()
    # Read Function 
    def ReadCIE1931ColorMatchingFunction(self,path_cie1931=path_cie1931, file_cie1931='CIE1931_color_matching_function.txt'):
        TagList_cie1931 = [['wavelength','cie1931_x','cie1931_y','cie1931_z']]
        validFile, cie1931Dict, TagDict, unitDict, groupNumber = ColFileRead(path_cie1931, file_cie1931, TagList_cie1931)
        self.__CIE1931CMF = collections.defaultdict()
        self.__CIE1931CMF["x"] = SpectrumClass(cie1931Dict["wavelength"], cie1931Dict["cie1931_x"])
        self.__CIE1931CMF["y"] = SpectrumClass(cie1931Dict["wavelength"], cie1931Dict["cie1931_y"])
        self.__CIE1931CMF["z"] = SpectrumClass(cie1931Dict["wavelength"], cie1931Dict["cie1931_z"])
        return self.__CIE1931CMF
    def ReadTestingSpectrum(self,path_cri=path_cie1931, file_cri='CRI_Testing_Spectum.txt'):
        TagList_cri = [['wavelength','tsc_1','tsc_2','tsc_3','tsc_4','tsc_5','tsc_6','tsc_7','tsc_8']]
        validFile, criDict, TagDict, unitDict, groupNumber = ColFileRead(path_cri, file_cri, TagList_cri)
        self.__TestObjSpecList = [SpectrumClass(criDict["wavelength"],criDict["tsc_"+str(ii+1)],wavelengthunitstr="nm") for ii in range(8)]
        return self.__TestObjSpecList
    # Standard Light Source                                                               
    def Standard_Illuminant(self, illum):
        #illum:A C D_65 F2 TL4 UL_3000 D_50 D_60 D_75
        Xn = collections.namedtuple("Xn","A C E D_65 F2 TL4 UL_3000 D_50 D_55 D_60 D_75")
        xn = Xn(109.85, 98.07, 100, 95.04, 99.14, 103.25, 107.99, 96.42, 95.68, 95.23, 94.97)
        Zn = collections.namedtuple("Zn","A C E D_65 F2 TL4 UL_3000 D_50 D_55 D_60 D_75")
        zn = Zn(35.58, 118.22, 100, 108.89, 67.32, 65.90, 33.91, 82.52, 92.15, 100.86, 122.64)
        return getattr(xn,illum), 100, getattr(zn,illum)
    # CIE
    def CIE1931XYZ(self,spec):
        """
        CIE1931XYZ is a function to calculate the CIE 1931 of the given spectrum.
        Reference: Website
        >>> cie1931XYZ = CS.CIE1931XYZ(spec)
        >>> print(cie1931XYZ)
        """

        wv = self.__CIE1931CMF["x"].wavelength_store()
        spec_cie= spec.Intensity(wv,OutofRangeValue=0.0)
        X = myNumericalIntegration(wv, spec_cie.values*self.__CIE1931CMF["x"].intensity_store())
        Y = myNumericalIntegration(wv, spec_cie.values*self.__CIE1931CMF["y"].intensity_store())
        Z = myNumericalIntegration(wv, spec_cie.values*self.__CIE1931CMF["z"].intensity_store())
        cie1931XYZ = CIE1931XYZ(X,Y,Z)
        return cie1931XYZ
    def CIE1931xyz(self,spec):
        """
        CIE1931XYZ is a function to calculate the CIE 1931 of the given spectrum.
        Reference: Website
        >>> cie1931xyz = CS.CIE1931xyz(spec)
        >>> print(cie1931xyz)
        """
        cie1931XYZ = self.CIE1931XYZ(spec)
        XYZ = (cie1931XYZ.X+cie1931XYZ.Y+cie1931XYZ.Z)
        if XYZ != 0:
            x = cie1931XYZ.X/XYZ
            y = cie1931XYZ.Y/XYZ
            z = cie1931XYZ.Z/XYZ
        else:
            x,y,z = 0,0,0
        cie1931xyz = CIE1931xyz(x,y,z)
        return cie1931xyz
    def CIE1931RGB(self,spec):
        """
        CIE1931XYZ is a function to calculate the CIE 1931 of the given spectrum.
        Reference: Website
        >>> cie1931RGB = CS.CIE1931RGB(spec)
        >>> print(cie1931RGB)
        """
        cie1931XYZ = self.CIE1931XYZ(spec)
        R = 0.4185*cie1931XYZ.X-0.1587*cie1931XYZ.Y-0.0828*cie1931XYZ.Z
        G = -0.0912*cie1931XYZ.X+0.2524*cie1931XYZ.Y+0.0157*cie1931XYZ.Z
        B =  0.0009*cie1931XYZ.X+0.0025*cie1931XYZ.Y+0.1786*cie1931XYZ.Z
        cie1931RGB = CIE1931RGB(R,G,B)
        return cie1931RGB
    def CIE1931rgb(self,spec):
        """
        CIE1931XYZ is a function to calculate the CIE 1931 of the given spectrum.
        Reference: Website
        >>> cie1931rgb = CS.CIE1931rgb(spec)
        >>> print(cie1931rgb)
        """
        cie1931RGB = self.CIE1931RGB(spec)
        RGB = (cie1931RGB.R+cie1931RGB.G+cie1931RGB.B)
        if RGB != 0:
            r = cie1931RGB.R/RGB
            g = cie1931RGB.G/RGB
            b = cie1931RGB.B/RGB
        else:
            r,g,b = 0,0,0
        cie1931rgb = CIE1931rgb(r,g,b)
        return cie1931rgb
    def CIE1960UVW(self,spec):
        """
        CIE1931XYZ is a function to calculate the CIE 1931 of the given spectrum.
        Reference: Website
        >>> cie1960UVW = CS.CIE1960UVW(spec)
        >>> print(cie1960UVW)
        """
        cie1931XYZ = self.CIE1931XYZ(spec)
        [U,V,W] = [2/3*cie1931XYZ.X, cie1931XYZ.Y, 0.5*(-cie1931XYZ.X+3*cie1931XYZ.Y+cie1931XYZ.Z)]
        cie1960UVW = CIE1960UVW(U,V,W)
        return cie1960UVW
    def CIE1960uv(self,spec):
        """
        CIE1931XYZ is a function to calculate the CIE 1931 of the given spectrum.
        Reference: Website
        >>> cie1960uv = CS.CIE1960uv(spec)
        >>> print(cie1960uv)
        """
        cie1960UVW = self.CIE1960UVW(spec)
        UVW = (cie1960UVW.U+cie1960UVW.V+cie1960UVW.W)
        if UVW!=0:
            u = cie1960UVW.U/UVW
            v = cie1960UVW.V/UVW        
        else:
            u,v = 0,0
        cie1960uv = CIE1960uv(u,v)
        return cie1960uv
    def CIE1964UVW(self,spec):
        """
        CIE1931XYZ is a function to calculate the CIE 1931 of the given spectrum.
        Reference: Website
        >>> cie1964UVW = CS.CIE1964UVW(spec)
        >>> print(cie1964UVW)
        """
        cie1931XYZ = self.CIE1931XYZ(spec)
        cie1960uv = self.CIE1960uv(spec)
        # default un = 0.2009, vn = 0.4610, calculate U* V* W*
        W = 25*pow(cie1931XYZ.Y,1/3)-17
        [U,V] = [13*W*(cie1960uv.u-0.2009), 13*W*(cie1960uv.v-0.4610)]
        cie1964UVW = CIE1964UVW(U,V,W)
        return cie1964UVW
    def CIE1976u_v_(self,spec):
        """
        CIE1931XYZ is a function to calculate the CIE 1931 of the given spectrum.
        Reference: Website
        >>> cie1976u_v_ = CS.CIE1976u_v_(spec)
        >>> print(cie1976u_v_)
        """
        #calculate u' v'    
        cie1931xyz = self.CIE1931xyz(spec)
        de = (12*cie1931xyz.y-2*cie1931xyz.x+3)
        if de!=0:
            u_ = 4*cie1931xyz.x/de
            v_ = 9*cie1931xyz.y/de
        else:
            u_, v_ = 0,0
        cie1976u_v_ = CIE1976u_v_(u_,v_)
        return cie1976u_v_
    def CIE1976Luv(self,spec,illum = "D_65"):
        """
        CIE1931XYZ is a function to calculate the CIE 1931 of the given spectrum.
        Reference: Website
        >>> cie1976Luv = CS.CIE1976Luv(spec)
        >>> print(cie1976Luv)
        """
        # default Yn = 100,un = 0.2009, vn = 0.4610, calculate L*,u*,v*    
        cie1931XYZ = self.CIE1931XYZ(spec)
        cie1976u_v_ = self.CIE1976u_v_(spec)
        [Xn,Yn,Zn] = self.Standard_Illuminant(illum)
        L = 116 * self.lab_fx(cie1931XYZ.Y / Yn) - 16
        [u, v] = [13*L*(cie1976u_v_.u_-0.2009),13*L*(cie1976u_v_.v_-0.4610)]
        cie1976Luv = CIE1976Luv(L,u,v)
        return cie1976Luv
    def CIE1976Lab(self,spec,illum = "D_65", ifillum = 0, defaultillum = Blackbody.BlackbodySpectrum(6500)):
        """
        CIE1931XYZ is a function to calculate the CIE 1931 of the given spectrum.
        Reference: Website
        >>> cie1976Lab = CS.CIE1976Lab(spec)
        >>> print(cie1976Lab)
        """
        cie1931XYZ = self.CIE1931XYZ(spec)
        temptspec = SpectrumClass( defaultillum.wavelength_store(), 
                                   defaultillum.Intensity_NormalizedByMax(defaultillum.wavelength_store(), alpha=100.0), 
                                   wavelengthunitstr=defaultillum.wavelengthunitstr)
        cie1931XYZ_illum = self.CIE1931XYZ(temptspec)
        if ifillum == 1:
            [Xn, Yn, Zn] = [cie1931XYZ_illum.X, cie1931XYZ_illum.Y, cie1931XYZ_illum.Z]
        else:
            [Xn,Yn,Zn] = self.Standard_Illuminant(illum)
        L = 116*self.lab_fx(cie1931XYZ.Y/Yn)-16
        [a, b] = [500 * (self.lab_fx(cie1931XYZ.X/Xn)-self.lab_fx(cie1931XYZ.Y/Yn)), 200*(self.lab_fx(cie1931XYZ.Y/Yn)-self.lab_fx(cie1931XYZ.Z/Zn))]
        cie1976Lab = CIE1976Lab(L,a,b)
        return cie1976Lab
    def lab_fx(self, num):
        if num > 0.008856:
            fx = pow(num,1/3)
        else:
            fx = 7.787*num + 16/116
        return fx
    def Chroma_Cuv(self,spec):
        """
        CIE1931XYZ is a function to calculate the CIE 1931 of the given spectrum.
        Reference: Website
        >>> C_uv = CS.Chroma_Cuv(spec)
        >>> print(C_uv)
        """
        cie1976Luv = self.CIE1976Luv(spec)
        C_uv = np.sqrt(pow(cie1976Luv.u,2)+pow(cie1976Luv.v,2))
        return C_uv
    def Chroma_Cab(self,spec):
        """
        CIE1931XYZ is a function to calculate the CIE 1931 of the given spectrum.
        Reference: Website
        >>> C_ab = CS.Chroma_Cab(spec)
        >>> print(C_ab)
        """
        cie1976Lab = self.CIE1976Lab(spec)
        C_ab = np.sqrt(pow(cie1976Lab.a,2)+pow(cie1976Lab.b,2))
        return C_ab
    def Hue_Huv(self,spec):
        """
        CIE1931XYZ is a function to calculate the CIE 1931 of the given spectrum.
        Reference: Website
        >>> H_uv = CS.Hue_Huv(spec)
        >>> print(H_uv)
        """
        cie1976Luv = self.CIE1976Luv(spec)
        H_uv = np.arctan(cie1976Luv.v/cie1976Luv.u)
        return H_uv
    def Hue_Hab(self,spec):
        """
        CIE1931XYZ is a function to calculate the CIE 1931 of the given spectrum.
        Reference: Website
        >>> H_ab = CS.Hue_Hab(spec)
        >>> print(H_ab)
        """
        cie1976Lab = self.CIE1976Lab(spec)
        H_ab = np.arctan(cie1976Lab.b/cie1976Lab.a)
        return H_ab
    def CCT(self,spec):
        """
        CIE1931XYZ is a function to calculate the CIE 1931 of the given spectrum.
        Reference: Website
        >>> cct = CS.CCT(spec)
        >>> print(cct)
        """
        cie1931xyz = self.CIE1931xyz(spec)
        # xe=0.3320 ye=0.1858
        n = (cie1931xyz.x-0.3320)/(cie1931xyz.y-0.1858)
        cct = -449*pow(n,3)+3525*pow(n,2)-6823.3*n+5520.33
        return cct
    def CRI(self,spec):
        """
        CIE1931XYZ is a function to calculate the CIE 1931 of the given spectrum.
        Reference: Website
        >>> cri, Ra = CS.CRI(spec)
        >>> print(cri, Ra)
        """
        temptspec = Blackbody.BlackbodySpectrum(AbsoluteTemp=self.CCT(spec))
        bk_spec = SpectrumClass( temptspec.wavelength_store(), 
                                 temptspec.Intensity(temptspec.wavelength_store(), alpha=100.0), 
                                 wavelengthunitstr=temptspec.wavelengthunitstr)
        spec_TestSpec_List = [ self.__TestObjSpecList[jj]*spec  for jj in range(8)]
        bk_spec_TestSpec_List = [ self.__TestObjSpecList[jj]*bk_spec  for jj in range(8)]
        ri_List = [ self.Ri(self.CIE1964UVW(spec_TestSpec_List[ii]), self.CIE1964UVW(bk_spec_TestSpec_List[ii])) for ii in range(8)]
        cri = CRI(*ri_List)
        Ra = np.mean(ri_List)
        return cri, Ra
    def Ri(self, cie1964_1, cie1964_2):
        delta_E = np.sqrt(pow(cie1964_1.U-cie1964_2.U,2)+pow(cie1964_1.V-cie1964_2.V,2)+pow(cie1964_1.W-cie1964_2.W,2))
        Ri = 100-4.6*delta_E
        return Ri
    def Lightness(self, spec):
        """
        CIE1931XYZ is a function to calculate the CIE 1931 of the given spectrum.
        Reference: Website
        >>> l = CS.Lightness(spec)
        >>> print(l)
        """
        cie1976Luv = self.CIE1976Luv(spec)
        return cie1976Luv.L
    @property
    def CIE1931CMF(self):
       return self.__CIE1931CMF

if __name__ == '__main__':
    from Material.SpectrumReader import SpectrumReader
    validFile, spec = SpectrumReader(fpath='./Material',filename='CBP_Ir(ppy)2acac_8wt', printInformationBool=True, FilenameExtension = 'spc') 
    if validFile:
        print('Successfully read spectrum.')
    else:
        print('Fail read spectrum.')
        sys.exit()

    CS = ColorScienceClass()
    #import doctest
    #doctest.testmod()
    print('CIE1931 xyz : ', CS.CIE1931xyz(spec) )
    print('CIE1931 rgb : ', CS.CIE1931rgb(spec) )
    print('CIE1960 uv  : ', CS.CIE1960uv(spec) )
    print('CIE1976 u*v*: ', CS.CIE1976u_v_(spec) )









