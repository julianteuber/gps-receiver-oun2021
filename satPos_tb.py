# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 10:29:12 2021

@author: julian
"""

import os
import pandas as pd
import numpy as np

from datetime import datetime, timezone, timedelta
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from readRinex import readRinex
from extractEphi import extractEphi
from satPos import satPos, sat2enu, enu2ae
from coordTrans import dec2dez, dez2dec, geo2cart, cart2geo

from numpy import interp

rinexPath = "C:/Users/julian/Documents/Studium/ET - Master/Module/OuN/Praktikum/RinexFiles"
outputPath = "C:/Users/julian/Documents/Studium/ET - Master/Module/OuN/Praktikum/Python/sat_data"
#rinexFileName = "delf1320.21n"
rinexFileName = "delf1570.21n"
rinexFullPath = os.path.join(rinexPath,rinexFileName)
rnx_data = readRinex(rinexFullPath)

#from_datetime = pd.to_datetime('2021-05-12 09:40:46')
#to_datetime   = pd.to_datetime('2021-05-12 10:11:22')

from_datetime = pd.to_datetime('2021-06-06 00:00:00')
to_datetime   = pd.to_datetime('2021-06-07 00:00:00')

svprn_list = [1,6,25,30]
#svprn_list = list(range(32))
ephimeris = extractEphi(rnx_data, from_datetime, to_datetime, svprn_list)

pd.DataFrame(ephimeris).to_csv(os.path.join(outputPath,'ephi.csv'), sep=';')

#time_now = datetime.now(timezone.utc)
time_now = pd.to_datetime('2021-06-06 00:00:00')
time_vec = np.empty((0,0), float)
s_pos    = [ np.matrix(np.empty((0,3), float)) for i in range(len(ephimeris)) ]
ae_data  = [ np.matrix(np.empty((0,2), float)) for i in range(len(ephimeris)) ]

user_longitude = 4.0, 23.0, 14.845
user_latitude  = 51.0, 59.0, 9.6579
height = 75.0
longitude_deg  = dec2dez(*user_longitude)
latitude_deg   = dec2dez(*user_latitude)
userPos_vec    = np.array(geo2cart(longitude_deg,latitude_deg,height))

for i in range(200):
    time_vec = np.append(time_vec, [time_now + timedelta(hours=i*24/199)])

for en in range(len(ephimeris)):
    for i in range(time_vec.size):
        s_pos[en] = np.vstack((s_pos[en], satPos(ephimeris[en], time_vec[i])))
        satPos_vec = np.array(s_pos[en][i,:])[0]
        enu = sat2enu(satPos_vec, userPos_vec)
        ae_data[en] = np.vstack((ae_data[en], enu2ae(enu)))
        
#print(s_pos)

fig = plt.figure()
ax = fig.add_subplot(121, projection='3d')

for en in range(len(ephimeris)):
    # Data for a three-dimensional line
    zline = np.array(s_pos[en][:,2].T).tolist()[0]
    xline = np.array(s_pos[en][:,0].T).tolist()[0]
    yline = np.array(s_pos[en][:,1].T).tolist()[0]

    ax.plot3D(xline, yline, zline)

ax.scatter(userPos_vec[0],
           userPos_vec[0],
           userPos_vec[0],
           marker='x',
           c='red')

ax.set_xlabel('x axis')
ax.set_ylabel('y axis')
ax.set_zlabel('z axis')
ax.legend(svprn_list)

# draw sphere
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = 6.371e6 * np.cos(u)*np.sin(v)
y = 6.371e6 * np.sin(u)*np.sin(v)
z = 6.371e6 * np.cos(v)
ax.plot_surface(x, y, z, color='grey', alpha=0.25)

sky = fig.add_subplot(122, projection='polar')

fig2 = plt.figure()
elev = fig2.add_subplot(111)

for en in range(len(ephimeris)):
    
    azdata = np.array(ae_data[en][:,0].T)
    eldata = np.array((360/(2*np.pi))*ae_data[en][:,1].T)
    
    azdata = azdata.reshape(azdata.size)
    eldata = eldata.reshape(eldata.size)
    
    mask = eldata < 10.0
    
    eldata[mask] = np.nan
    azdata[mask] = np.nan
    
    sky.plot(azdata, eldata)
    elev.plot(eldata)
    
sky.set_theta_zero_location("N")
sky.set_theta_direction(-1)
sky.set_rlim(90, 0, 1)
sky.legend(svprn_list)

plt.show()