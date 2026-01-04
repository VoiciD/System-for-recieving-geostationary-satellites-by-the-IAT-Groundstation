#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 18:43:24 2025

@author: daniel
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig


#Define Samplingtime and Sampling Frequency

ts = 0.001              #Samplingtime 0.001s

t = np.arange(0,1,ts)   #time axis


#Define the signals and noise
A_s = 1*10**(-3)
A_r = 1*10**(-3)
A_i = 0.1*10**(-3)


f_s_t = 200                                 #Input Frequency
f_i_t = 100                                 #Image Frequency
f_n_t = 150                                 #LO Frequency


s_t = A_s * np.cos(2*np.pi*f_s_t*t)         #Input Signal
i_t = A_i * np.cos(2*np.pi*f_i_t*t)         #Image Signal
n_t = A_r * np.cos(2*np.pi*f_n_t*t)         #LO Signal

x_t = s_t * n_t                             #Mixing
xsp_t = i_t * n_t                             #Mixing


#Using the FFT
n = len(t)
fs = int(1/ts)                              #Defining the Sampling Frequency and those the sampling points
x_t_fft = np.fft.fft(x_t,fs)                #Doing the FFT
s_t_fft = np.fft.fft(s_t,fs)                #Doing the FFT
n_t_fft = np.fft.fft(n_t,fs)                #Doing the FFT
i_t_fft = np.fft.fft(i_t,fs)                #Doing the FFT
xsp_t_fft = np.fft.fft(xsp_t,fs)                #Doing the FFT


shifted_x_t_fft = np.fft.fftshift(x_t_fft)  #bringing the 0 Hz into the center
shifted_s_t_fft = np.fft.fftshift(s_t_fft)  #bringing the 0 Hz into the center
shifted_n_t_fft = np.fft.fftshift(n_t_fft)  #bringing the 0 Hz into the center
shifted_i_t_fft = np.fft.fftshift(i_t_fft)  #bringing the 0 Hz into the center
shifted_xsp_t_fft = np.fft.fftshift(xsp_t_fft)  #bringing the 0 Hz into the center

mag_x = abs(shifted_x_t_fft)/n                          #calculating the magnitude
mag_s = abs(shifted_s_t_fft)/n                          #calculating the magnitude
mag_n = abs(shifted_n_t_fft)/n                          #calculating the magnitude
mag_i = abs(shifted_i_t_fft)/n                          #calculating the magnitude
mag_xsp = abs(shifted_xsp_t_fft)/n                          #calculating the magnitude

mag_x_dB = 10*np.log10(mag_x[int(fs/2):]/0.001)
mag_s_dB = 10*np.log10(mag_s[int(fs/2):]/0.001)
mag_n_dB = 10*np.log10(mag_n[int(fs/2):]/0.001)
mag_i_dB = 10*np.log10(mag_i[int(fs/2):]/0.001)
mag_xsp_dB = 10*np.log10(mag_xsp[int(fs/2):]/0.001)

freq = np.arange(0,500,len(t)/fs)

#Plotting
plt.figure()
plt.subplot(211)
plt.plot(freq,mag_s_dB, label = "HF-Signal")
plt.plot(freq,mag_n_dB, label = "LO-Signal")
plt.plot(freq,mag_i_dB, label = "SP-Signal")
plt.ylabel("Signalstrength in [dBm]")
plt.xlabel("Frequency in [MHz]")
plt.grid()
plt.legend(loc='upper right')
plt.tight_layout(h_pad=1.5, w_pad=0.8) 
plt.subplot(212)
plt.plot(freq,mag_x_dB, label = "ZF-Signal")
plt.plot(freq,mag_xsp_dB, label = "SP-Signal")
plt.ylabel("Signalstrength in [dBm]")
plt.xlabel("Frequency in [MHz]")
plt.grid()
plt.legend(loc='upper right')
plt.tight_layout(h_pad=1.5, w_pad=0.8)   