# -*- coding: utf-8 -*-
"""
Created on Thu May 28 13:54:28 2020

@author: Evan
"""
from abc import ABC, abstractmethod


class FactorGenerator(ABC):
    def __init__(self, generatorType_str, generateRequirement_dict):
        self.generatorType =generatorType
        self.generateRequirement = generateRequirement_dict
        
    @abstractmethod  
    def get_factor_profile(self, factorName):
        '''
        construct the factor profile according to the factor name and the counterpart message in the generateRequirement
        for each profile, prepare all the informatoin needed
        Parameters
        ----------
        factorName : str
            determine the factor name to construct profile
        Returns
        -------
        FactorProfile.

        '''
        pass
    
    @abstractmethod  
    def cal_factor(self, factorProfile):
        '''
        use the information in the profile to calculate the factor,(include the start calculate date etc.)
        call the function or class that actually defines the algo to calculate
        ideally the funcion above should be called using the factorProfile.functionName
        and return the factor data 

        Parameters
        ----------
        factorProfile : FactorProfile
            the recipe to cal culate factor
            including the time mode, the needed dataset name(datasets if needed), the para ect.

        Returns
        -------
        numpy matrix or pd.DataFrame.

        '''
        pass
    
    @abstractmethod
    def get_factor(self, factorName):
        '''
        call the self.get_factor_profile and self.cal_factor to return a nice 
        tuple with the calculated factor data with its profile
        make adjustment if needed (determine the startdate, endDate , currentFlag ect.)
        for example
        in matlab version I override the method as following 
        def get_factor(self, factorName, incrementalFlag):

        Parameters
        ----------
        factorName : str
            determine the factor name to construct profile

        Returns
        -------
        return((self.cal_factor(factorProfile), factorProfile))

        '''
        pass
    
    
    def get_factor_current(self, factorName):
        '''
        get the current factor with its factor name
        for good user interface
        plz override the method if your get_factor method has different way to use  
        

        Parameters
        ----------
        factorName : str
           determine the factor name to construct profile

        Returns
        -------
        return((self.cal_factor(factorProfile), factorProfile)).

        '''
        return(self.get_factor(factorName, 1))
        
    def get_factor_history(self, factorName):
         '''
        get the history factor with its factor name
        for good user interface
        plz override the method if your get_factor method has different way to use  

        Parameters
        ----------
        factorName : str
            determine the factor name to construct profile

        Returns
        -------
        return((self.cal_factor(factorProfile), factorProfile)).

        '''
        return(self.get_factor(factorName, 0))
    
    def get_all_factor_current(self):
        '''
        iter through all the factor names in the generateRequirement
        and calculate the current factor data

        Returns
        -------
        dict.

        '''
        return({aFactorName:self.get_factor_increment(aFactorName) for aFactorName in self.generateRequirement.keys()})
    
    def get_all_factor_history(self):
        '''
        iter through all the factor names in the generateRequirement
        and calculate the history factor data

        Returns
        -------
        dict.

        '''
        return({aFactorName:self.get_factor_history(aFactorName) for aFactorName in self.generateRequirement.keys()})
        
          
    
