# -*- coding: utf-8 -*-
"""
Created on Thu May 28 14:26:07 2020

@author: Evan
"""
from FactorGenerator import FactorGenerator
from FactorProfile import FactorProfile

class MatlabFactorGenerator(FactorGenerator):
    def __init__(self, generatorType_str, generateRequirement_dict):
        super().__init__( generatorType_str, generateRequirement_dict)
        # self.metirialDataSet = metirialDataSet_dict
        
    def get_factor_profile(self, factorName, incrementalFlag = 0):
        '''
        in this version we use incrementalFlag to determine the time mode to use
        we construct the FactorProfile with a flag in it

        Parameters
        ----------
        factorName : TYPE
            which factor to get.
        incrementalFlag : TYPE, optional
           whether we get the last factor given the raw data.

        Returns
        -------
        None.

        '''
        requirement_dict = generateRequirement_dict[factorName]
        functionName = requirement_dict[functionName]
        datasetNames_list = requirement_dict['dataset']
        parameters_dict = requirement_dict['parameter']
        parameters_dict.update({'updateFlag':incrementalFlag})
        
        # dataset_dict = {aDataName:self.metirialDataSet[aDataName] for aDataName in datasetNames_list}
        
        factorProfile = FactorProfile(functionName, datasetNames_list, parameters_dict)
        return(factorProfile)
    
    def get_factor(self, factorName, incrementalFlag = 0):
        '''
        

        Parameters
        ----------
        factorName : TYPE
            which factor to get.
        incrementalFlag : bool
            whether we get the last factor given the raw data.

        Returns
        -------
        tuple(self.cal_factor(factorProfile), factorProfile).

        '''
        factorProfile = self.get_factor_profile(factorName, incrementalFlag)
        return((self.cal_factor(factorProfile), factorProfile))
    
     
    def cal_factor(self, factorProfile):
        '''
        use the matlab engine to calculate the factor
        because we load the data in the matlab engine, we do not pass the raw data into the engine
        instead we use the data in the workspace in the matlab engine
        thats why we do not need the dataset_dict in this version, we just pass the datasetNames_list

        Parameters
        ----------
        factorProfile : FactorProfile
           

        Returns
        -------
        factor numpy matrix or dataframe.

        '''
        functionName = factorProfile.functionName
        inputKwargs = factorProfile.get_factor_args()
        # print()
        
        
        
