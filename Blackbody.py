#!/usr/bin/env python3
# coding=utf-8
# -*- coding: utf8 -*-

import os
import sys
import numpy as np

# my module
from Material.SpectrumClass import SpectrumClass
#import matplotlib.pyplot as plt


def BlackbodySpectrum(AbsoluteTemp, Wavelength_List = np.linspace(380, 805, 86) ):
    """
    CIE1931XYZ is a function to calculate the CIE 1931 of the given spectrum.
    Reference: https://en.wikipedia.org/wiki/Black-body_radiation
    >>> Wavelength_List = list(range(100, 3005, 5))
    >>> T = 6000            # AbsoluteTemp
    """
    T = AbsoluteTemp
    h = 6.62607e-34     # Planck constant (J.s)
    k = 1.38065e-23     # Boltzmann constant (J/K)
    c = 3e8             # speed of light (m/s)
    v = c*1e9/Wavelength_List   #frequency (1/s)

    Bv_List = (8*np.pi*h*c)/((Wavelength_List*1e-9)**5) * (np.exp(h*v/(k*T))-1)
    Blackbody_spec = SpectrumClass(Wavelength_List, Bv_List)
    #plt.plot(Wavelength_List, Bv_List)
    #plt.show()

    return Blackbody_spec
