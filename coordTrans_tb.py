# -*- coding: utf-8 -*-
"""
Created on Tue May 25 20:49:19 2021

@author: Julian Teuber
"""

import numpy as np
from coordTrans import dec2dez, dez2dec, geo2cart, cart2geo

longitude = 7.0, 19.0, 16.6976
latitude = 52.0, 8.0, 35.7764
height = 75.0
precision = 1e-6

longitude_deg = dec2dez(*longitude)
latitude_deg = dec2dez(*latitude)

print("lon, lat, height = %15.6f, %15.6f, %15.6f" % (longitude_deg,latitude_deg,height))
x,y,z = geo2cart(longitude_deg,latitude_deg,height)
print("x, y, z          = %15.6f, %15.6f, %15.6f" % (x,y,z))
print("lon, lat, height = %15.6f, %15.6f, %15.6f" % cart2geo(x,y,z,precision))
print(dez2dec(longitude_deg))
print(dez2dec(latitude_deg))

longitude1 = 7.321061478744795
latitude1  = 52.14236450962284
longitude2 = 7.320353365356649
latitude2  = 52.14237952558552
x1,y1,z1   = geo2cart(longitude1,latitude1,75.5904)
x2,y2,z2   = geo2cart(longitude2,latitude2,75.5904)

v1 = np.array([x1,y1,z1])
v2 = np.array([x2,y2,z2])

print(np.linalg.norm(v2-v1))