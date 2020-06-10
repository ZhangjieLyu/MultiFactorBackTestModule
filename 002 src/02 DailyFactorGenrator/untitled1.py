# -*- coding: utf-8 -*-
"""
Created on Thu May 28 12:50:52 2020

@author: Evan
"""
PROJROOT = 'C:\\Users\\Evan\\MyFile\\Python\\MultiFactorBackTestModule'

import sys, os, pickle
sys.path.append(PROJROOT)
sys.path.append(os.path.join(os.path.join(PROJROOT, "002 src"), "01 Data Filter"))
sys.path.append(os.path.join(PROJROOT, "001 data"))
print(sys.path)
#%%
from utils import extract_data_from_matlabFile

import numpy as np
import matlab.engine
#%% read pickle
with open(os.path.join(os.path.join(PROJROOT, "001 data"),'sampleData_0528.p'), 'rb') as fp:
    data = pickle.load(fp)
    
print(data.keys())
#%% 

engine = matlab.engine.start_matlab()
baseFolderPath = "C:\\Users\\Evan\MyFile\\Python\\MultiFactorBackTestModule\\002 src\\03 FactorFunctions\\matlab"

engine.workspace

allMatLabPath = engine.genpath(baseFolderPath)
engine.addpath(allMatLabPath)
engine.alpha053(data['close'])
engine.double(data['close'])
close = data['close']
img = np.random.rand(87, 195, 126)
imgMatlab = matlab.double(img)

close.shape



engine.load()
