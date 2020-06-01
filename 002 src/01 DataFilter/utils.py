# -*- coding: utf-8 -*-
"""
Created on Wed May 27 2020

@author: Robert
"""
from collections import OrderedDict
from TimeSeriesTrailingGenerator import TrailingTimeSeries
from CrossSectionTrailingGenerator import TrailingCrossSection
import numpy as np
import h5py
from tqdm import tqdm

def extract_data_from_matlabFile(targetFilePath, relativeSearchPath, 
                                 isTranspose = False):
    """
    Parameter
    -------------------------
    targetFilePath: str, pointing to file path
    relativeSearchPath: list[str], relative fields position in MATLAB
    isTranspose: is or not transpose the matrix to meet given format,
    maybe D x N, maybe N x D
    
    Return
    -------------------------
    orderedDict = {last string in relative search path : matrix}
    """
    aDict = OrderedDict()
    matlabFile = h5py.File(targetFilePath)
    
    # retrieve data from matlab file according to the relative serach path
    for relativePath in tqdm(relativeSearchPath):
        keyName = relativePath.split(".")[-1]
        
        # retrieve data from corresponding position
        data = matlabFile
        for e in relativePath.split("."):
            data = data.get(e)
        
        # isTranspose
        if isTranspose:
            data = np.array(data).T
        else:
            data = np.array(data)
        
        # update dict
        aDict.update({keyName:data})
        
    return aDict


class Under_Threshold_CumulativeTradableRule(TrailingTimeSeries):
    """
    used to do some cumulation based filter, e.g.
    must be tradable for the last 100 trading days 
    in order to be selected into the stock universe
    """
    def __init__(self, df, startPos, endPos, trailingSize, cumulationThreshold):
        super().__init__(df, startPos, endPos, trailingSize)
        self.cumulationThreshold = cumulationThreshold
    
    def compute_trailing_slice(self, trailingSlice):
        """
        imaging have the following dataframe:
            
        index | col1  | col2  | ...|
        n     | value1| value2|
        n+1   | value3| value5|
        n+2   | value4| value6|
        """
        return np.sum(trailingSlice.values[:-1,:],axis = 0)\
            <=self.cumulationThreshold


class Over_Threshold_CumulativeTradableRule(TrailingTimeSeries):
    """
    used to do some cumulation based filter, e.g.
    must be tradable for the last 100 trading days 
    in order to be selected into the stock universe
    """
    def __init__(self, df, startPos, endPos, trailingSize, cumulationThreshold):
        super().__init__(df, startPos, endPos, trailingSize)
        self.cumulationThreshold = cumulationThreshold
    
    def compute_trailing_slice(self, trailingSlice):
        """
        imaging have the following dataframe:
            
        index | col1  | col2  | ...|
        n     | value1| value2|
        n+1   | value3| value5|
        n+2   | value4| value6|
        """
        return np.sum(trailingSlice.values[:-1,:],axis = 0)\
            >=self.cumulationThreshold


class Under_Threshold_CrossSectionalQuantile(TrailingCrossSection):
    """
    used to filter stocks in a given quantile
    """
    def __init__(self, df, startPos, endPos, trailingSize, quantileThreshold):
        super().__init__(df, startPos, endPos, trailingSize)
        self.quantileThreshold = quantileThreshold
        
    def compute_trailing_slice(self, trailingSlice):
        """
        imaging have the following dataframe:
            
        index | col1  | col2  | ...|
        n     | value1| value2|
        n+1   | value3| value5|
        n+2   | value4| value6|
        """
        return trailingSlice.values[-2,:]<=np.nanquantile(trailingSlice.values[-2,:],
                                                       self.quantileThreshold)


class Over_Threshold_CrossSectionalQuantile(TrailingCrossSection):
    """
    used to filter stocks in a given quantile
    """
    def __init__(self, df, startPos, endPos, trailingSize, quantileThreshold):
        super().__init__(df, startPos, endPos, trailingSize)
        self.quantileThreshold = quantileThreshold
        
    def compute_trailing_slice(self, trailingSlice):
        """
        imaging have the following dataframe:
            
        index | col1  | col2  | ...|
        n     | value1| value2|
        n+1   | value3| value5|
        n+2   | value4| value6|
        """
        return trailingSlice.values[-2,:]>=np.nanquantile(trailingSlice.values[-2,:],
                                                       self.quantileThreshold)

