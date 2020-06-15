# -*- coding: utf-8 -*-
"""
Created on Wed May 27 2020

@author: Robert
"""
from TrailingGenerator import TrailingGenerator
from collections import OrderedDict
import pandas as pd
import numpy as np

class TrailingTimeSeries(TrailingGenerator):
    """
    Init Parameter
    ----------------------
     df, startPos, endPos, trailingSize
    ----------------------
    Trailing time series, in a matrix of days * stocks, call method will:
        1. init with startPos, endPos, a 2d DataFrame, and an absolute index
        2. iterate starting from startPos, return NaN if no trailingSize
        for a given pos
        3. during each iteration, give a computation function
        4. in each iteration, the return will be a row of numeric value
        5. in defining trailingSize, define trailingSize = n indicates:
            
            pos-n
            ...
            pos-1
            pos<- suppose you're here, don't know pos-th information
            
            i.e. compute pos-th day information based on 
            past n days information(exclude pos-th day)
            
        WARNING: "pos" as index, is an absolute index to make
        data prior to/after slicing consistent
    """
    def __init__(self, df, startPos, endPos, trailingSize):
        self.startPos = startPos
        self.endPos = endPos
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
        trailingSlice = self.get_trailing_slice(pos, trailingSize)
        if len(trailingSlice)>0:
            return self.compute_trailing_slice(trailingSlice)
        else:
            return np.nan
        
    def run_trailingCS_slice(self, pos, trailingSize):
        raise NotImplementedError("Cannot use trailing cross-sectional computation\
                                  in a time-series-trailing-type class.")

    def run_trailing(self):
        self.set_range_of_data()
        offset = list(self.data.index)[0]
        for pos in self.data.index:
            self.trailingResult[pos-offset,:] = \
                self.run_trailingTS_slice(pos, self.trailingSize)
    
    def run_trailing_and_get_result(self):
        self.run_trailing()
        return self.get_trailing_result()
    
    def description(self):
        print("startPos(included): {}".format(str(self.startPos)))
        print("endPos(included): {}".format(str(self.endPos)))
        print("trailingSize: {}".format(str(self.trailingSize)))
        
class TrailingMultipleTimeSeries(TrailingTimeSeries):
    """
    Enhancement of TrailingTimeSeries, allowing calculation among more than one
    data frame. Same mechanism as TrailingTimeSeries, but offer multiple table
    at the same time
    Data structure to visit multiple data frame: ordered dictionary
    
    Note:
        1. input must be either ordered dict or 3-d matrix - e.g. days x stocks x features
        2. the major usage of TrailingMultipleTimeSeries is different from TrailingTimeSeries,
        so the default value for null is nan 
    """
    def __init__(self, df_dict, startPos, endPos, trailingSize):
        self.startPos = startPos
        self.endPos = endPos
        self.trailingSize = trailingSize
        self.data = OrderedDict()
        self.rawData = OrderedDict()
        
        # check if input is a ordered dict
        if isinstance(df_dict, OrderedDict):
            for dfName in df_dict:
                if isinstance(df_dict[dfName], pd.DataFrame):
                    self.rawData[dfName] = df_dict[dfName]
                else:
                    self.rawData[dfName] = pd.DataFrame(data = df_dict[dfName])
        else:
            self.rawData = OrderedDict()
            for aDim in range(df_dict.shape[2]):
                self.rawData['df_'+str(aDim)] = \
                    pd.DataFrame(data = df_dict[:,:,aDim])
    
    def set_range_of_data(self):
        for dfName in self.rawData.keys():
            self.data[dfName] = \
                self.rawData[dfName].loc[self.startPos: self.endPos]
        self.trailingResult = np.nan*np.ones(self.data[dfName].shape)
    
    def get_trailing_slice(self, pos, trailingSize):
        trailingSlice = OrderedDict()
        if self.is_valid_trailing_slice(pos, trailingSize):
            for dfName in self.rawData.keys():
                trailingSlice[dfName] = \
                    self.rawData[dfName].loc[pos-trailingSize:pos]
            return trailingSlice
        else:
            return []
    
    def run_trailingTS_slice(self, pos, trailingSize):
        trailingSlice = self.get_trailing_slice(pos, trailingSize)
        if len(trailingSlice)>0:
            return self.compute_trailing_slice(trailingSlice)
        else:
            return np.nan
        
    def run_trailingCS_slice(self, pos, trailingSize):
        raise NotImplementedError("Cannot use trailing cross-sectional computation\
                                  in a time-series-trailing-type class.")

    def run_trailing(self):
        self.set_range_of_data()
        offset = list(self.data[list(self.data.keys())[0]].index)[0]
        for pos in self.data[list(self.data.keys())[0]].index:
            self.trailingResult[pos-offset,:] = \
                self.run_trailingTS_slice(pos, self.trailingSize)
    
    
class TrailingMultipleTimeSeriesCustomized(TrailingMultipleTimeSeries):
    """
    allow using a more free way to define compute_trailing_slice() method, 
    though the CUSTOMIZED computation methods still need a key word, 'compute',
    now, method name e.g. compute_XXXX can be used in calculation
    """
    def __init__(self, df_dict, startPos, endPos, trailingSize):
        super().__init__(df_dict, startPos, endPos, trailingSize)

    def set_computation_method(self, functionName, datasetNames, parameters):
        self.functionName = functionName
        self.datasetNames = datasetNames 
        self.parameters = parameters
    
    def run_trailingTS_slice(self, pos, trailingSize):
        trailingSlice = self.get_trailing_slice(pos, trailingSize)
        if len(trailingSlice)>0:
            return getattr(self, self.functionName)(trailingSlice, 
                                                    self.datasetNames, 
                                                    self.parameters)
        else:
            Warning('trailingSlice is empty, return nan')
            return np.nan
        

class FactorTemplate(TrailingMultipleTimeSeries):
    """
    a class speciailzed to API of cal_factor in PythonFactorGenerator class
    """
    def __init__(self, 
                 dataset = None, 
                 datasetNames = None,
                 functionName = None, 
                 parameters = None,
                 startPos = None, 
                 endPos = None, 
                 currPos = None):
        self.parameters = parameters
        self.functionName = functionName
        self.datasetNames = datasetNames
        if isinstance(startPos, int) and isinstance(endPos, int):
            super().__init__(dataset, startPos, endPos, 1)
        elif isinstance(currPos, int):
            super().__init__(dataset, currPos, currPos, 1)
        else:
            pass
    
    def set_trailing_size(self, newTrailingSize):
        self.trailingSize = newTrailingSize    
    
    def comput_trailing_slice(trailingSlice, datasetNames, parameters):
        pass
        
    def run_trailingTS_slice(self, pos, trailingSize):
        trailingSlice = self.get_trailing_slice(pos, trailingSize)
        if len(trailingSlice)>0:
            return self.compute_trailing_slice(trailingSlice, 
                                                self.datasetNames, 
                                                self.parameters)
        else:
            Warning('trailingSlice is empty, return nan')
            return np.nan