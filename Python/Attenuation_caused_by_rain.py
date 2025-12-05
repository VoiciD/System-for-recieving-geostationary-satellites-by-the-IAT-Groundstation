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





#determination of the effective rain height [km]
h_R = h_0 + 0.36

#determination of path length the EM-Wave has to travel below the 
D_s = (h_R-h_Station)/(np.sin(elevation))

#determination of the horizontal projection caused by the path length of the EM-Wave
D_HP = D_s*np.cos(elevation)


#determination of the Rain intensity [mm/h] which exceeding the anual mean by 0.01% of the time
R_001 = 30                    #Mean in the northern part of Germany 35 to 40 mm/h



#determination of the frequency dependend coeffizients
if freq < 1:
    print("Below minimium fequency f=1 GHz")
elif freq == 1:
    k_H = 0.0000387
    k_V = 0.0000352
    alpha_H = 0.912
    alpha_V = 0.880

elif 1 < freq < 2:      # NOT CORRECT
    k_H = 0.0000387
    k_V = 0.0000352
    alpha_H = 0.912
    alpha_V = 0.880
    
elif 10 < freq < 12:
    k_H = 3.949*10**(-6)*freq**(3.4078)
    k_V = 2.785*10**(-6)*freq**(3.5032)
    alpha_H = -0.7451*np.log10(freq)+2.0211
    alpha_V = -0.8083*np.log10(freq)+2.0723
    

#determination of the specific rain attenuatuion
k = (k_H+k_V+(k_H-k_V)*(np.cos(elevation))**2+np.cos(2*tau))/2
alpha = ((k_H*alpha_H)+(k_V*alpha_V)+((k_H*alpha_H)-(k_V*alpha_V)*(np.cos(elevation))**2+np.cos(2*tau)))/(2*k)

y_R = k*(R_001)**alpha
print("y_R:",y_R,"dB/km")

#calculation horizontal reduction factor
r001 = (1+0.78*np.sqrt((D_HP*y_R)/freq)-0.38*(1-np.exp(-2*D_HP)))**(-1)
#calculation vertical reduction factor





