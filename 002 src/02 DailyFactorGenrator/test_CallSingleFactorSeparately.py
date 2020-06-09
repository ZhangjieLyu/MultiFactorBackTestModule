# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9  2020

@author: Robert
"""
import sys
sys.path.insert(1, '..\\01 DataFilter\\') # TODO: modify this
from utils import extract_data_from_matlabFile
from PythonFactorGenerator import PythonFactorGenerator

class MyFactor(PythonFactorGenerator):
    def __init__(self,
                 generatorType_str, 
                 generateRequirement_dict, 
                 startPos=0, 
                 endPos=None,
                 currPos = None):
        super().__init__(generatorType_str, 
                 generateRequirement_dict, 
                 startPos, 
                 endPos,
                 currPos)
        
    def compute_factor1(self, trailingSlice, dataset, parameter):
        return trailingSlice[dataset[0]].values[-2,:] +\
            trailingSlice[dataset[1]].values[-2,:]
        
    def compute_factor2(self, trailingSlice, dataset, parameter):
        return trailingSlice[dataset[0]].values[-2,:] -\
            trailingSlice[dataset[1]].values[-2,:]
            
        
            
if __name__ == '__main__':

    testDataPath = ".\\projectData\\projectData.mat" #FIXME: change to your own path
    searchPath = ["projectData.stock.properties.close",
                "projectData.stock.properties.high",
                "projectData.stock.properties.low"]
    sampleData = extract_data_from_matlabFile(testDataPath, 
                                              searchPath,
                                              True)
    
    
        
    generatorType_str = 'Python'
    generateRequirement_dict = {"factor1":{
                                    'factorName':'factor1', 
                                    'dataset': ['close','high'],
                                    'parameter': [5,10]
                                    },
                                "factor2":{
                                    'factorName':'factor2', 
                                    'dataset': ['close','high'],
                                    'parameter': [5,10]
                                    }} # actually, paramter makes no sense in this example
    startPos=3
    endPos=5
            
    mf = MyFactor(generatorType_str, 
                generateRequirement_dict,
                startPos,
                endPos)
    mf.set_TRAILING_SIZE(1)
    
    # will not do computation here
    mf.produce_factor('factor1')
    mf.produce_factor('factor2')
    
    # do computation here
    print(mf.calculate_a_factor('factor1',sampleData))
    print(mf.calculate_a_factor('factor2',sampleData))


