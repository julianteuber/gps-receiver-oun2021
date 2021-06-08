# -*- coding: utf-8 -*-
"""
Created on Tue May 25 20:49:19 2021

@author: Julian Teuber
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from readRinex import readRinex
from extractEphi import extractEphi
from satPos import satPos

rinexPath = "C:/Users/julian/Documents/Studium/ET - Master/Module/OuN/Praktikum/RinexFiles"
outputPath = "C:/Users/julian/Documents/Studium/ET - Master/Module/OuN/Praktikum/Python/sat_data"
rinexFileName = "delf1320.21n"
rinexFullPath = os.path.join(rinexPath,rinexFileName)
rnx_data = readRinex(rinexFullPath)

from_datetime = pd.to_datetime('2021-05-12 09:40:46')
to_datetime   = pd.to_datetime('2021-05-12 10:11:22')

svprn_list = [2,6,12,25,26,29,31,32]
ephimeris = extractEphi(rnx_data, from_datetime, to_datetime, svprn_list)