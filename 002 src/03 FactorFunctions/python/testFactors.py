# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 15:58:26 2020

@author: Robert
"""
import sys

# FIXME: implement with 'import module' in later development
sys.path.insert(1, "C:\\Users\\91592\\Dropbox\\WorkingSpace\\NaiveBackTestPy_ForLoop\\02 src\\01 DataFilter")
from TimeSeriesTrailingGenerator import FactorTemplate


class testSum(FactorTemplate):
    def compute_trailing_slice(self, trailingSlice, datasetNames, parameters):
        return trailingSlice['close'].values[-2,:] + trailingSlice['high'].values[-2,:]
    
    def testSum(self):
        self.set_trailing_size(2)
        return(self.run_trailing_and_get_result())      


class testMinus(FactorTemplate):
    def compute_trailing_slice(self, trailingSlice, datasetNames, parameters):
        return trailingSlice['close'].values[-2,:] - trailingSlice['high'].values[-2,:]
    
    def testMinus(self):
        self.set_trailing_size(2)
        return(self.run_trailing_and_get_result())                                                                                                
                                                                                                  
        