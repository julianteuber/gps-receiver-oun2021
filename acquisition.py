# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 10:48:57 2021

@author: julian
"""

import numpy as np

def rsmp(inpt,fsIn,fsOut):
    
    # Verhältnis aus Wunsch-Sample-Rate und Ist-Sample-Rate
    ratio = fsOut/fsIn
    
    # Floor Funktion zur Bestimmung der Anzahl der Ausgangs-Samples
    n = int(inpt.size*ratio)
    nbr = np.arange(n)
    
    # Transformieren der Sample-Nummern
    tmp = (nbr/ratio).astype(int)
    #tmp = tmp + 1;
    tmp[tmp>inpt.size] = inpt.size
    
    # Umschreiben des Index-Starts von 0 auf 1
    inpt = inpt.reshape((inpt.size))
    out = inpt[tmp.tolist()]
    
    return out