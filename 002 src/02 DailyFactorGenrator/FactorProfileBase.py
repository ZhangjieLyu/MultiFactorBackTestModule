# -*- coding: utf-8 -*-
"""
Created on Thu May 28 14:18:05 2020

@author: Evan
"""
from abc import ABC, abstractmethod
class FactorProfileBase:
    def __init__(self, functionName, datasetName_list, parameters_dict):
        self.functionName = functionName
        self.datasetName = datasetName_list
        self.dataset = None
        self.parameters = parameters_dict
        
        self.dataset = self.get_data_set()
        
        
    @abstractmethod        
    def get_data_set(self):
        pass
        
    def get_factor_kwargs(self):
        out = dict()
        out.update(self.dataset)
        out.update(self.parameters)
        return(out)
        