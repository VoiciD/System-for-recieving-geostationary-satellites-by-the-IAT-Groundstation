#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 09:29:18 2025

@author: daniel
"""

import numpy as np
import matplotlib.pyplot as plt

# Link parameter
freq = 10.5
elevation = np.deg2rad(27.888)
tau =  np.deg2rad(-12.412)
cord_station = [53.055, 8.78]
c = 3e8
D_SAT = 38672.34e3

#Free Space Attenuation
lambda_center = c/(freq*10**9)
L_FR = 20*np.log10((4*np.pi*D_SAT)/lambda_center)
print("Free Space Attenuation:",L_FR,"dB")


#Rain Attenuation for p=0.01%
h_0 = 3                                     #Height of the isothermic barrier of the region from the groundstation[km]
h_Station = 0.023                           #Height of the groundstation above Sealevel [km]
h_R = h_0 + 0.36                            #Effectiv Rain height [km]
D_s = (h_R-h_Station)/(np.sin(elevation))   #Slant path length [km]
D_HP = D_s*np.cos(elevation)                #Horizontal Projection [km]
R_001 = 35                                  #Rainrate exxceeding p=0.01% the anual average [mm/h]

#von ITU-R P.838-3
k_H = 0.01217
k_V = 0.01129
alpha_H = 1.2571
alpha_V = 1.2156
k = (k_H + k_V + (k_H-k_V) * (np.cos(elevation))**2 * np.cos(2*tau))/2
alpha = (k_H * alpha_H + k_V * alpha_V + (k_H * alpha_H - k_V * alpha_V) * (np.cos(elevation))**2 * np.cos(2*tau)) / (2*k)

gamma_R001 = k*(R_001)**alpha               #specific rain attenuatuin for p=0.01%

r001 = 1 / (1 + 0.78 * np.sqrt((D_HP*gamma_R001) / freq) - 0.38 * (1 - np.exp(-2 * D_HP)))
cc001 = np.rad2deg(np.arctan((h_R-h_Station)/(D_HP*r001)))
if cc001 > np.rad2deg(elevation):
    D_R001 = (D_HP*r001)/np.cos(elevation)
else:
    D_R001 = (h_R-h_Station)/np.sin(elevation)
if abs(cord_station[0]) > 36:
    X = 36 - abs(cord_station[0])
else:
    X = 0
v001 = 1 / (1 + np.sqrt(np.sin(elevation)) * (31 * (1 - np.exp( (-1)* ( elevation/(1+X))))*(np.sqrt(D_R001 *gamma_R001))/(freq**2)-0.45))
D_Regen001 = D_R001*v001                    #Effectiv Path length
print("Effectiv Path lenght through the rain 0.01:",D_Regen001,"km")
L_Regen001 = gamma_R001*D_Regen001
print("Attenuation caused by rain exceeded for 0.01% of an avarage year:",L_Regen001,"dB")
# Attenuatuion for other percanteges
unit = 1

p = 5*unit
long = 53.055

if p >= 1*unit or abs(long) >= 36:
    beta = 0
elif p < 1*unit and abs(long) < 36 and elevation >= 25:
    beta = (-1)*0.005*(abs(long)-36)
else:
    beta = (-1)*0.005*(abs(long)-36)+1.8-4.25*np.sin(elevation)

exponent = (-1)*(0.655+0.033*np.log(p)-0.045*np.log(L_Regen001)-beta*(1-p)*np.sin(elevation))

L_Regenother = L_Regen001*(p/0.01)**exponent
print("Attenuation for Rainrates exceeding",p,"% of the time the anual avarage:",L_Regenother,"dB")





#Attenuation through Gases in the Atmosphäre
L_Gas = 0.1
print("Attenuation through Gas and Waterwapor in the Atmosphere:",L_Gas,"dB")
#Discrimation of the isolation trough crosspolarisation
p = 1               #percantage in %



C_f = 30*np.log10(freq)
if 8<= freq <= 20:
    Vf = 12.8*freq**0.19
elif 20<= freq <= 35:
    Vf = 22.6

C_A = Vf*np.log10(L_Regen001)
C_A = Vf*np.log10(L_Regenother)
C_tau = -10*np.log10(1-0.484*(1+np.cos(4*tau)))
C_theta = -40*np.log10(np.cos(elevation))

if p == 1:
    sigma = 0
elif p == 0.1:
    sigma = 5
elif p == 0.01:
    sigma = 10
elif p == 0.001:
    sigma = 15
else:
    sigma = 0

C_sigma = 0.0052*sigma**2

XPD_Regen = C_f-C_A+C_tau+C_theta+C_sigma               #Cross Polarisation Discrimination in dB
C_Eis = XPD_Regen*((0.3+0.1*np.log10(p))/2)             #Contribution of Ice in the clouds

XPD = XPD_Regen - C_Eis                                 #Cross Polarisation Discrimintion not exceeding p% of the year
print("Cross Polarisation Discrimination not exceeding",p,"% of the year",XPD,"dB")





