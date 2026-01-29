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






G_R = 7244.36
G_LNC = 316227.76
G_SDR = 1412.54

L_sys = 5.02  
G_sys = G_LNC*G_SDR*(1/L_sys)

T0 = 290

#Äquivalente Rauschtemperatur

Te1 = 133.4                #133.4
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

T_esys = Te1 + (TeLNC/(G1) ) + (Te2/(G1*GLNC) ) + (TeBiasTee/(G1*GLNC*G2) ) + (Te3/(G1*GLNC*G2*GBiasTee) ) + (TePatchfeld/(G1*GLNC*G2*G3) ) + (Te4/(G1*GLNC*G2*G3*GPatchfeld) ) + (TeRFSwitch /(G1*GLNC*G2*G3*GPatchfeld*G4) )+ (Te5 /(G1*GLNC*G2*G3*GPatchfeld*G4*GRFSwitch) )+ (TeSDR /(G1*GLNC*G2*G3*GPatchfeld*G4*GRFSwitch*G5) )
print("Äquivalente Rauschtemperatur Te,sys:",T_esys,"K")





#klarer Himmel
print("Für Bedingung klarer Himmel:")
L_ATklarerHimmel = 1.13             #Dämpfung in der Atmosphäre bei klarem Himmel
L_ATklarerHimmel_dB = 0.547
T_AklarerHimmel = 6.5               #Antennentemperatur bei klaren Himmel


P_R_klarer_Himmel = EIRP*G_R*(1/L_FR)*(1/L_OT)*(1/L_OR)*(1/L_ATklarerHimmel)
P_R_klarer_Himmel_dB = 10*np.log10(P_R_klarer_Himmel/(0.001))
print("empfangene Leistung $P_R$:",P_R_klarer_Himmel,"W")
print("empfangene Leistung $P_R$",P_R_klarer_Himmel_dB,"dBm")

P_RX_klarer_Himmel = EIRP*G_R*(1/L_FR)*(1/L_OT)*(1/L_OR)*(1/L_ATklarerHimmel)*G_sys
P_RX_klarer_Himmel_dB = 10*np.log10(P_RX_klarer_Himmel/(0.001))
print("Ausgangsleistung des Empfangssystems $P_{RX}$:",P_RX_klarer_Himmel,"W")
print("Ausgangsleistung des Empfangssystems $P_{RX}$",P_RX_klarer_Himmel_dB,"dBm")

N_i = k*T_AklarerHimmel*B
SNR_i_klarerHimmel = P_R_klarer_Himmel/N_i
SNR_i_klarerHimmel_dB = 10*np.log10(SNR_i_klarerHimmel)
print("SNR am Eingang bei klaren Himmel:",SNR_i_klarerHimmel_dB,"dB")


N_o = k*(T_AklarerHimmel+T_esys)*B
SNR_o_klarer_Himmel = P_R_klarer_Himmel/N_o
SNR_o_klarer_Himmel_dB = 10*np.log10(SNR_o_klarer_Himmel)
print("SNR am Ausgang des Empfangssystems:",SNR_o_klarer_Himmel_dB,"dB")



T_S_klarer_Himmel = (T_AklarerHimmel/L_sys)+T0*(1-(1/L_sys))+T_esys
CN0_klarer_Himmel = P_RX_klarer_Himmel/(k*T_S_klarer_Himmel)
CN0_klarer_Himmel_dBHz = 10*np.log10(CN0_klarer_Himmel)
print("Qualität des Downlinks:",CN0_klarer_Himmel_dBHz,"dBHz")

Link_Budget_klarer_Himmel_label = np.array(["Sende-\nLeistung","EIRP","Freiraum-\nDämpfung","Ausrichtungs-\nVerluste","Dämpfung\n Atmosphäre","Empfangene\nLeistung","Leistung\n am Ausgang"])
Link_Budget_klarer_Himmel = np.array([P_T,EIRP_dBm,EIRP_dBm-L_FR_dB,EIRP_dBm-L_FR_dB-L_OR_dB-L_OT_dB,EIRP_dBm-L_FR_dB-L_OR_dB-L_OT_dB-L_ATklarerHimmel_dB,P_R_klarer_Himmel_dB,P_RX_klarer_Himmel_dB])

plt.figure("LinkBudget clear Sky")
plt.title("Link Budget bei klaren Himmel")
for i, val in enumerate(Link_Budget_klarer_Himmel):
    plt.annotate(f'{val:.2f}', (i, val), textcoords="offset points",
                 xytext=(0,10), ha='center')  # 10 Pkt über dem Punkt
plt.plot(Link_Budget_klarer_Himmel_label,Link_Budget_klarer_Himmel,'o-')
plt.ylabel("Leistung in dBm")
plt.grid()
plt.ylim([-180,90])
plt.xticks(range(len(Link_Budget_klarer_Himmel_label)), Link_Budget_klarer_Himmel_label, rotation=45)
plt.tight_layout(pad=0.5)
plt.show()





#leichter Regen
print("Für die Bedingung leichter Regen:")
L_ATleichterRegen = 1.24
L_ATleichterRegen_dB = 0.947

T_AleichterRegen = 19.29

P_R_leichter_Regen = EIRP*G_R*(1/L_FR)*(1/L_OT)*(1/L_OR)*(1/L_ATleichterRegen)
P_R_leichter_Regen_dB = 10*np.log10(P_R_leichter_Regen/(0.001))
print("empfangene Leistung $P_R$:",P_R_leichter_Regen,"W")
print("empfangene Leistung $P_R$",P_R_leichter_Regen_dB,"dBm")

P_RX_leichter_Regen = EIRP*G_R*(1/L_FR)*(1/L_OT)*(1/L_OR)*(1/L_ATleichterRegen)*G_sys
P_RX_leichter_Regen_dB = 10*np.log10(P_RX_leichter_Regen/(0.001))
print("Ausgangsleistung des Empfangssystems $P_{RX}$:",P_RX_leichter_Regen,"W")
print("Ausgangsleistung des Empfangssystems $P_{RX}$",P_RX_leichter_Regen_dB,"dBm")

N_i = k*T_AleichterRegen*B
SNR_i_leichter_Regen = P_R_leichter_Regen/N_i
SNR_i_leichter_Regen_dB = 10*np.log10(SNR_i_leichter_Regen)
print("SNR am Eingang bei klaren Himmel:",SNR_i_leichter_Regen_dB,"dB")


N_o = k*(T_AleichterRegen+T_esys)*B
SNR_o_leichter_Regen = P_R_leichter_Regen/N_o
SNR_o_leichter_Regen_dB = 10*np.log10(SNR_o_leichter_Regen)
print("SNR am Ausgang des Empfangssystems:",SNR_o_leichter_Regen_dB,"dB")



T_S_leichter_Regen = (T_AleichterRegen/L_sys)+T0*(1-(1/L_sys))+T_esys
CN0_leichter_Regen = P_RX_leichter_Regen/(k*T_S_leichter_Regen)
CN0_leichter_Regen_dBHz = 10*np.log10(CN0_leichter_Regen)
print("Qualität des Downlinks:",CN0_leichter_Regen_dBHz,"dBHz")

Link_Budget_leichter_Regen_label = np.array(["Sende-\nLeistung","EIRP","Freiraum-\nDämpfung","Ausrichtungs-\nVerluste","Dämpfung\n Atmosphäre","Empfangene\nLeistung","Leistung\n am Ausgang"])
Link_Budget_leichter_Regen = np.array([P_T,EIRP_dBm,EIRP_dBm-L_FR_dB,EIRP_dBm-L_FR_dB-L_OR_dB-L_OT_dB,EIRP_dBm-L_FR_dB-L_OR_dB-L_OT_dB-L_ATleichterRegen_dB,P_R_leichter_Regen_dB,P_RX_leichter_Regen_dB])

plt.figure("LinkBudget light Rain")
plt.title("Link Budget bei leichten Regen")
for i, val in enumerate(Link_Budget_leichter_Regen):
    plt.annotate(f'{val:.2f}', (i, val), textcoords="offset points",
                 xytext=(0,10), ha='center')  # 10 Pkt über dem Punkt
plt.plot(Link_Budget_leichter_Regen_label,Link_Budget_leichter_Regen,'o-')
plt.ylabel("Leistung in dBm")
plt.grid()
plt.ylim([-180,90])
plt.xticks(range(len(Link_Budget_leichter_Regen_label)), Link_Budget_leichter_Regen_label, rotation=45)
plt.tight_layout(pad=0.5)
plt.show()


#Regen
print("Für die Bedingung Regen:")
L_ATRegen = 9.14
L_ATRegen_dB = 9.61

T_ARegen = 240.1

P_R_Regen = EIRP*G_R*(1/L_FR)*(1/L_OT)*(1/L_OR)*(1/L_ATRegen)
P_R_Regen_dB = 10*np.log10(P_R_Regen/(0.001))
print("empfangene Leistung $P_R$:",P_R_Regen,"W")
print("empfangene Leistung $P_R$",P_R_Regen_dB,"dBm")

P_RX_Regen = EIRP*G_R*(1/L_FR)*(1/L_OT)*(1/L_OR)*(1/L_ATRegen)*G_sys
P_RX_Regen_dB = 10*np.log10(P_RX_Regen/(0.001))
print("Ausgangsleistung des Empfangssystems $P_{RX}$:",P_RX_Regen,"W")
print("Ausgangsleistung des Empfangssystems $P_{RX}$",P_RX_Regen_dB,"dBm")

N_i = k*T_ARegen*B
SNR_i_Regen = P_R_Regen/N_i
SNR_i_Regen_dB = 10*np.log10(SNR_i_Regen)
print("SNR am Eingang bei klaren Himmel:",SNR_i_Regen_dB,"dB")


N_o = k*(T_ARegen+T_esys)*B
SNR_o_Regen = P_R_Regen/N_o
SNR_o_Regen_dB = 10*np.log10(SNR_o_Regen)
print("SNR am Ausgang des Empfangssystems:",SNR_o_Regen_dB,"dB")



T_S_Regen = (T_ARegen/L_sys)+T0*(1-(1/L_sys))+T_esys
CN0_Regen = P_RX_Regen/(k*T_S_Regen)
CN0_Regen_dBHz = 10*np.log10(CN0_Regen)
print("Qualität des Downlinks:",CN0_Regen_dBHz,"dBHz")

Link_Budget_Regen_label = np.array(["Sende-\nLeistung","EIRP","Freiraum-\nDämpfung","Ausrichtungs-\nVerluste","Dämpfung\n Atmosphäre","Empfangene\nLeistung","Leistung\n am Ausgang"])
Link_Budget_Regen = np.array([P_T,EIRP_dBm,EIRP_dBm-L_FR_dB,EIRP_dBm-L_FR_dB-L_OR_dB-L_OT_dB,EIRP_dBm-L_FR_dB-L_OR_dB-L_OT_dB-L_ATRegen_dB,P_R_Regen_dB,P_RX_Regen_dB])

plt.figure("LinkBudget Rain")
plt.title("Link Budget bei Regen")
for i, val in enumerate(Link_Budget_Regen):
    plt.annotate(f'{val:.2f}', (i, val), textcoords="offset points",
                 xytext=(0,10), ha='center')  # 10 Pkt über dem Punkt
plt.plot(Link_Budget_Regen_label,Link_Budget_Regen,'o-')
plt.ylabel("Leistung in dBm")
plt.grid()
plt.ylim([-180,90])
plt.xticks(range(len(Link_Budget_Regen_label)), Link_Budget_Regen_label, rotation=45)
plt.tight_layout(pad=0.5)
plt.show()

