# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 19:31:24 2020

@author: Robert
"""
from collections import OrderedDict
import numpy as np
import sys
import os

class TimeRollingModel(object):
    """
    The job of TimeRollingModel is: fetch SPECIFIED data as X, get SPECIFIED
    data as Y, SPECIFY a window size, then pass (Y_window,X_window,parameters) 
    tuple to SPECIFIED models, after getting result, pass the result to right 
    posistion, compare the predicted Y vs. real Y and return some evaluation 
    metric.
    
    This job divide TimeRollingModel as several parts, they're:
        1. set-up parameters:
            
            1.0. specify the window size for each rolling
            
            1.1. to correctly specify X, should clarify following params: where
            to find X( X should be a variable in RAM), specify how X_window
            look like in a given window(i.e. how to get X_window for model in a
            given rolling loop, X_window is a subset of X_aRollingLoop)
            
            1.2. to correctly specify Y, should clarify following params: where
            to find Y( Y should be a variable in RAM), specify how Y_window
            look like in a given window(i.e. how to get Y_window for model in a
            given rolling loop, Y_window is a subset of Y_aRollingLoop)
            
            1.3. a ordered dict of {modelNickName:params} 
        
        2. call models with params inited in 'set-up parameters'
        
        3. fetch result from models and return it to correct position
        
        4. evaluate the model according to user-defined evaluation function
            
            
    """
    def __init__(self):
        """
        Generate a null constructor

        Returns
        -------
        None.

        """
        self.model_dict = OrderedDict() # string modelName: dict params
        self.modelClassFolderPath = [] # list[str] point to folders storing models, use sys.path.append to add
        self.rollingWindowSize = np.nan # should be an integer when giving value
        self.XRule = OrderedDict() #should be string label: list [], where inner list = [startPos -midPos ,midPos, endPos - midPos]
        self.YRule = OrderedDict() #should be the same length of generateXRule
        self.evaluationMetric_dict = OrderedDict() # string metricName: string evaluationFuncName
        self.evaluationFunctionFolderPath = str() # empty string pointer
    
    # ===========part 1: set-up params ====================
    
    # ----------set rolling window size--------------------
    def set_rolling_window_size(self, rollingWindowSize):
        if isinstance(rollingWindowSize ,int) and rollingWindowSize > 0:
            self.rollingWindowSize = rollingWindowSize
        else:
            raise ValueError('window size must be positive integer')
    
    
    def reset_rolling_window_size(self, newRollingWindowSize = None):
        self.rollingWindowSize = []
        self.set_rolling_window_size(newRollingWindowSize)
        
    # -----------------------------------------------------
        
    # ----------set model class folder path ---------------
    def set_model_folder(self, modelClassFolderPath):
        flag = 1
        for path in modelClassFolderPath:
            if not os.path.exists(path):
                flag = 0
                break
        
        if flag == 1:
            self.modelClassFolderPath = modelClassFolderPath
        else:
            Warning('set failed, {} is not an existing path'.format(path))
            
    
    def add_a_model_folder(self, aModelClassFolderPath):
        flag = 1
        if not os.path.exists(aModelClassFolderPath):
            flag = 0
            
        if flag == 1:
            self.modelClassFolderPath.append(aModelClassFolderPath)
        else:
            Warning('add failed, {} is not an existing path'.format(aModelClassFolderPath))


    def add_a_list_of_model_folders(self, aListOfModelClassFolderPath):
        for path in aListOfModelClassFolderPath:
            self.add_a_model_folder(path)
            
    def remove_a_model_folder(self, aModelClassFolderPath, force = False):
        if force == False:
            if len(self.model_dict)>0:
                Warning('CANNOT REMOVE: already set model_dict, may lose some \
                        information if remove path now, use force = True to \
                            override this warning.')
                return
            
        try:
            self.modelClassFolderPath.remove(aModelClassFolderPath)
        except ValueError:
            print('cannot remove, because no such path in existing modelClassFolderPath')
            
            
    def remove_a_list_of_model_folder(self, aListOfModelClassFolderPath, force = False):
        for path in aListOfModelClassFolderPath:
            self.remove_a_model_folder(path, force)
            
    
    def reset_model_folder(self, newModelClassFolderPath = None):
        self.modelClassFolderPath = []
        
        if newModelClassFolderPath != None:
            self.set_model_folder(newModelClassFolderPath)
            
    # ------------------------------------------------------
                
    # ---------------set model dict-------------------------
    # model dict: {'Ridge':params}, params = {'modelName': 'LinearModel.Ridge','lambda':1}
    # or maybe {'AdaBoost':params}, params = {'modelName': 'TreeModel.BoostingTree.AdaBoost','leaf_node_depth':10}
    def try_load_model_from_model_folder_path(self, modelName, path, modelNickname):
        # init a success flag
        flag = 0
        # add path to sys
        sys.path.append(path)
        importString = 'import '+modelName+' as '+modelNickname
        # try to execute the import command
        try:
            exec(importString)
            return flag
        except ImportError:
            flag = 1
            sys.path.remove(path)
            Warning('model with name {} :: import failed'.format(modelName)) 
            return flag


    def try_load_model_from_a_list_of_model_folder_path(self, modelName, aListOfPath, modelNickname):
        for path in aListOfPath:
            flag = self.try_load_model_from_model_folder_path(modelName, path, modelNickname)
            if flag == 1:
                print('model with name {} :: import success, import from path {}'.format(modelName,path))
                break
        
        if flag == 0:
            Warning('model with name {} :: load failed'.format(modelName))
            return flag
        return flag
    
    
    def set_model_dict(self, model_dict, verbose = False):
        nicknameAndModelName_dict = {key:model_dict[key].get('modelName') for key in model_dict.keys()}
        modelClassFolderPath = self.modelClassFolderPath
        loadedModels = set([])
        
        if len(modelClassFolderPath) == 0:
            raise AttributeError('must assign pointer pointing to directory \
                                 storing model first, can use set_model_path')
        
        for aNickname in nicknameAndModelName_dict.keys():
            if nicknameAndModelName_dict[aNickname].get('modelName') == None:
                Warning("CANNOT ADD: the model with nickname {} has no modeName,\
                        must assign one through params['modelName']".format(aNickname))
                continue
            flag = self.try_load_model_from_a_list_of_model_folder_path(nicknameAndModelName_dict[aNickname].get('modelName'),
                                                                        modelClassFolderPath,
                                                                        aNickname)
            if flag == 1:
                loadedModels.add(nicknameAndModelName_dict[aNickname].get('modelName'))
        
        if verbose == True:
            print(loadedModels)
                
    # FIXME: add method:: 1. update_model_dict_with_a_record, 2. update_model_dict_with_a_list_of_records
            
    def reset_model_dict(self, newModel_dict = None, verbose = False):
        self.model_dict = OrderedDict()
        
        if newModel_dict != None:
            self.set_model_dict(newModel_dict, verbose)
    
    # -------------------------------------------------------
    
    # ------------set how to get X,Y in a rollin' loop-------
    def is_XRule_and_YRule_length_match(self):
        if len(self.XRule) == len(self.YRule):
            return True
        else:
            return False
        
    def from_rule_to_startPos_and_endPos(self, aRule):
        if len(aRule) == 2:
            startPos = aRule[0]
            endPos = aRule[1]
            return(startPos, endPos)
        elif len(aRule) == 3:
            refPos = aRule[1]
            startPosMinusRefPos = aRule[0]
            endPosMinusRefPos = aRule[2]
            
            startPos = refPos + startPosMinusRefPos
            endPos = refPos + endPosMinusRefPos
            
            return(startPos, endPos)
        else:
            raise AttributeError('len of rule can only be 2 or 3.')
        
    def is_a_valid_rule(self, aRule, label):
        if self.rollingWindowSize == None:
            raise ValueError('should assign self.rollingWindowSize first')
        
        try:
            startPos, endPos = self.from_rule_to_startPos_and_endPos(aRule)
            
            if startPos < endPos and startPos >= 0 and endPos < self.rollingWindowSize:
                return True
            else:
                return False
        
        except:
            Warning('rule with label {} is not a valid rule input'.format(str(label)))
            return False
            
    
    def is_a_list_of_valid_rules(self, rules, labels):
        if len(rules) != len(labels):
            raise ValueError('rules and labels should have the same length')
            
        cumFlag = 0
        for aRule, aLabel in zip(rules, labels):
            flag = self.is_a_valid_rule(aRule, aLabel)
            cumFlag += flag
            
        if cumFlag == len(rules):
            return True
        else:
            return False
        
    def set_rule(self, rules, labels = None):
        """
        set same rule for X and Y

        Parameters
        ----------
        rules : TYPE
            DESCRIPTION.
        labels : TYPE, optional
            DESCRIPTION. The default is None.

        Raises
        ------
        ValueError
            DESCRIPTION.

        Returns
        -------
        None.

        """
        if isinstance(rules, OrderedDict) or isinstance(rules, dict):
            labels = list(rules.keys())
            rules = list(rules.values())
            flag = self.is_a_list_of_valid_rules(rules, labels)
        elif len(rules) == len(labels) and labels != None:
            flag = self.is_a_list_of_valid_rules(rules, labels)
        else:
            flag = False
            
        if flag == True:
            self.XRule = rules
            self.YRule = rules
        else:
            raise ValueError('contains invalid rule input')
            
        
    # FIXME: add methods to set_X_Y_Rule(), gives X,Y different rule
    #        add methods to remove_rule
            
    # --------------------------------------------------------
            
    # --------------set evaluation method---------------------
    
    # FIXME: add evaluation methods later
            
    # --------------------------------------------------------
    
    # ========================================================
            
    # ======================part 2.3.4.=======================
    # contains a major loop controller, in every loop(i.e. in a rollin' loop)
    # should do:
    # 1. get slice for Y, X in a rollin' loop
    # 2. do some check for Y, X 
    # 3. send Y, X to models(call models with init parameters)
    # 4. get result back and put result in a correct position
    # 5. call evaluation method
            
    def slice_data_from_rule(self, data, aRule):
        pass
    
    def call_model_by_model_nickname(self, Y, X, params):
        pass
    
    def fetch_data_to_model(self, data, aRule, modelName, modelNickname):
        pass
            
        
    
        
        

