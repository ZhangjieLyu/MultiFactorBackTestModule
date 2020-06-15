# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 21:36:56 2020

@author: Robert
"""
import sys
from FactorGenerator import FactorGenerator
from FactorProfile import FactorProfile
from collections import OrderedDict
import os

YOUR_PATH = "..\\projectData\\projectData.mat"

# FIXME: import module instead of .py file later
# The following codes assuming the working directory is '02 DailyFactorGenerator'
sys.path.insert(1,"..\\01 DataFilter")
from utils import extract_data_from_matlabFile
    
class PythonFactorGenerator(FactorGenerator):
    """
    This class is only responsible for calculating factor, only calculating!
    
    The way of calculating a factor and the function used to calculate a factor
    is not defined in this class!!
    
    Parameters
    ----------
    generatorType_str: str, 'matlab' or 'python', temporarily just an indicator.
    
    generateRequirement_dict: dict(), a dict of factor set-ups, organized like
    {factorName(str):{"functionName":str,
                      "parameters":dict(),
                      "datasetNames":list[str]}}.
    
    startPos: int, start posistion
    
    endPos: int, end position
    
    currPos: int, current posistion, not compatible with usage of (startPos, endPos) pair.
    
    
    Notes:
    ------
        1. when having duplicated function names in different modules:
            will execute the function that first encountered
        2. only specify factor_expression_search_path but didn't give module names or
        give incorrect module names:
            cannot point to correct function, may result in failure of 
            loading modules
    """
    def __init__(self,
                 generatorType_str, 
                 generateRequirement_dict, 
                 startPos=None, 
                 endPos=None,
                 currPos = None):
        
        super().__init__(generatorType_str, generateRequirement_dict)
        self.factorExpressionSearchPath = []
        self.moduleNames = []
        self.generatedFactorDict = OrderedDict()
        
        # MODE 1: if current position inited, only calculate the exact day.
        if isinstance(currPos, int):
            self.generationMode = 0 # use current position
            self.currPos = currPos
            print("Factor generation mode: incremental mode.\n")
            return
        
        # MODE2: init startPos and endPos
        if isinstance(startPos, int) and isinstance(endPos, int) and (startPos < endPos):
            self.generationMode = 1 # use start position - end posistion
            self.startPos = startPos
            self.endPos = endPos
            print("Factor generation mode: history mode.\n")
        else:
            raise ValueError("use valid value of (startPos, endPos) pair or \
                             use valid value of currPos!")
    
    # ========static variables, use to point to data loading method===========
    @staticmethod
    def get_data():
        Warning("only a test method to test that the programme is executable!")    
        testDataPath = YOUR_PATH
        searchPath = ["projectData.stock.properties.close",
                      "projectData.stock.properties.high"]   
        sampleData = extract_data_from_matlabFile(testDataPath, 
                                                  searchPath,
                                                  True)
        print('\n test data loaded successfully.')
        return(sampleData)
    
    sampleData = get_data.__func__()  
    #======= modify above static function in later development ================
                
    def set_factor_expression_search_path(self, filePath, moduleNames_list):
        """
        set folder to which filex of factor expressions are stored

        Parameters
        ----------
        filePath : str
            a file path pointed to a folder, the file structure is:
                filePath - module1
                         - module2
                         ...
                         - moduleN

        Returns
        -------
        None

        """
        if os.path.exists(filePath):
            self.factorExpressionSearchPath = filePath
            self.moduleNames = moduleNames_list
            print('set factor expression path: {}'.format(self.factorExpressionSearchPath))
        else:
            raise FileExistsError('Cannot found {}'.format(filePath))
                       
            
    def get_factor_profile(self, factorName):
        """
        wrap dict into FactorProfile structure
        
        Parameters
        ----------
        factorName: str
        """
        factorSetUps = self.generateRequirement.get(factorName, 'Not Found.')
        if factorSetUps == 'Not Found.':
            print(factorSetUps)
            return
        else:
            factorProfile = FactorProfile(factorName,
                                          factorSetUps.get('functionName'),
                                          factorSetUps.get('datasetNames'),
                                          factorSetUps.get('parameters'),
                                          None)
            return(factorProfile)


    def cal_factor(self, factorProfile, verbose = 1):
        """
        will call functionName defined in factorProfile, and run the function.
        self.generationMode will be pass back to specified factor expression(i.e.
        factorProfile.functionName) to determine if using (start~end) or current
        position

        Parameters
        ----------
        factorProfile: FactorProfile.FactorProfile
            the attribute 'dataset' can be empty
            
        verbose: boolean

        Returns
        -------
        boolean

        """
        if len(self.factorExpressionSearchPath) > 0:
            sys.path.insert(1, self.factorExpressionSearchPath)
            moduleLoaded = []
            successFlag = 0
            
            # load data set
            # FIXME: modify the proccess of getting data set in the following lines
            # in later development
            dataset = OrderedDict({name: PythonFactorGenerator.sampleData[name] for 
                                   name in factorProfile.datasetNames if
                                   name in PythonFactorGenerator.sampleData})
            if len(list(dataset.keys())) != len(factorProfile.datasetNames):
                print("factor {} loaded data incomplete!".format(factorProfile.factorName))
            
            # import factor expression from given module
            for aModule in self.moduleNames:
                try:
                    importStr = "from {} import *".format(aModule)
                    exec(importStr)
                    moduleLoaded.append(aModule)
                except:
                    print('fail to import module {}'.format(aModule))
                    continue
            
            # call functionName in factorPorfile
            for aModule in moduleLoaded:
                try:
                    # search module by module, if found, break loop
                    if self.generationMode == 1:
                        generatedFactor = getattr(__import__(aModule), factorProfile.functionName)(dataset,
                                                                                                   factorProfile.functionName,
                                                                                                   factorProfile.parameters,
                                                                                                   startPos = self.startPos,
                                                                                                   endPos = self.endPos)
                        self.generatedFactorDict[factorProfile.factorName] = getattr(generatedFactor, factorProfile.functionName)()
                        successFlag = 1
                        break
                    elif self.generationMode == 0:
                        generatedFactor = getattr(eval(factorProfile.functionName), factorProfile.functionName)(dataset,
                                                                                                                factorProfile.functionName,
                                                                                                                factorProfile.parameters,
                                                                                                                currPos = self.currPos)
                        self.generatedFactorDict[factorProfile.factorName] = getattr(generatedFactor, factorProfile.functionName)()
                        successFlag = 1
                        break
                    else:
                        raise ValueError('self.generationMode can only be 0(use currPos) or 1(use startPos-endPos pair)')
                except:
                    continue
            
            if verbose == 1:
                # if verbose = True, print detailed information
                if successFlag == 1:
                    print('{} generated successfully via {}.{}'.format(factorProfile.factorName,
                                                                       aModule,
                                                                       factorProfile.functionName))
                else:
                    print('fail to generated {}'.format(factorProfile.factorName))
                    
            return(successFlag)
        
        else:
            raise AttributeError('must set_factor_expression_search_path first')


    def get_factor(self, factorName, verbose = 1):
        '''
        call the self.get_factor_profile and self.cal_factor to return a nice 
        tuple with the calculated factor data with its profile
        make adjustment if needed (determine the startdate, endDate , currentFlag ect.)

        Parameters
        ----------
        factorName : str
            determine the factor name to construct profile
        verbose: boolean
            The default is 1

        Returns
        -------
        return((self.cal_factor(factorProfile), factorProfile))

        '''       
        factorProfile = self.get_factor_profile(factorName)
        successFlag = self.cal_factor(factorProfile, verbose)
        
        if successFlag == 1:
            return((self.generatedFactorDict[factorProfile.factorName], factorProfile))
        else:
            return((None, factorProfile))
        
        
    def cal_all_factors(self, verbose = 1):
        '''
        wrapped method of cal_factor(factorProfile, verbose), if this method is called,
        will calculate all factors declared in generateRequirement_dict.
        Whenever call this method, will clear all previous calculation result

        Parameters
        ----------
        verbose : boolean, optional
            print details or not. The default is 1(print details).

        Returns
        -------
        logDict = {factorName: successFlag}.
        
        '''
        # clear previous calculation results
        self.generatedFactorDict = OrderedDict()
        
        # write logs
        logDict = OrderedDict()
        for aFactorName in self.generateRequirement.keys():
            aFactorProfile = self.get_factor_profile(aFactorName)
            aSuccessFlag = self.cal_factor(aFactorProfile, verbose)
            logDict.update({aFactorName:aSuccessFlag})
        return(logDict)
    
    
    def get_all_factors(self, verbose = 1):
        """
        wrapped methods of get_factor(factorName, verbose), if this method is called,
        will calculated all factors declared in generateRequirement_dicts and return
        a nice tuple of (generatedFactorDict, logDict)
        Whenever call this method, will clear all previous calculation result

        Parameters
        ----------
        verbose : boolean, optional
            print details or not. The default is 1.

        Returns
        -------
        Tuple (generatedFactorDict, logDict)

        """
        logDict = self.cal_all_factors(verbose)
        return((self.generatedFactorDict, logDict))
    
    
    def get_factor_current(self, factorName, currPos, verbose = 1):
        """
        This method allows to redefine generate type regardless of what was inited.
        
        Parameters
        ----------
        factorName : str
            factor name registed
        currPos : int
        verbose: boolean
            The default is 1.(print in details)

        Returns
        -------
        Tuple (generatedFactorDict, factorProfile)

        """
        self.generationMode = 0 # means use current posistion
        self.currPos = currPos # set current position
        self.get_factor(factorName, verbose)
        
        
    def get_all_factors_current(self, currPos, verbose = 1):
        """
        This method allows to redefine generate type regardless of what was inited.
        WARNING: once this method is called, all previous calculation results will
        be cleared!

        Parameters
        ----------
        currPos : int
        verbose : bool, optional
            The default is 1.

        Returns
        -------
        Tuple (generatedFactorDict, logDict)

        """
        self.generationMode = 0 #means use current position
        self.currPos = currPos # set current position
        self.get_all_factors(verbose)
        
    def get_factor_history(self, factorName, startPos, endPos, verbose = 1):
        """
        This method allows to redefine generate type regardless of what was inited.

        Parameters
        ----------
        factorName : str
        startPos : int
        endPos : int
        verbose : bool, optional. The default is 1.

        Returns
        -------
        Tuple (generatedFactorDict, factorProfile)

        """
        self.generationMode = 1 # means use history mode
        self.startPos = startPos
        self.endPos = endPos
        self.get_factor(factorName, verbose)
        
        
    def get_all_factors_history(self, startPos, endPos, verbose = 1):
        """
        This method allows to redefine generate type regardless of what was inited.
        WARNING: once this method is called, all previous calculation results will
        be cleared!

        Parameters
        ----------
        startPos : int
        endPos : int
        verbose : bool, optional. The default is 1.

        Returns
        -------
        None.

        """
        self.generationMode = 1 # means use history mode
        self.startPos = startPos
        self.endPos = endPos
        self.get_all_factors(verbose)
        
        
    def get_all_factor_current(self):
        raise NotImplementedError('deprecated, use get_all_factors_current instead!')
        
    def get_all_factor_history(self):
        raise NotImplementedError('deprecated, use get_all_factors_history instead!')
