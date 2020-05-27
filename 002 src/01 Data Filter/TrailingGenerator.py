# -*- coding: utf-8 -*-
"""
Created on Wed May 27 2020

@author: Robert
"""
from abc import ABC, abstractmethod

class TrailingGenerator(ABC):
    """
    Trailing generator is used for constructing Filters,
    In multi-factor model, there're generally 3 types of 
    numerical result - Factor, Filter, Classifier. 
    Filter can be time-series-based or cross-sectional-based,
    But, one common thing is Filter often works on a trailing slice 
    of data.
    
    From Filter, the return type is boolean. 
    Multiple Filters can be compounded.
    
    Though the purpose of trailingGenerator is to calculate 
    a Filter, but actually, Factor and Classifier can also be 
    computed on a trailing basis.
    """
    @abstractmethod
    def set_rangeOfData(self, startPos, endPos):
        pass
    
    @abstractmethod
    def get_trailingSlice(self, pos, trailingSize):
        pass
    
    @abstractmethod
    def isValid_trailingSlice(self, pos, trailingSize):
        pass
    
    @abstractmethod
    def run_trailingTS_slice(self, pos, trailingSize):
        pass
    
    @abstractmethod
    def run_trailingCS_slice(self, pos, trailingSize):
        pass
    
    @abstractmethod
    def run_trailing(self):
        """
        trailing cross-section vs. time-series may take in different
        trailingSize.
        """
        pass
    
