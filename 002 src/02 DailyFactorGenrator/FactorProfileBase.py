# -*- coding: utf-8 -*-
"""
Created on Thu May 28 14:18:05 2020

@author: Evan
"""
from abc import ABC, abstractmethod
class FactorProfileBase:
    def __init__(self, functionName, datasetNames_list, parameters_dict):
        """
        Parameter
        ----------------------------
        functionName: str
        datasetNames_list: list[str]
        parameters_dict: dict()
        """
        self.functionName = functionName
        self.datasetNames = datasetNames_list
        self.dataset = None
        self.parameters = parameters_dict
        
        self.dataset = self.get_data_set()
        
        
    @abstractmethod        
    def get_data_set(self):
        pass
        
    def get_factor_kwargs(self, verbose = 0):
        """
        Parameter
        -------------------------------
        verbose: boolean, if verbose is True, return factorName, parameters,dataset; otherwise, return return factorName, parameters
        """
        out = dict()
        out.update({'datasetNames':self.datasetNames})
        out.update({'parameters':self.parameters})
        
        if verbose == 0:
            return(out)
        elif verbose == 1:
            out.update({'dataset':self.dataset})
            return(out)
        else:
            raise ValueError('verbose can only be 0 or 1.')
        
