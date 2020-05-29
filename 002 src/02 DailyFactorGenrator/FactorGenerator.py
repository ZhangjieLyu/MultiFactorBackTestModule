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
    def get_factor_input(self, factorName, incrementalFlag = 0):
        pass
    
    @abstractmethod  
    def produce_factor(self, factorInput):
        pass
    
    @abstractmethod
    def get_factor(self, factorName, incrementalFlag):
        pass
    
    def get_factor_increment(self, factorName):
        return(self.get_factor(factorName, 1))
        
    def get_factor_history(self, factorName):
        return(self.get_factor(factorName, 0))
    
    def get_all_factor_increment(self):
        return({aFactorName:self.get_factor_increment(aFactorName) for aFactorName in self.generateRequirement.keys()})
    
    def get_all_factor_history(self):
        return({aFactorName:self.get_factor_history(aFactorName) for aFactorName in self.generateRequirement.keys()})
        
          
    
