# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 10:42:42 2021

@author: julian
"""

from os.path import join as ospj
import scipy.io as sio
import matplotlib.pyplot as plt
from acquisition import rsmp
import numpy as np
import numpy.fft as npfft

pathname = 'C:/Users/julian/Documents/Studium/ET - Master/Module/OuN/Praktikum/matFiles'
prncode_fname = 'GPSL1_LUT.mat'
prnonly_fname = 'prnOnly.mat'

satPrnNum = 1

prncode_mat = sio.loadmat(ospj(pathname,prncode_fname))
prnonly_mat = sio.loadmat(ospj(pathname,prnonly_fname))

caCodes = prncode_mat['caCodesLUT']
signal = prnonly_mat['sigCode'].reshape(prnonly_mat['sigCode'].size)

code = rsmp(caCodes[0,:],1.023e6,1.63676e7)

signal_corr = np.correlate(signal,code,'full')
num_corr = signal_corr.size
time_corr = np.linspace(0,num_corr / 1.63676e7,num_corr)

var = np.var(signal_corr)
var3 = var*3

#code_fft = npfft.fft(code)
#code_rsmp_fft = npfft.fft(code)

plt.plot(time_corr, signal_corr)
plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
plt.show()