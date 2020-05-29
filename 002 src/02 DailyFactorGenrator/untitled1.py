# -*- coding: utf-8 -*-
"""
Created on Thu May 28 12:50:52 2020

@author: Evan
"""
PROJROOT = 'C:\\Users\\Evan\\MyFile\\Python\\MultiFactorBackTestModule'

import sys, os
sys.path.append(PROJROOT)
sys.path.append(os.path.join(os.path.join(PROJROOT, "002 src"), "01 Data Filter"))
sys.path.append(os.path.join(PROJROOT, "001 data"))
print(sys.path)
#%%
from utils import extract_data_from_matlabFile
import pickle

#%% read pickle
with open(os.path.join(os.path.join(PROJROOT, "001 data"),'sampleData_0528.p'), 'rb') as fp:
    data = pickle.load(fp)
#%% 
print(data.keys())
