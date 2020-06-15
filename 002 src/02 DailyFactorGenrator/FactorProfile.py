# -*- coding: utf-8 -*-
"""
Created on Thu May 28 15:11:11 2020

@author: Evan
@reviewer: Robert
"""
from FactorProfileBase import FactorProfileBase

class FactorProfile(FactorProfileBase):
    def __init__(self, factorName, functionName, datasetNames_list, parameters_dict, dataset_dict):
        
        super().__init__(factorName, functionName, datasetNames_list, parameters_dict)
        self.dataset = dataset_dict
            
    def get_data_set(self):
        if self.dataset:
            return(self.dataset)
        
#%%  
# TODO: delete after test
if __name__ == "__main__":
    factorName = "toyFactor"
    functionName = "test"
    datasetNames_list = list()
    parameters_dict = dict()
    dataset = dict()
    Klass = FactorProfile(factorName, functionName, datasetNames_list, parameters_dict, dataset)
    
    print(Klass.get_factor_kwargs(verbose = 0))
    print(Klass.get_factor_kwargs(verbose = 1))
    
