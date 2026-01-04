#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 17:25:15 2025

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
A_r = 3*10**(-3)

f_s_t = 50

s_t = A_s * np.sin(2*np.pi*f_s_t*t)         #wanted signal
n_t = A_r * np.random.randn(len(t))         #Generating Noise with the length of the time axis

x_t = s_t + n_t

#Using the FFT
n = len(t)
fs = int(1/ts)                              #Defining the Sampling Frequency and those the sampling points
s_t_fft = np.fft.fft(x_t,fs)                #Doing the FFT


shifted_s_t_fft = np.fft.fftshift(s_t_fft)  #bringing the 0 Hz into the center
mag = abs(shifted_s_t_fft)/n                          #calculating the magnitude
freq = np.arange(-500,500,len(t)/fs)

mag = 10*np.log10(mag[int(fs/2):]/0.001)
freq = np.arange(0,500,len(t)/fs)



#Plotting
plt.figure()
plt.subplot(311)
plt.plot(t,s_t*1000,label = "Wanted signal")
plt.plot(t,n_t*1000,label = "Noise")
plt.ylabel("Voltage in [mV]")
plt.xlabel("Time in [s]")
plt.grid()
plt.legend(loc='upper right')
plt.subplot(312)
plt.plot(t,x_t*1000,label = "Mixed signal")
plt.ylabel("Voltage in [mV]")
plt.xlabel("Time in [s]")
plt.grid()
plt.legend(loc='upper right')
plt.subplot(313)
plt.plot(freq,mag, label = "FFT of the mixed signal")
plt.ylabel("Signalstrength in [dBm]")
plt.xlabel("Frequency in [Hz]")
plt.grid()
plt.legend(loc='upper right')
plt.tight_layout(h_pad=1.5, w_pad=0.8)   