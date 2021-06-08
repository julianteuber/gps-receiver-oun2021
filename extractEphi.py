# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 11:46:03 2021

@author: julian
"""

def extractEphi(rinexData, from_datetime, to_datetime, svprn_list):
    """extract ephemerides from rinex-data

    Parameters:
        rinexData        (DataFrame): rinex data
    Returns:
        ephi_extract (list of dicts): ephemerides data
      
    """
    
    ephimerie_columns = ['svprn',
                         'cic','cis','crc','crs','cuc','cus',
                         'deltan','ecc','i0','idot','M0',
                         'omega','Omega0','Omegadot','roota','toe']
    
    ephi_extract = rinexData[(rinexData['datetime'] > from_datetime) & (rinexData['datetime'] < to_datetime)]
    ephi_extract = ephi_extract.sort_values(by = 'datetime', axis = 'index')
    ephi_extract = ephi_extract.drop_duplicates(subset = 'svprn', keep = 'first', ignore_index = True)
    ephi_extract = ephi_extract[ephi_extract['svprn'].isin(svprn_list)]
    ephi_extract = ephi_extract[ephimerie_columns]
    
    return ephi_extract.sort_values(by = 'svprn', axis = 'index').reset_index().to_dict('records')