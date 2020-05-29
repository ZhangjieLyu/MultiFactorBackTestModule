# -*- coding: utf-8 -*-
"""
Created on Thu May 28 14:26:07 2020

@author: Evan
"""
from FactorGenerator import FactorGenerator
from FactorProfile import FactorProfile

class MatlabFactorGenerator(FactorGenerator):
    def __init__(self, generatorType_str, generateRequirement_dict, metirialDataSet_dict):
        super().__init__( generatorType_str, generateRequirement_dict)
        self.metirialDataSet = metirialDataSet_dict
        
    def get_factor_profile(self, factorName, incrementalFlag = 0):
        requirement_dict = generateRequirement_dict[factorName]
        functionName = requirement_dict[functionName]
        datasetNames_list = requirement_dict['dataset']
        parameters_dict = requirement_dict['parameter']
        
        parameters_dict.update({'updateFlag':incrementalFlag})
        
        dataset_dict = {aDataName:self.metirialDataSet[aDataName] for aDataName in datasetNames_list}
        
        factorProfile = FactorProfile(functionName, datasetNames_list, parameters_dict, dataset_dict)
        return(factorProfile)
    
    def get_factor(self, factorName, incrementalFlag):
        factorProfile = self.get_factor_profile(factorName, incrementalFlag)
        return((self.cal_factor(factorProfile), factorProfile))
    
     
    def cal_factor(self, factorProfile):
        functionName = factorProfile.functionName
        inputKwargs = factorProfile.get_factor_args()
        # print()
        
        
        
