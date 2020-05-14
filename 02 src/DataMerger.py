# -*- coding: utf-8 -*-
"""
Created on Thu May 14 2020

@author: Robert
"""
import pandas as pd
import numpy as np
import collections
import os

from MarketData import MarketData
from NameObj import NameObj

class DataMerger(MarketData, NameObj):
    """
    merge data of type 'MarketData' into a data frame
    """
    # static variables
    DATA_FREQUENCY = ["D","W","M","Q","S","A","X"]
    DATA_TAG = ["OHLC", "PriceAdj", "Return", "FundamentalData",\
                       "AlternativeData", "Benchmark", "ScreenReference"]
    
    # methods
    def __init__(self, *marketDatas):
        self.dataMaps = {}
        self.dataTagMaps = {}
        self.dataFrequencyMaps = {}
        self.columnsToDropMaps = {}
        self.featureFinderMaps = {}
        self.featureNameByTag = {}
        self.dataMaps_mergedByTag = {}
        for marketData in marketDatas:
            if isinstance(marketData, MarketData):
                self.dataMaps.update({marketData.objName:marketData})
                self.dataTagMaps.update({marketData.objName:marketData.dataTag})
                self.dataFrequencyMaps.update({marketData.objName:marketData.dataFrequency})
                self.featureFinderMaps.update({marketData.objName:marketData.featureFinder})
                try:
                    self.columnsToDropMaps.update({marketData.objName:marketData.columnsToDrop})
                except:
                    self.columnsToDropMaps.update({marketData.objName:[]})
                    
        print("Data set loaded success, number = {}.".format(len(self.dataMaps)))
                
    def set_objName(self, nickname):
        super(NameObj, self).__init__(nickname)
    
    def __isDataTagValid(self):
        dataTagDict = {}
        for key in self.dataTagMaps.keys():
            if self.dataTagMaps[key] in dataTagDict:
                dataTagDict[self.dataTagMaps[key]] += 1
            else:
                dataTagDict[self.dataTagMaps[key]] = 1
        if dataTagDict.get("OHLC",0) != 1:
            raise ValueError("Must define only one OHLC-tagged data")
        if dataTagDict.get("PriceAdj",0) !=1 and dataTagDict.get("Return",0) !=1:
            raise ValueError("Must define only one PriceAdj or Return-tagged data")
        if dataTagDict.get("Benchmark",0) == 0:
            raise ValueError("Must define at least one Benchmark-tagged data")
        # FIXME: fix bug, must check the data frequency for marketData with same tag is the same
        return True
    
    def reverse_dataTagMapsByTag(self, tagName):
        """reverse the dataTagMaps dict"""
        reverse_dataTagMaps = {}
        for key in self.dataTagMaps.keys():
            if self.dataTagMaps[key] in reverse_dataTagMaps:
                reverse_dataTagMaps[self.dataTagMaps[key]].append(key)
            else:
                reverse_dataTagMaps[self.dataTagMaps[key]] = [key]
        try:
            tablesWithTagNames = reverse_dataTagMaps[tagName]
        except:
            raise ValueError("tag name not in OHLC, PriceAdj, Return, FundamentalData,\
                   AlternativeData, Benchmark, ScreenReference or tag name not defined.")
        return tablesWithTagNames
    
    def drop_columnsByTag(self, tagName):
        # find tables with given tagName from dataTagMaps
        tablesWithTagNames = self.reverse_dataTagMapsByTag(tagName)
        # drop desired columns
        for name in tablesWithTagNames:
            columns2Drop = self.columnsToDropMaps[name]
            if len(columns2Drop) > 0:
                self.dataMaps[name].drop(columns = columns2Drop, inplace = True)
    
    def find_featureNamesByTag(self, tagName):
        # find tables with given tagName from dataTagMaps
        tablesWithTagNames = self.reverse_dataTagMapsByTag(tagName)
        # update feature names
        featureNames = set([])
        for name in tablesWithTagNames:
            featureNamesOneTable = list(self.dataMaps[name].columns)
            featuresForCrossTagMerge = list(self.featureFinderMaps[name].values())
            featureNamesOneTable = set(featureNamesOneTable).difference(set(featuresForCrossTagMerge))
            featureNames = featureNames.union(featureNamesOneTable)    
        return list(featureNames)

    def merge_marketDataByTag(self, tagName, axis, *concatTableArgs):
        if self.__isDataTagValid():
            # get tables names of tables with given tagName
            tablesWithTagName = self.reverse_dataTagMapsByTag(tagName)           
            # drop columns
            try:
                self.drop_columnsByTag(tagName)
            except:
                raise Warning("Abundant columns in tag {} have been dropped, cannot drop again!".format(str(tagName)))            
            # update feature names
            featureNames = self.find_featureNamesByTag(tagName)
            self.featureNameByTag.update({tagName:featureNames})                  
            # for data of same tagName, merge by axis
            # merge step by step
            nameCacheQueue = []
            for name in tablesWithTagName:
                if len(nameCacheQueue) == 0:
                    nameCacheQueue.append(name)
                    dataFrame = self.dataMaps[name]
                elif len(nameCacheQueue) < 2:
                    nameCacheQueue.append(name)
                if len(nameCacheQueue) == 2:
                    rightName = nameCacheQueue[-1]
                    dataFrame = pd.concat([dataFrame, self.dataMaps[rightName]],
                                          axis = axis, concatTableArgs)
                    nameCacheQueue.pop(0)
                if len(nameCacheQueue) > 2:
                    raise ValueError("name cache queue shouldn't be longer than 2, mannual check required!")
                  
            self.dataMaps_mergedByTag.update({tagName:dataFrame})
            return True
    
    
    def merge_marketDataCrossTag(self):
        pass
    
