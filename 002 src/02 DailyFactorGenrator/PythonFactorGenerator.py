# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 21:36:56 2020

@author: Robert
"""
import numpy as np
import pandas as pd
from FactorGenerator import FactorGenerator
from collections import OrderedDict

try:
    import alphalens as al
except Exception as error:
    print(error)
    Warning("not install alphalens, graphic related feature not appliable!")
    
class PythonFactorGenerator(FactorGenerator):
    """
    Parameter
    -------------------------------------------
     __init__(self, generatorType_str, generateRequirement_dict, 
                 startPos=0, endPos=None,
                 incrementalFlag = 0)
    -------------------------------------------
    a Pythonic template for calculating factors, support 3 types of input:
        1. trailing slice
        2. incremental input
        3. a matrix (NOT REALIZED, wait for further discussion)
        (warning:
            order of execution, incrementalFlag > matrixFlag > startPos,endPos)
    
    The purpose of this class is to offer a template so that factors can be 
    calculated easily from giving just expression.
    
    Use a method "compute_XXXX(self)" (XXXX is the factorName) to store a 
    specific calculation method of XXXX.
    
    Don't need to specify "compute_XXXX" inside PythonFactorGenerator.
    
    Note: if factorName is duplicated, the later one will be preserved
    automatically, i.e. any previous ones will be overwritten.
    """
    def __init__(self, generatorType_str, generateRequirement_dict, 
                 startPos=0, endPos=None,
                 incrementalFlag = 0):
        super().__init__(generatorType_str, generateRequirement_dict)
        
        
        # if incremental flat is inited, not use other methods
        if incrementalFlag:
            self.generationMode = "incremental"
            print("Factor generation mode: incremental mode.\n")
            return
        
        # init startPos and endPos
        if startPos < endPos:
            self.generationMode = "read_data_byDefault"
            self.startPos = startPos
            self.endPos = endPos
            print("Factor generation mode: slicing using start position and\
                  end position.\n")
        else:
            raise ValueError("if slicing, start posistion must be \
                             smaller than end posistion")
        
        
    def get_factor_input(self, factorName):
        """
        register factor's required data field and parameters
        a dict(generateRequirement_dict) which originally records all information of factors
        is like:
            
            requirement_dict -- factorName_1 == factorName_1(facto name again)
                            |                ||== dataset(field names)
                            |                ||== parameter(a dict)
                            |-- factorName_2
        """
        pass
    
    def produce_factor(self):
        """
        This method will find all functions satisfy the given signature rule.
        i.e. search all methods like "compute_XXXX" and "XXXX" is a registered
        factor name by register_all_factor_input(self):void, which is an extension of 
        get_factor_input(self, factorName).
        
        Don't need to call register_all_factor_input explicitly, this method is
        called automatically when calling produce_factor
        
        If encountering unknown factorName, will raise warning
        
        Note: this method will not call any computation!!
        """
        pass
    
    def calculate_a_factor(self, factorName):
        """
        perform calculation, return bool
        """
        pass
    
    def calculate_all_factors(self):
        """
        perform calculation, return bool
        """
        pass
    
    def get_factor(self, factorName):
        """
        return the matrix of given factorName,
        raise error if not found
        """
        pass
    
    def get_all_factors(self):
        """
        extension of get_factor,return OrderedDict(factorName: matrix)
        """
        pass
    
    def __clean_data_to_plot(self):
        """
        a method only for plotting
        """
        pass
    
    def plot_asset_return_vs_factor_loading(self, groupingNumber = 5):
        pass
    
    
    def get_all_factor_history(self):
        raise NotImplementedError("cannot implement this method is PythonFactorGenerator")
        
    def get_factor_increment(self):
        raise NotImplementedError("cannot implement this method is PythonFactorGenerator")
        
    def get_all_factor_increment(self):
        raise NotImplementedError("cannot implement this method is PythonFactorGenerator")
        
    def get_factor_history(self):
        raise NotImplementedError("cannot implement this method is PythonFactorGenerator")