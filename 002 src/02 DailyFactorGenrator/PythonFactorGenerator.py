# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 21:36:56 2020

@author: Robert
"""
import numpy as np
import pandas as pd
from FactorGenerator import FactorGenerator
from collections import OrderedDict
import types

import sys
sys.path.insert(1, '..\\01 DataFilter\\') # TODO: modify this
try:
    from TimeSeriesTrailingGenerator import TrailingMultipleTimeSeriesCustomized
except ImportError:
    raise ImportError('cannot import TrailingTimeSeries, plz \
                      add position to search directory, see line 13')

try:
    import alphalens as al
except ImportError:
    Warning("not install alphalens, graphic related feature not appliable!")
    
    
class PythonFactorGenerator(FactorGenerator, TrailingMultipleTimeSeriesCustomized):
    """
    Use a method "compute_XXXX(self)" (XXXX is the factorName) to store a 
    specific calculation method of XXXX.
    
    Don't need to specify "compute_XXXX" inside PythonFactorGenerator.
    
    Behavior when having duplicated factorName:
        1. if call calculate_a_factor(factorName), preserve the first one
        2. if call cal
    """
    def __init__(self,
                 generatorType_str, 
                 generateRequirement_dict, 
                 startPos=0, 
                 endPos=None,
                 currPos = None):
        super().__init__(generatorType_str, generateRequirement_dict)
        
        # set length of data prior to startPos to reduce the nan in the begining of slicing
        # self.__PRIOR_START_POS_LENGTH = 10
        # self.__real_startPos_of_slice = 0
        self.__FIX_TRAILING_SIZE = 20
    
        # init empty FILO queue
        self.factorName_queue = [];
        self.dataset_queue = [];
        self.parameter_queue = [];
        self.computationMethod_queue = [];
        
        # MODE 1: if current position inited, only calculate the exact day.
        # computation methods depend on methods whose signature is 
        # compute_XXXX
        if isinstance(currPos, int):
            self.generationMode = "incremental"
            self.currPos = currPos
            
            print("Factor generation mode: incremental mode.\n")
            return
        
        # MODE2: init startPos and endPos
        if startPos < endPos:
            self.generationMode = "history"
            self.startPos = startPos
            self.endPos = endPos
            print("Factor generation mode: history mode.\n")
        else:
            raise ValueError("USE valid value of (startPos, endPos) pair or \
                             USE valid value of currPos! Valid value must be\
                                 in range of index!")
                                 
                                
    # def set_PRIOR_START_POS_LENGTH(self, newPriorLength):
    #     """
    #     To reduce nan in the beginnig of trailing slicing calculation
    #     and to avoid nan in calculation using current position, one must assign
    #     a pre-defined length of data set prior to start position of slice or 
    #     current position, however, nan is still inevitable when there is no 
    #     enough length of data prior to the start position.
    #     """
    #     self.__PRIOR_START_POS_LENGTH = newPriorLength
    #     self.cal_real_startPos_of_slice()
    #     print('re-calulate real start position successfully.')
        
    def set_TRAILING_SIZE(self, trailingSize):
        self.__FIX_TRAILING_SIZE = trailingSize
        print('set trailing size to be {}.'.format(str(trailingSize)))
    
    # def cal_real_startPos_of_slice(self):
    #     """
    #     a method that will adjust real start slicing length in both 'currPos'
    #     and '(startPos, endPos)' modes.
        
    #     Note:
    #         1. this method is covered in "set_PRIOR_START_POS_LENGTH"
    #     """
    #     # get all attributes
    #     allAttributes = \
    #         [i for i in self.__dict__.keys() if i[:1] != '_']
    #     # if initialization with startPos and endPos
    #     if 'currPos' in allAttributes:
    #         if self.currPos - self.__PRIOR_START_POS_LENGTH < 0:
    #             self.__real_startPos_of_slice = 0
    #         else:
    #             self.__real_startPos_of_slice =\
    #                 self.currPos - self.__PRIOR_START_POS_LENGTH 
    #     else:
    #         if self.startPos - self.__PRIOR_START_POS_LENGTH < 0:
    #             self.__real_startPos_of_slice = 0
    #         else:
    #             self.__real_startPos_of_slice =\
    #                 self.startPos - self.__PRIOR_START_POS_LENGTH 
        
        
    def get_factor_input(self, factorName):
        """
        register factor's required data field and parameters
        a dict(generateRequirement_dict) which originally records all information of factors
        is like:            
            requirement_dict -- factorName_1 == factorName(factor name again)
                            |                ||== dataset(field names)
                            |                ||== parameter(a dict)
                            |-- factorName_2
        """
        return self.generateRequirement.get(factorName, 'Not Found.')

        
    def register_a_factor_input(self, factorName):
        """
        When calling register_a_factor_input(self, factorName), you actually push
        the dataset&parameter into a FILO queue, like following:
            dataset_queue      | parameter_queue    | computationMethod_queue
            [dataset_factorN]   [parameter_factorN]  [compute_factorN]
            ...                  ...                   ...
            [dataset_factor1]   [parameter_factor1]  [compute_factor1]
            
        Returns
        -------
        None.
        
        WARNING: don't use this method, cause error in logic
        """
        if self.get_factor_input(factorName) == 'Not Found.':
            raise KeyError('{}: registration of dataset/parameter failed, \
                           no such parameters declared!'.format(factorName))
        else:
            inputStructure = self.get_factor_input(factorName)
            self.factorName_queue.append(inputStructure['factorName']) #FIXME: maybe need fix, depend on how the structure look like
            self.dataset_queue.append(inputStructure['dataset'])
            self.parameter_queue.append(inputStructure['parameter'])

        
    def produce_factor(self, factorName, methodName=None):
        """
        By calling produce_factor(self, factorName), you actually try to
        register the compute_factorName(self, dataset, parameter) into a queue.
    
        Note: 
            1. this method will not execute any computation!!
            2. this method covers register_a_factor_input(self, factorName)!
        """
        flag = 0 # indicate whether method name pushed into queue successfully
        self.register_a_factor_input(factorName)    
        if methodName:
            if methodName in dir(self):
                self.computationMethod_queue.append(methodName)
                flag = 1
        else:
            if 'compute_'+factorName in dir(self):
                self.computationMethod_queue.append('compute_'+factorName)
                flag = 1
        if flag == 0:
            raise AttributeError('No compute_{} method or {} method defined!'.format(factorName, methodName))
    
    def calculate_a_factor(self, factorName, df_dict = OrderedDict()): #FIXME: current still use df, substitue with singleton instance later
        """
        execute calculation
        """
        try:
            idx = self.factorName_queue.index(factorName)
        except:
            raise ValueError('{} is not registered!'.format(factorName))
        datasetIdx = self.dataset_queue[idx]
        parameterIdx = self.parameter_queue[idx]
        methodCallIdx = self.computationMethod_queue[idx]
        
        if self.generationMode == 'incremental':
            super(FactorGenerator,self).__init__(df_dict, self.currPos, self.currPos, self.__FIX_TRAILING_SIZE)
        else:
            super(FactorGenerator,self).__init__(df_dict, self.startPos, self.endPos, self.__FIX_TRAILING_SIZE)
        self.set_computation_method(methodCallIdx, datasetIdx, parameterIdx)
        return self.run_trailing_and_get_result()
    
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
    
    @classmethod
    def __addMethod(cls, func):
        return setattr(cls, func.__name__, types.MethodType(func, cls))
    
    def get_all_factor_history(self):
        raise NotImplementedError("cannot implement this method is PythonFactorGenerator")
        
    def get_factor_increment(self):
        raise NotImplementedError("cannot implement this method is PythonFactorGenerator")
        
    def get_all_factor_increment(self):
        raise NotImplementedError("cannot implement this method is PythonFactorGenerator")
        
    def get_factor_history(self):
        raise NotImplementedError("cannot implement this method is PythonFactorGenerator")