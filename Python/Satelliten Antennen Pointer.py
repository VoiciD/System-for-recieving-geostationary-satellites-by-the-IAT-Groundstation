#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  3 10:56:20 2025

@author: daniel
"""

import numpy as np


lat_ant = np.deg2rad(53.05515)
long_ant = np.deg2rad(8.78335)

lat_sat = np.deg2rad(0)
long_sat = np.deg2rad(25.8)

r_geo = 38600
r_earth = 6370

d_long = long_ant-long_sat

#Brechnung der Azimut
azimut = np.rad2deg(np.arctan((np.tan(d_long))/(np.sin(lat_ant))))+180
print("Azimut:",azimut,"°")

#Berechnung der Elevation

ratio = r_earth/(r_earth+r_geo)

elevation = np.rad2deg(np.arctan((np.cos(lat_ant)*np.cos(d_long)-ratio)/(np.sqrt(1-(np.cos(lat_ant)*np.cos(d_long))**2))))
print("Elevation:",elevation,"°")

#Berechnung Skew
offset = 0

skew = np.rad2deg(np.arctan((np.sin(d_long))/(np.tan(lat_ant))))-offset
print("Skew:",skew,"°")