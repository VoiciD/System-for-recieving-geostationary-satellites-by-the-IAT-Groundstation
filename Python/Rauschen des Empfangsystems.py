#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 06:38:49 2026

@author: daniel
"""

import numpy as np
import matplotlib.pyplot as plt

#Äquivalente Rauschtemperatur
Te1 = 133.4  /2               #133.4
TeLNC = 139.2
Te2 = 200.1
TeBiasTee = 118.9
Te3 = 17.4
TePatchfeld = 58
Te4 = 8.7
TeRFSwitch = 20.3
Te5 = 8.7
TeSDR = 1539.9

G1 = 0.685
GLNC = 316227.77
G2 = 0.59
GBiasTee = 0.71
G3 = 0.94
GPatchfeld = 0.83
G4 = 0.97
GRFSwitch = 0.93
G5 = 0.97

Tesys = Te1 + (TeLNC/(G1) ) + (Te2/(G1*GLNC) ) + (TeBiasTee/(G1*GLNC*G2) ) + (Te3/(G1*GLNC*G2*GBiasTee) ) + (TePatchfeld/(G1*GLNC*G2*G3) ) + (Te4/(G1*GLNC*G2*G3*GPatchfeld) ) + (TeRFSwitch /(G1*GLNC*G2*G3*GPatchfeld*G4) )+ (Te5 /(G1*GLNC*G2*G3*GPatchfeld*G4*GRFSwitch) )+ (TeSDR /(G1*GLNC*G2*G3*GPatchfeld*G4*GRFSwitch*G5) )
print("Äquivalente Rauschtemperatur Te,sys:",Tesys,"K")