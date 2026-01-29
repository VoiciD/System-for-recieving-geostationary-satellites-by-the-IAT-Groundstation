#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 24 14:32:20 2026

@author: daniel
"""

import numpy as np
import matplotlib.pyplot as plt

k = 1.38*10**(-23)

P_T = 17.78                         #Sendeleistung Es'Hail-2 in W
P_T_dBm = 42.5
G_T = 50.12                         #Gewinn der Sendeantenne
EIRP = P_T * G_T                    #EIRP von Es'Hail-2
EIRP_dBm = 59.5
B = 2.7*10**3                       #Bandbreite des Downlinks

L_FR = 2.9*10**(20)                 #Freiraumdämpfung
L_FR_dB = 204.61
L_OT = 3.33                         #Senderseitige Fehlausrichtung
L_OT_dB = 5.23
L_OR = 0.69                         #Empfangsseitige Fehlasusrichtung
L_OR_dB = 0.69


L_ATklarerHimmel = 1.13             #Dämpfung in der Atmosphäre bei klarem Himmel
L_ATklarerHimmel_dB = 0.547
T_AklarerHimmel = 6.5               #Antennentemperatur bei klaren Himmel



G_R = 7244.36
G_LNC = 316227.76
G_SDR = 1412.54

L_sys = 5.02  
G_sys = G_LNC*G_SDR*(1/L_sys)

P_R_klarer_Himmel = EIRP*G_R*(1/L_FR)*(1/L_OT)*(1/L_OR)*(1/L_ATklarerHimmel)
P_R_klarer_Himmel_dB = 10*np.log10(P_R_klarer_Himmel/(0.001))

P_RX_klarer_Himmel = EIRP*G_R*(1/L_FR)*(1/L_OT)*(1/L_OR)*(1/L_ATklarerHimmel)*G_sys
P_RX_klarer_Himmel_dB = 10*np.log10(P_RX_klarer_Himmel/(0.001))


Link_Budget_klarer_Himmel_label = np.array(["Sende-\nLeistung","EIRP","Freiraum-\nDämpfung","Ausrichtungs-\nVerluste","Dämpfung\n Atmosphäre","Empfangene\nLeistung","Leistung\n am Ausgang"])
Link_Budget_klarer_Himmel = np.array([P_T,EIRP_dBm,EIRP_dBm-L_FR_dB,EIRP_dBm-L_FR_dB-L_OR_dB-L_OT_dB,EIRP_dBm-L_FR_dB-L_OR_dB-L_OT_dB-L_ATklarerHimmel_dB,P_R_klarer_Himmel_dB,P_RX_klarer_Himmel_dB])

G_Goon_dB = 65
L_FR_G_dB = 204.34
L_OT_G_dB = 1.91
P_R_G = -107.77
P_RX_G = -42.77


Link_Budgter_klarer_Himmel_Goonhilly = np.array([P_T,EIRP_dBm,EIRP_dBm-L_FR_G_dB,EIRP_dBm-L_FR_G_dB-L_OR_dB-L_OT_G_dB,EIRP_dBm-L_FR_G_dB-L_OR_dB-L_OT_G_dB-L_ATklarerHimmel_dB,P_R_G,P_RX_G])



plt.figure("LinkBudget clear Sky")
plt.title("Vergleich des Link Budgets bei klaren Himmel")
for i, val in enumerate(Link_Budget_klarer_Himmel):
    plt.annotate(f'{val:.2f}', (i, val), textcoords="offset points",
                 xytext=(0,10), ha='center')  # 10 Pkt über dem Punkt
    for i, val in enumerate(Link_Budgter_klarer_Himmel_Goonhilly):
        plt.annotate(f'{val:.2f}', (i, val), textcoords="offset points",
                     xytext=(0,-15), ha='center')  # 10 Pkt über dem Punkt
plt.plot(Link_Budget_klarer_Himmel_label,Link_Budget_klarer_Himmel,'o-',label="IAT")
plt.plot(Link_Budget_klarer_Himmel_label,Link_Budgter_klarer_Himmel_Goonhilly,'o-',label="Goonhilly")
plt.ylabel("Leistung in dBm")
plt.grid()
plt.legend()
plt.ylim([-180,90])
plt.xticks(range(len(Link_Budget_klarer_Himmel_label)), Link_Budget_klarer_Himmel_label, rotation=45)
plt.tight_layout(pad=0.5)
plt.show()