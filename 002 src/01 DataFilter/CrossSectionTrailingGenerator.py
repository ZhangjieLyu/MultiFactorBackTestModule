# -*- coding: utf-8 -*-
"""
Created on Wed May 27  2020

@author: Robert
"""
from TrailingGenerator import TrailingGenerator
import pandas as pd
import numpy as np

class TrailingCrossSection(TrailingGenerator):
    """
    Init Parameter
    ----------------------
     df, startPos, endPos, trailingSize = 2
    ----------------------
    Trailing time series, in a matrix of days * stocks, call method will:
        1. init with startPos, endPos, a 2d DataFrame, and an absolute index
        2. iterate starting from startPos, return NaN if no enough trailingSize
        for a given pos
        3. during each iteration, give a computation function
        4. in each iteration, the return will be a row of numeric value
        5. in defining trailingSize, define trailingSize = n indicates:
            
            pos-n
            ...
            pos-1
            pos <- suppose you're here, don't know pos-th information
            
            i.e. compute pos-th day information based on 
            past n days information(exclude pos-th day)
            
        WARNING: "pos" as index, is an absolute index to make
        data prior to/after slicing consistent
    """
    def __init__(self, df, startPos, endPos, trailingSize = 2):
        self.startPos = startPos
        self.endPos = endPos
        
        if trailingSize > 2:
            raise ValueError("cross-sectional trailing window can only be 1 or 2")
        else:
            self.trailingSize = trailingSize
        
        # check if input is a dataframe
        if isinstance(df, pd.DataFrame):
            self.rawData = df
        else:
            self.rawData = pd.DataFrame(data = df)
    
    def set_range_of_data(self):
        self.data = self.rawData.loc[self.startPos: self.endPos]
        self.trailingResult = 0*np.ones(self.data.shape)
    
    def get_trailing_result(self):
        return self.trailingResult
    
    def is_valid_trailing_slice(self, pos, trailingSize):
        if pos-trailingSize<0:
            return False
        else:
            return True
    
    def get_trailing_slice(self, pos, trailingSize):
        if self.is_valid_trailing_slice(pos, trailingSize):
            trailingSlice = self.rawData.loc[pos-trailingSize:pos]
            return trailingSlice
        else:
            return []
    
    def compute_trailing_slice(self, trailingSlice):
        return np.ones((1,trailingSlice.shape[1]))
        
    def run_trailingTS_slice(self, pos, trailingSize):
        raise NotImplementedError("Cannot use trailing time-series computation\
                                  in a cross-sectional-trailing-type class.")
        
    def run_trailingCS_slice(self, pos, trailingSize):
        trailingSlice = self.get_trailing_slice(pos, trailingSize)
        if len(trailingSlice)>0:
            return self.compute_trailing_slice(trailingSlice)
        else:
            return np.nan

    def run_trailing(self):
        self.set_range_of_data()
        offset = list(self.data.index)[0]
        for pos in self.data.index:
            self.trailingResult[pos-offset,:] = \
                self.run_trailingCS_slice(pos, self.trailingSize)
                
    def run_trailing_and_get_result(self):
        self.run_trailing()
        return self.get_trailing_result()
    
    def description(self):
        print("startPos: {}".format(str(self.startPos)))
        print("endPos: {}".format(str(self.endPos)))
        print("trailingSize: {}".format(str(self.trailingSize)))


