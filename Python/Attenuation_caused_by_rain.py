#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 15:38:21 2025

@author: daniel
"""

import numpy as np
import matplotlib.pyplot as plt

elevation = np.deg2rad(27.888)  #elevation of the Antenna [°]
tau = np.deg2rad(-12.412)       #skew of the Antenna
h_0 = 3                         #Height of the isothermic barrier of the region from the groundstation[km]
h_Station = 0.023               #Height of the groundstation above Sealevel [km]
freq = 10.5                    #Frequency at which the link operates [GHz]
cordiantes_station = (53.05515290792716, 8.783348525839578,0.0)




#determination of the effective rain height [km]
h_R = h_0 + 0.36

#determination of path length the EM-Wave has to travel below the 
D_s = (h_R-h_Station)/(np.sin(elevation))

#determination of the horizontal projection caused by the path length of the EM-Wave
D_HP = D_s*np.cos(elevation)


#determination of the Rain intensity [mm/h] which exceeding the anual mean by 0.01% of the time
R_001 = 35                    #Mean in the northern part of Germany 35 to 40 mm/h 
R_graph = np.arange(0,40, 0.1 ) #For Graph Plotting 0 mm/H to 40mm/h

#determination of the frequency dependend coeffizients. Equations from the Book

# k_H = 3.949*10**(-6)*freq**(3.4078)
# k_V = 2.785*10**(-6)*freq**(3.5032)
# alpha_H = -0.7451*np.log10(freq)+2.0211
# alpha_V = -0.8083*np.log10(freq)+2.0723

#von ITU-R P.838-3
k_H = 0.01217
k_V = 0.01129
alpha_H = 1.2571
alpha_V = 1.2156
    

#determination of the specific rain attenuatuion
k = (k_H + k_V + (k_H-k_V) * (np.cos(elevation))**2 * np.cos(2*tau))/2
alpha = (k_H * alpha_H + k_V * alpha_V + (k_H * alpha_H - k_V * alpha_V) * (np.cos(elevation))**2 * np.cos(2*tau)) / (2*k)

gamma_R001 = k*(R_001)**alpha
print("y_R001:",gamma_R001,"dB/km")

#calculation horizontal reduction factor
r001 = 1 / (1 + 0.78 * np.sqrt((D_HP*gamma_R001) / freq) - 0.38 * (1 - np.exp(-2 * D_HP)))
#calculation vertical adjustment factor

cc001 = np.rad2deg(np.arctan((h_R-h_Station)/(D_HP*r001)))

if cc001 > np.rad2deg(elevation):
    D_R001 = (D_HP*r001)/np.cos(elevation)
else:
    D_R001 = (h_R-h_Station)/np.sin(elevation)



if abs(cordiantes_station[0]) > 36:
    X = 36 - abs(cordiantes_station[0])
else:
    X = 0

v001 = 1 / (1 + np.sqrt(np.sin(elevation)) * (31 * (1 - np.exp( (-1)* ( elevation/(1+X))))*(np.sqrt(D_R001 *gamma_R001))/(freq**2)-0.45))


#for graph 
A_graph = np.empty_like(R_graph)
gamma_Rgraph = np.empty_like(R_graph)
for i, R in enumerate(R_graph): 
    gamma_Rgraph[i] = k * (R)**alpha
    rgraph = 1 / (1 + 0.78 * np.sqrt((D_HP * gamma_Rgraph[i]) / freq) - 0.38 * (1 - np.exp(-2 * D_HP)))
    ccgraph = np.rad2deg(np.arctan((h_R - h_Station) / (D_HP * rgraph)))
    if ccgraph > np.rad2deg(elevation):
        D_Rgraph = (D_HP * rgraph) / np.cos(elevation)
    else:
        D_Rgraph = (h_R - h_Station) / np.sin(elevation)
    if abs(cordiantes_station[0]) > 36:
        X = 36 - abs(cordiantes_station[0])
    else:
        X = 0
    vgraph = 1 / (1 + np.sqrt(np.sin(elevation)) * (31 * (1 - np.exp(-1 * (elevation / (1 + X)))) * 
                      np.sqrt(D_Rgraph * gamma_Rgraph[i]) / (freq**2) - 0.45))
    D_Regengraph = D_Rgraph * vgraph
    A_graph[i] = gamma_Rgraph[i] * D_Regengraph

    

print("Vertikal adjusmentfaktor 0.01:",v001)

#calculation effective path length D_Regen
D_Regen001 = D_R001*v001

print("Effectiv Path lenght through the rain 0.01:",D_Regen001,"km")

#calculation worst case attenuation for rain exceeded for 0.01% of an avarage year
A_001 = gamma_R001*D_Regen001

print("worst case attenuation caused by rain exceeded for 0.01% of an avarage year:",A_001,"dB")


plt.figure("Attenuation caused by rain 10 GHz")
plt.title("Attenuation caused by rain for f = 10 GHz")
plt.plot(R_graph,A_graph)
plt.ylabel("Attenuation [dB]")
plt.xlabel("Rain intensity [mm/h]")
plt.grid()

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

exponent = (-1)*(0.655+0.033*np.log(p)-0.045*np.log(A_001)-beta*(1-p)*np.sin(elevation))

A_other = A_001*(p/0.01)**exponent
print("Attenuation for Rainrates exceeding",p,"% of the time the anual avarage:",A_other,"dB")







