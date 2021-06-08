# -*- coding: utf-8 -*-
"""
Created on Tue May 25 20:49:19 2021

@author: Julian Teuber
"""

import os
from readRinex import readRinex

rinexPath = "C:/Users/julian/Documents/Studium/ET - Master/Module/OuN/Praktikum/RinexFiles"
rinexFileName = "delf1310.21n"
rinexFullPath = os.path.join(rinexPath,rinexFileName)
rnx_data = readRinex(rinexFullPath)
print(rnx_data)