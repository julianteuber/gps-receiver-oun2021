# -*- coding: utf-8 -*-
"""
Created on Tue May 25 20:49:19 2021

@author: Julian Teuber
"""

import math

def dec2dez(b60_deg, b60_min, b60_sec):
    """Convert base-60/sexagesimal representative to single degree value

    Parameters:
        b60_deg   (int): Base-60 degrees
        b60_min   (int): Base-60 minutes
        b60_sec (float): Base-60 seconds
    Returns:
                  (int): Angle in degrees
      
    """
    
    return b60_deg + b60_min / 60 + b60_sec / 3600

def dez2dec(deg):
    """Convert single degree value to base-60/sexagesimal representative
    
    Parameters:
        deg      (int): Angle in degrees
    Returns:
        b60_deg  (int): Base-60 degrees
        b60_min  (int): Base-60 minutes
        b60_dsec (int): Base-60 seconds

   """
   
    b60_deg = int(deg)
    b60_min = int((deg * 60) % 60)
    b60_sec = (deg * 3600) % 60
    
    return b60_deg, b60_min, b60_sec

def str2dec():
    """Convert base-60/sexagesimal representative to single degree value

    52°08'35.7764"N 7°19'16.6976"E
    |  |  |  |
    |  |  |  l-> Nachkommastellen Sekunde
    |  |  l----> Sekunde
    |  l-------> Minute
    l----------> Grad
    """

    return -1

def dec2str():
    """Convert base-60/sexagesimal representative to single degree value

    52°08'35.7764"N 7°19'16.6976"E
    |  |  |  |
    |  |  |  l-> Nachkommastellen Sekunde
    |  |  l----> Sekunde
    |  l-------> Minute
    l----------> Grad
    """

    return -1

def pvroc(lat):
    """Compute prime-vertical radius of curvature (Querkrümmungshalbmesser)
    
    Parameters:
        lat  (float): The geodetic latitude
    Returns:
        N    (float): The prime-vertical radius of curvature

   """
   
    a = 6378137                    # earth equatorial radius / semi-major axis
    #b = 6356752                    # earth polar radius / semi-minor axis
    #e = math.sqrt(1 - b**2 / a**2) # earth eccentricity
    f = 1/298.257223563             # earth flattening
    e = math.sqrt(2*f-f**2)         # earth eccentricity
    
    N = a / math.sqrt(1 - (e * (math.sin(math.radians(lat))))**2)
    return N

# 
def cart2geo(x, y, z, height_epsilon):
    """Cartesian to geodetic coordinate transformation
    
    Parameters:
        x              (float): Cartesian coordinate
        y              (float): Cartesian coordinate
        z              (float): Cartesian coordinate
        height_epsilon (float): The eccentricity
    Returns:
        lon            (float): The geodetic longitude
        lat            (float): The geodetic latitude
        height         (float): The geodetic height

   """
   
    lat = 0.0
    height = 0.0
    height_prev = 0.0
    height_delta = height_epsilon + 1
    
    #a = 6378137                    # earth equatorial radius / semi-major axis
    #b = 6356752                    # earth polar radius / semi-minor axis
    #e = math.sqrt(1 - b**2 / a**2) # earth eccentricity
    f = 1/298.257223563             # earth flattening
    e = math.sqrt(2*f-f**2)         # earth eccentricity

    p = math.sqrt(x**2  + y**2)
    lon = math.degrees(math.atan(y/x)) % 360
    
    # iterate until change in height gets smaller than height_epsilon
    while height_delta > height_epsilon:
        N = pvroc(math.degrees(lat))
        height_prev = height
        height = p / math.cos(lat) - N
        lat = math.atan(z/(p*(1-e**2 * N/(N + height)))) # latitude in radians
        height_delta = abs(height_prev - height)
    
    lat = math.degrees(lat) % 360
    
    return lon, lat, height

def geo2cart(lon, lat, height):
    """Geodetic to cartesian coordinate transformation
    
    Parameters:
        lon    (int): The geodetic longitude
        lat    (int): The geodetic latitude
        height (int): The geodetic height
    Returns:
        x      (int): Cartesian coordinate
        y      (int): Cartesian coordinate
        z      (int): Cartesian coordinate

   """
    
    #a = 6378137                    # earth equatorial radius / semi-major axis
    #b = 6356752                    # earth polar radius / semi-minor axis
    #e = math.sqrt(1 - b**2 / a**2) # earth eccentricity
    f = 1/298.257223563             # earth flattening
    e = math.sqrt(2*f-f**2)         # earth eccentricity

    N = pvroc(lat)

    x = (N + height) * math.cos(math.radians(lat)) * math.cos(math.radians(lon))
    y = (N + height) * math.cos(math.radians(lat)) * math.sin(math.radians(lon))
    z = ((1 - e**2) * N + height) * math.sin(math.radians(lat))
    
    return x, y, z