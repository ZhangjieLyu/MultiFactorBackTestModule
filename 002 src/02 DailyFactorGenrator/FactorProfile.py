# -*- coding: utf-8 -*-
"""
Created on Thu May 28 15:11:11 2020

@author: Evan
"""
from FactorProfileBase import FactorProfileBase

class FactorProfile(FactorProfileBase):
    def __init__(self, functionName, datasetNames_list, parameters_dict, dataset_dict):
        
        super().__init__(functionName, datasetNames_list, parameters_dict)
        self.dataset = dataset_dict
            
    def get_data_set(self):
        if self.dataset:
            return(self.dataset)
        
    def get_factor_args(self):
        out = dict()
        out.update(self.dataset)
        out.update(parameters)
        return(out)
        
#%%    
if __name__ == "__main__":
    functionName = "test"
    datasetName_list = list()
    parameters_dict = dict()
    dataset = dict()
    Klass = FactorProfile(functionName, datasetName_list, parameters_dict, dataset)
    
    print(Klass.get_factor_kwargs())
    
