#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 13:46:56 2026

@author: daniel
"""

import numpy as np
import matplotlib.pyplot as plt

#Allgemeine Parameter
k = 1.38*10**(-23)

P_T = 17.78                         #Sendeleistung Es'Hail-2 in W
G_T = 50.12                         #Gewinn der Sendeantenne
EIRP = P_T * G_T                    #EIRP von Es'Hail-2
B = 2.7*10**3                       #Bandbreite des Downlinks

L_FR = 2.9*10**(20)                 #Freiraumdämpfung
L_OT = 3.33                         #Senderseitige Fehlausrichtung
L_OR = 0.69                         #Empfangsseitige Fehlasusrichtung

G_LNC = 316227.76
G_SDR = 1000
G_sys = G_LNC*G_SDR
T_esys = 336.63



#klarer Himmel

L_ATklarerHimmel = 1.13             #Dämpfung in der Atmosphäre bei klarem Himmel
T_AklarerHimmel = 6.5               #Antennentemperatur bei klaren Himmel


P_R = EIRP*G_T*(1/L_FR)*(1/L_OT)*(1/L_OR)*(1/L_ATklarerHimmel)
P_R_dB = 10*np.log10(P_R/(0.001))
print("empfangene Leistung $P_R$:",P_R,"W")
print("empfangene Leistung $P_R",P_R_dB,"dBm")

P_RX = EIRP*G_T*(1/L_FR)*(1/L_OT)*(1/L_OR)*(1/L_ATklarerHimmel)*G_sys
P_RX_dB = 10*np.log10(P_RX/(0.001))
print("Ausgangsleistung des Empfangssystems $P_{RX}$:",P_RX,"W")
print("Ausgangsleistung des Empfangssystems $P_{RX}$",P_RX_dB,"dBm")

N_i = k*T_AklarerHimmel*B
SNR_i_klarerHimmel = P_R/N_i
SNR_i_klarerHimmel_dB = 10*np.log10(SNR_i_klarerHimmel)
print("SNR am Eingang bei klaren Himmel:",SNR_i_klarerHimmel_dB,"dB")


N_o = k*(T_AklarerHimmel+T_esys)*B
SNR_o_klarer_Himmel = P_R/N_o
SNR_o_klarer_Himmel_dB = 10*np.log10(SNR_o_klarer_Himmel)
print("SNR am Ausgang des Empfangssystems:",SNR_o_klarer_Himmel_dB,"dB")


