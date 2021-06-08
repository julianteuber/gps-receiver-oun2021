# -*- coding: utf-8 -*-
"""
Created on Tue May 25 20:49:19 2021

@author: Julian Teuber
"""

import pandas as pd

def readRinex(ephemerisfile):
    """read ephemerides from rinex-file with name 'ephemerisfile'

    Parameters:
        ephemerisfile (string): name of regex data path
    Returns:
                            (): ephemerides structure
      
    """
    
    # öffnen der Datei
    fid = open(ephemerisfile, 'r')
    
    # überspringen des Headers
    head_lines = 0
    while True:
        head_lines = head_lines + 1
        line = fid.readline().rstrip()
        #answer = findstr(line,'END OF HEADER')
        #if ~isempty(answer):
        #    break
        #answer = line.find("END OF HEADER")
        if "END OF HEADER" in line:
            break
   
    # anzahl der vorhandenen Ephemeriden
    noeph = 0
    #while True:
    #   noeph = noeph +1
    #   line = fid.readline().rstrip()
    #   if line == -1:
    #       break
    for line in fid:
        noeph += 1
           
    noeph = int(noeph / 8)
    
    # zurückstellen des File-Pointers
    fid.seek(0)
    
    for i in range(1,head_lines+1):
        line = fid.readline().rstrip()
    
    rinexData = pd.DataFrame(columns = ('svprn','year','month','day','hour','minute','second','af0','af1','af2','IODE','crs','deltan','M0','cuc','ecc','cus','roota','toe','cic','Omega0','cis','i0','crc','omega','Omegadot','idot','codes','weekno','L2flag','svaccur','svhealth','tgd','iodc','tom'))
    
    # Einlesen der Navigationsdaten nach dem RINEX-2.10 Format
    for i in range(0,noeph-1):
        
        line = fid.readline().rstrip()
        svprn    = line[0:3]       # Satellite PRN number
        year     = line[3:7]       # Toc - Time of Clock year
        month    = line[7:9]       # Toc - Time of Clock month
        day      = line[9:12]      # Toc - Time of Clock day
        hour     = line[12:15]     # Toc - Time of Clock hour
        minute   = line[15:18]     # Toc - Time of Clock minute
        second   = line[18:22]     # Toc - Time of Clock second
        af0      = line[22:41]     # SV clock bias         (seconds)
        af1      = line[41:60]     # SV clock drift        (sec/sec)
        af2      = line[60:79]     # SV clock drift rate   (sec/sec2)
   
        line = fid.readline().rstrip()
        IODE     = line[3:22]      # IODE Issue of Data, Ephemeris
        crs      = line[22:41]     # Crs                   (meters)
        deltan   = line[41:60]     # Delta n               (radians/sec)
        M0       = line[60:79]     # M0                    (radians)
        
        line = fid.readline().rstrip()
        cuc      = line[3:22]      # Cuc                   (radians)
        ecc      = line[22:41]     # e Eccentricity
        cus      = line[41:60]     # Cus                   (radians)
        roota    = line[60:79]     # sqrt(A)               (sqrt(m))
   
        line = fid.readline().rstrip()
        toe      = line[3:22]      # Toe Time of Ephemeris (sec of GPS week)
        cic      = line[22:41]     # Cic                   (radians)
        Omega0   = line[41:60]     # OMEGA                 (radians)
        cis      = line[60:79]     # CIS                   (radians)
   
        line = fid.readline().rstrip()
        i0       =  line[3:22]     # i0                    (radians)
        crc      = line[22:41]     # Crc                   (meters)
        omega    = line[41:60]     # omega                 (radians)
        Omegadot = line[60:79]     # OMEGA DOT             (radians/sec)
   
        line = fid.readline().rstrip()
        #idot, codes, weekno, L2flag = line.split()
        idot     = line[3:22]      # IDOT                  (radians/sec)
        codes    = line[22:41]     # Codes on L2 channel
        weekno   = line[41:60]     # GPS Week # (to go with TOE), Continuous number, not mod(1024)!
        L2flag   = line[60:79]     # L2 P data flag
   
        line = fid.readline().rstrip()
        #svaccur, svhealth, tgd, iodc = line.split()
        svaccur  = line[3:22]      # SV accuracy           (meters)
        svhealth = line[22:41]     # SV health             (bits 17-22 w 3 sf 1)
        tgd      = line[41:60]     # TGD                   (seconds)
        iodc     = line[60:79]     # IODC Issue of Data, Clock
   
        line = fid.readline().rstrip()
        #tom, _, _, _ = line.split()
        tom      = line[3:22]      # Transmission time of message (sec of GPS week, derived e.g. from Z-count in Hand Over Word (HOW)
        #_ = line[22:41]           # Fit interval          (hours) (see ICD-GPS-200, 20.3.4.4)
                                   # Zero if not known
        #_ = line[41:60]           # spare
        #_ = line[60:79]           # spare
        
        # Jahr von zwei auf vier Ziffern erweitern
        if 59 <= int(year) <= 99:
            year = '19' + year
        else:
            year = '20' + year
            
        rinexData.loc[i] = svprn, year, month, day, hour, minute, second, af0, af1, af2, IODE, crs, deltan, M0, cuc, ecc, cus, roota, toe, cic, Omega0, cis, i0, crc, omega, Omegadot, idot, codes, weekno, L2flag, svaccur, svhealth, tgd, iodc, tom
        
    fid.close()
    
    # Konvertieren des scientific-formats
    for column in rinexData:
        rinexData[column] = rinexData[column].apply(lambda x: x.replace("D", "E"))
    
    # Konvertieren des Datentyps von String nach Numerisch
    rinexData = rinexData.apply(pd.to_numeric, errors='coerce')
    
    # Parsen der Datetime-Spalte aus den Zeitspalten
    rinexData['datetime'] = pd.to_datetime(rinexData[['year','month','day','hour','minute','second']])
    
    return rinexData