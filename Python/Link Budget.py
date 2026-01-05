#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  5 09:50:54 2026

@author: daniel
"""

import numpy as np
import matplotlib.pyplot as plt

#Bestimmung der Sendeleistung 

P_TX = 100                              #Einspeiseleistung ist 100W
P_TX_dBm = 10*np.log10((P_TX)/(0.001))  #Einspeiseleistung in dBm
L_SAT = 1.5                             #Verluste auf dem Satelliten in dB
OBO = 6                                 #Rückfluss in dB

P_T = P_TX_dBm-L_SAT-OBO                #Sendeleistung in dBm
print("Sendeleistung von Es'Hail-2(QO-100):",P_T,"dBm")

G_T = 17                                #Gewinn der Sendeantenne in dBi   
EIRP_dBm = P_T+G_T                      #EIRP von EsHail-2 in dBm
EIRP = 10**((EIRP_dBm)/10)*0.001        #EIRP in W
print("EIRP von Es'Hail-2:",EIRP_dBm,"dBm") 
print("EIRP von Es'Hail-2:",EIRP,"W") 


D_SAT = 38672.34 * 10**3                #Entfernung von der Bodenstation zu Es'Hail-2 in km
S_SAT = (EIRP)/(4*np.pi*D_SAT)              #Strahlungsleistungsdichte in W/m²
print("Strahlunsleistungsdichte:",S_SAT,"W/m²")

#Bestimmung der empfangenen Leistung 

L_FR = 204.63                           #Freiraumdämdpfung in dB
L_Regen_001 = 8.792                     #Dämpfung für starke Regenschauer in dB
L_Regen_5 = 0.198                       #Dämpfung für leichte Regenschauer in dB
L_Gas = 0.1                             #Dämpfung für Gase in der Atmosphäre in dB
L_Nebel = 0.444                         #Dämpfung durch Nebel in dB
L_Wolken = 0.2                          #Dämpfung durch Wolken in dB

L_ATclearSky = L_Gas+L_Nebel
L_ATlightRain = L_Gas+L_Nebel+L_Regen_5+L_Wolken
L_ATRain =  L_Gas+L_Nebel+L_Regen_001+L_Wolken

L_OT = 5.23                             #Ausrichtungsverlsute auf der Senderseite
L_OR = 0.69                             #Ausrichtungsverluste auf der Empfängerseite

G_R = 38.6                              #Gewinn der Empfangsantenne

P_R_clearSky = EIRP_dBm-L_FR-L_ATclearSky-L_OT-L_OR+G_R
P_R_lightRain = EIRP_dBm-L_FR-L_ATlightRain-L_OT-L_OR+G_R
P_R_Rain = EIRP_dBm-L_FR-L_ATRain-L_OT-L_OR+G_R
print("Empfangsleistung bei klaren Himmel:",P_R_clearSky,"dBm")
print("Empfangsleistung bei leichten Regen:",P_R_lightRain,"dBm")
print("Empfangsleistung bei starken Regen:",P_R_Rain,"dBm")

#Verstärkung durch die Empfangsstation

L_Koax1 = 1.655
G_LNC = 55
L_Koax2 = 2.282
L_BiasTee = 1.5
L_Koax3 = 0.254
L_PatchPanel = 0.007 
L_Koax4 = 0.106
L_RFSwitch = 0.3
L_Koax5 = 0.106

G_ges = G_LNC-L_Koax1-L_Koax2-L_Koax3-L_Koax4-L_Koax5-L_BiasTee-L_PatchPanel-L_RFSwitch
print("Gesamtverstärkung des Empfangssystems:",G_ges,"dB")

S_in = P_R_clearSky
S_in1 = S_in-L_Koax1
S_out1 = S_in1+G_LNC
S_in2 = S_out1-L_Koax2
S_out2 = S_in2-L_BiasTee
S_in3 = S_out2-L_Koax3
S_out3 = S_in3-L_PatchPanel
S_in4 = S_out3-L_Koax4
S_out4 = S_in4-L_RFSwitch
S_in5 = S_out4-L_Koax5

print("Eingangsleistung am SDR bei klaren Himmel:",S_in5,"dBm")

#Linkbudget
Linkbudget_clearsky_labels = np.array(["Sendeleistung\n $P_T$","EIRP","Freiraum-\ndämpfung $L_{FR}$","Dämpfung\n in der Atmosphäre\n $L_{ATclearSky}$","Ausrichtungs-\n verluste $L_{\\theta T}$ $L_{\\theta R}$","Eingangsleisung\n am SDR $P_{RX}$"])
Linkbudget_clearsky_Werte = np.array([P_T,EIRP_dBm,EIRP_dBm-L_FR,EIRP_dBm-L_FR-L_ATclearSky,EIRP_dBm-L_FR-L_ATclearSky-L_OT-L_OR,S_in5])

plt.figure("LinkBudget clear Sky")
plt.title("Link Budget bei klaren Himmel")
for i, val in enumerate(Linkbudget_clearsky_Werte):
    plt.annotate(f'{val:.2f}', (i, val), textcoords="offset points",
                 xytext=(0,10), ha='center')  # 10 Pkt über dem Punkt
plt.plot(Linkbudget_clearsky_labels,Linkbudget_clearsky_Werte,'o-')
plt.ylabel("Leistung in [dBm]")
plt.grid()
plt.ylim([-180,90])
plt.xticks(range(len(Linkbudget_clearsky_labels)), Linkbudget_clearsky_labels, rotation=45)
plt.tight_layout(pad=0.5)
plt.show()

S_in = P_R_lightRain
S_in1 = S_in-L_Koax1
S_out1 = S_in1+G_LNC
S_in2 = S_out1-L_Koax2
S_out2 = S_in2-L_BiasTee
S_in3 = S_out2-L_Koax3
S_out3 = S_in3-L_PatchPanel
S_in4 = S_out3-L_Koax4
S_out4 = S_in4-L_RFSwitch
S_in5 = S_out4-L_Koax5

print("Eingangsleistung am SDR bei leichte Regen:",S_in5,"dBm")

#Linkbudget
Linkbudget_lightRain_labels = np.array(["Sendeleistung\n $P_T$","EIRP","Freiraum-\ndämpfung $L_{FR}$","Dämpfung\n in der Atmosphäre\n $L_{ATlightRain}$","Ausrichtungs-\n verluste $L_{\\theta T}$ $L_{\\theta R}$","Eingangsleisung\n am SDR $P_{RX}$"])
Linkbudget_lightRain_Werte = np.array([P_T,EIRP_dBm,EIRP_dBm-L_FR,EIRP_dBm-L_FR-L_ATlightRain,EIRP_dBm-L_FR-L_ATlightRain-L_OT-L_OR,S_in5])

plt.figure("LinkBudget lightRain")
plt.title("Link Budget bei leichten Regen")
for i, val in enumerate(Linkbudget_lightRain_Werte):
    plt.annotate(f'{val:.2f}', (i, val), textcoords="offset points",
                 xytext=(0,10), ha='center')  # 10 Pkt über dem Punkt
plt.plot(Linkbudget_clearsky_labels,Linkbudget_lightRain_Werte,'o-')
plt.ylabel("Leistung in [dBm]")
plt.grid()
plt.ylim([-180,90])
plt.xticks(range(len(Linkbudget_lightRain_labels)), Linkbudget_lightRain_labels, rotation=45)
plt.tight_layout()
plt.show()

S_in = P_R_Rain
S_in1 = S_in-L_Koax1
S_out1 = S_in1+G_LNC
S_in2 = S_out1-L_Koax2
S_out2 = S_in2-L_BiasTee
S_in3 = S_out2-L_Koax3
S_out3 = S_in3-L_PatchPanel
S_in4 = S_out3-L_Koax4
S_out4 = S_in4-L_RFSwitch
S_in5 = S_out4-L_Koax5

print("Eingangsleistung am SDR bei starken Regen:",S_in5,"dBm")

#Linkbudget
Linkbudget_Rain_labels = np.array(["Sendeleistung\n $P_T$","EIRP","Freiraum-\ndämpfung $L_{FR}$","Dämpfung\n in der Atmosphäre\n $L_{ATRain}$","Ausrichtungs-\n verluste $L_{\\theta T}$ $L_{\\theta R}$","Eingangsleisung\n am SDR $P_{RX}$"])
Linkbudget_Rain_Werte = np.array([P_T,EIRP_dBm,EIRP_dBm-L_FR,EIRP_dBm-L_FR-L_ATRain,EIRP_dBm-L_FR-L_ATRain-L_OT-L_OR,S_in5])

plt.figure("LinkBudget Rain")
plt.title("Link Budget bei starken Regen")
for i, val in enumerate(Linkbudget_Rain_Werte):
    plt.annotate(f'{val:.2f}', (i, val), textcoords="offset points",
                 xytext=(0,10), ha='center')  # 10 Pkt über dem Punkt
plt.plot(Linkbudget_Rain_labels,Linkbudget_Rain_Werte,'o-')
plt.ylabel("Leistung in [dBm]")
plt.grid()
plt.ylim([-180,90])
plt.xticks(range(len(Linkbudget_Rain_labels)), Linkbudget_Rain_labels, rotation=45)
plt.tight_layout()
plt.show()






