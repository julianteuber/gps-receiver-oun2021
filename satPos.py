# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 11:46:03 2021

@author: julian
"""

import math
import numpy as np
from datetime import datetime, timezone
from astropy.time import Time, TimeGPS

from coordTrans import dec2dez, dez2dec, geo2cart, cart2geo

def uwr(x):
    (x + 2*np.pi) % (2*np.pi)
    return x

def satPos(ephi_dict, t_eval):
    """calculate the 3d satelite position for time t_eval based on the given ephimeris

    Parameters:
        ephi_dict (dict): ephimeris data
        t_eval    (datetime): evaluation time
    Returns:
        x_k      (float): Cartesian coordinate
        y_k      (float): Cartesian coordinate
        z_k      (float): Cartesian coordinate

    """
    
    c_rs       = ephi_dict['crs']
    delta_n   = ephi_dict['deltan']
    M_0       = ephi_dict['M0']
    c_uc       = ephi_dict['cuc']
    ecc       = ephi_dict['ecc']
    c_us       = ephi_dict['cus']
    roota     = ephi_dict['roota']
    t_oe      = ephi_dict['toe']
    Omega0    = ephi_dict['Omega0']
    c_is       = ephi_dict['cis']
    i0        = ephi_dict['i0']
    c_rc       = ephi_dict['crc']
    c_ic       = ephi_dict['cic']
    omega     = ephi_dict['omega']
    Omega_dot = ephi_dict['Omegadot']
    i_dot      = ephi_dict['idot']
    #codes     = ephi_dict['codes']
    #weekno    = ephi_dict['weekno']
    #L2flag    = ephi_dict['L2flag']
    #svaccur   = ephi_dict['svaccur']
    #svhealth  = ephi_dict['svhealth']
    #tgd       = ephi_dict['tgd']
    #iodc      = ephi_dict['iodc']
    #tom       = ephi_dict['tom']
    #datetime  = ephi_dict['datetime']
    
    mu = 3.986005e14              # WGS 84 value of the earth's gravitational constant for GPS user
    Omega_e_dot = 7.2921151467e-5 # WGS 84 value of the earth's rotation rate
    
    a = roota**2                             # Semi-major axis
    n0 = math.sqrt(mu/(a**3))                # Computed mean motion (rad/sec)
        
    tgps_sec = Time(t_eval).gps % 604800
    t_k = tgps_sec - t_oe                # Time from ephemeris reference epoch
    
    # Account for beginning or end of week crossovers
    if t_k > 302400:
        t_k = t_k - 604800
    elif t_k < -302400:
        t_k = t_k + 604800
        
    n = n0 + delta_n                  # Corrected mean motion
    M_k = M_0 + n * t_k               # Mean anomaly
    M_k = (M_k + 2*np.pi) % (2*np.pi)
    
    # Kepler's Equation for Eccentric Anomaly (may be solved by iteration) (radians)
    E_k = M_k                         # First guess for E_k
    M_k_delta = 1                     # difference between two iterations
    
    #print('----------------------------')
    #print('t_k        = %d' % t_k)
    #print('M_k        = %12.6f' % M_k)
    for i in range(6):
        M_k_temp = E_k + ecc*math.sin(E_k)
        M_k_delta = M_k - M_k_temp
    #    print('i = %d, M_k_temp = %12.6f, M_k_delta = %3.3e' % (i, M_k_temp, M_k_delta))
        E_k = E_k + M_k_delta
        if abs(M_k_delta) < 1e-12:
            break
    
    E_k = (E_k + 2*np.pi) % (2*np.pi)
    
    # True Anomaly
    sinv_k = math.sqrt(1 - ecc**2)*math.sin(E_k) #/ (1 - ecc*math.cos(E_k))
    cosv_k = (math.cos(E_k) - ecc) #/ (1 - ecc*math.cos(E_k))
    v_k = math.atan2(sinv_k, cosv_k)
    
    #E_k = math.acos((ecc+cosv_k)/(1+ecc*cosv_k)) # Eccentric Anomaly
    
    Phi_k = (v_k + omega) % (2*np.pi)                             # Argument of Latitude
    
    # Second Harmonic Perturbations
    delta_u_k = c_us * math.sin(2*Phi_k) + c_uc * math.cos(2*Phi_k) # Argument of Latitude Correction
    delta_r_k = c_rs * math.sin(2*Phi_k) + c_rc * math.cos(2*Phi_k) # Radius Correction
    delta_i_k = c_is * math.sin(2*Phi_k) + c_ic * math.cos(2*Phi_k) # Inclination Correction
    
    u_k = Phi_k + delta_u_k                   # Corrected Argument of Latitude
    r_k = a*(1-ecc*math.cos(E_k)) + delta_r_k # Corrected Radius
    i_k = i0 + delta_i_k + i_dot * t_k        # Corrected Inclination
    
    # Positions in orbital plane
    x_k_dash = r_k * math.cos(u_k)
    y_k_dash = r_k * math.sin(u_k)
    
    # Corrected longitude of ascending node
    Omega_k = Omega0 + (Omega_dot - Omega_e_dot) * t_k - Omega_e_dot * t_oe
    Omega_k = uwr(Omega_k)
    
    # Earth-fixed coordinates
    x_k = x_k_dash * math.cos(Omega_k) - y_k_dash * math.cos(i_k) * math.sin(Omega_k)
    y_k = x_k_dash * math.sin(Omega_k) + y_k_dash * math.cos(i_k) * math.cos(Omega_k)
    z_k = y_k_dash * math.sin(i_k)
    
    return np.array([x_k, y_k, z_k])

def sat2enu(satPos_vec, userPos_vec):
    """

    Parameters:
        
    Returns:
        

    """
    
    lon, lat, height = cart2geo(userPos_vec[0], userPos_vec[1], userPos_vec[2], 10e-3)
    lon = np.radians(lon)
    lat = np.radians(lat)
    
    rotation_mat = np.matrix([[-np.sin(lon),              np.cos(lon),             0          ],
                              [-np.sin(lat)*np.cos(lon), -np.sin(lat)*np.sin(lon), np.cos(lat)],
                              [ np.cos(lat)*np.cos(lon),  np.cos(lat)*np.sin(lon), np.sin(lat)]])
    
    locPos_vec = np.array(rotation_mat * np.matrix(satPos_vec - userPos_vec).T).reshape((3,))
    
    return locPos_vec

def enu2ae(locPos_vec):
    """

    Parameters:
        
    Returns:
        

    """
    
    azimuth = np.arctan2(locPos_vec[0],locPos_vec[1])
    elevation = np.arcsin(locPos_vec[2]/np.linalg.norm(locPos_vec))
    
    return azimuth, elevation