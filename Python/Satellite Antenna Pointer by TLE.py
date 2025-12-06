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
tle_eshail2 = Tle("""EsHail-2 (Q0-100) 
1 43700U 18090A   25300.12149642  .00000156  00000-0  00000-0 0  9993
2 43700   0.0213 118.9319 0001997 135.6013 210.7612  1.00274319 25349""")


#Groundstation at the IAT
IAT = create_station('IAT', (53.05515290792716, 8.783348525839578,0.0))

print("Name    Time      Azim    Elev    Distance   Radial Velocity")
print("=========================================================")

for orb in IAT.visibility(tle_eshail2.orbit(), start=Date.now(), stop=timedelta(hours=1), step=timedelta(minutes=2), events=True):

    # As all angles are given in radians,
    # there is some conversion to do
    azim = -np.degrees(orb.theta) % 360
    elev = np.degrees(orb.phi)
    r = orb.r / 1000.

    print("{event:10} {tle.name}  {date:%Y-%m-%dT%H:%M:%S.%f} {azim:7.2f} {elev:7.2f} {r:10.2f}".format(
        date=orb.date, r=r, azim=azim, elev=elev,
        tle=tle_eshail2, event=orb.event if orb.event is not None else ""
    ))

    # Stop at the end of the first pass
    if orb.event and orb.event.info == "LOS":
        break


plt.figure()
ax = plt.subplot(111, projection='polar')
ax.set_theta_direction(-1)
ax.set_theta_zero_location('N')
plt.plot(np.radians(azim), elev, '.')
ax.set_yticks(range(0, 90, 20))
ax.set_yticklabels(map(str, range(90, 0, -20)))
ax.set_rmax(90)

if "no-display" not in sys.argv:
    plt.show()