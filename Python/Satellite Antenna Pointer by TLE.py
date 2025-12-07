# -*- coding: utf-8 -*-
"""
Spyder-Editor

Dies ist eine temporäre Skriptdatei.
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from beyond.io.tle import Tle
from beyond.frames import create_station
from beyond.dates import Date, timedelta


#TLE for Es'Hail-2
print("Welcome to Antennapointer for the IAT Groundstation")
satlist = "Sat-List:Es'Hail-2,METOP-B,GOES-13,custom"
print(satlist)
sat_choise = True
while sat_choise == True:
    decision = input("Choose Satellite from Sat-List or insert own:")
    if decision == "Es'Hail-2":
        tle = Tle("""EsHail-2 (Q0-100) 
1 43700U 18090A   25300.12149642  .00000156  00000-0  00000-0 0  9993
2 43700   0.0213 118.9319 0001997 135.6013 210.7612  1.00274319 25349""")
        sat_choise = False
    elif decision == "METOP-B":         #does not work for LEO Satellites for whatever reason -> timedelta(hours=24) is the soloution, new problem: only displays 90° elevation and 0° azimuth
        tle = Tle("""METOP-B
1 38771U 12049A   25340.24647737  .00000314  00000-0  16390-3 0  9996
2 38771  98.6808  30.3151 0002626 158.5858 201.5430 14.21404836685856""")
        sat_choise = False
    elif decision == "GOES-13":
        tle = Tle("""GOES-13
1 29155U 06018A   25340.14158588 -.00000169  00000-0  00000-0 0  9998
2 29155   4.0310  78.7810 0060269 268.3601 139.6796  0.98788337 41348""")
        sat_choise = False
    elif decision == "custom":
        tle = input("Please insert TLE")
        sat_choise = False
    else:
        print("Please insert an option from the Sat-List")
        print(satlist)

#Groundstation at the IAT
IAT = create_station('IAT', (53.05515290792716, 8.783348525839578,0.0))
print("created station")
print("Name    Time      Azimuth    Elevation    Skew    Distance   Radial Velocity")
print("=========================================================")

for orb in IAT.visibility(tle.orbit(), start=Date.now(), stop=timedelta(hours=24), step=timedelta(minutes=60), events=True):
    # As all angles are given in radians,
    # there is some conversion to do
    azim = -np.degrees(orb.theta) % 360
    elev = np.degrees(orb.phi)
    #offset = 0
    #skew = np.rad2deg(np.arctan((np.sin(d_long))/(np.tan(lat_ant))))-offset
    r = orb.r / 1000.

    print("{event:10} {tle.name}  {date:%Y-%m-%dT%H:%M:%S.%f} {azim:7.2f} {elev:7.2f} {r:10.2f}".format(
        date=orb.date, r=r, azim=azim, elev=elev,
        tle=tle, event=orb.event if orb.event is not None else ""
    ))

    # Stop at the end of the first pass
    if orb.event and orb.event.info == "LOS":
        break


plt.figure()
ax = plt.subplot(111, projection='polar')
ax.set_title("Satellite Position relativ to the station")
ax.set_theta_direction(-1)
ax.set_theta_zero_location('N')
plt.plot(np.radians(azim), elev, '.',label=decision)
plt.legend()
ax.set_yticks(range(0, 90, 20))
ax.set_yticklabels(map(str, range(90, 0, -20)))
ax.set_rmax(90)

if "no-display" not in sys.argv:
    plt.show()