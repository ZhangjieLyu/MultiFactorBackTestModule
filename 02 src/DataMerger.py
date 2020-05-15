# -*- coding: utf-8 -*-
"""
Created on Thu May 14 2020

@author: Robert
"""
import pandas as pd
import numpy as np
import collections
import os

from NameObj import NameObj
from MarketData import MarketData

class DataMerger(NameObj):
    """
    merge data of type 'MarketData' into a data frame
    """
    # static variables
    DATA_FREQUENCY = ["D","W","M","Q","S","A","X"]
    DATA_TAG = ["OHLC", "PriceAdj", "Return", "FundamentalData",
                "AlternativeData", "Benchmark", "ScreenReference",
                "SectorClassifier"]
    
    # methods
    def __init__(self, *marketDatas):
        self.dataMaps = {}
        self.dataTagMaps = {}
        self.dataFrequencyMaps = {}
        self.columnsToDropMaps = {}
        self.featureFinderMaps = {}
        self.featureNameByTag = {}
        self.dataMaps_mergedByTag = {}
        self.dataMaps_mergedCrossTag = {}
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
        print("Data set loaded success, number = {}.".format(str(len(self.dataMaps))))

        
    def set_objName(self, nickname):
        super(NameObj, self).__init__(nickname)
    
    
    def __isDataTagValid(self):
        dataTagDict = {}
        for key in self.dataTagMaps.keys():
            if self.dataTagMaps[key] in dataTagDict:
                dataTagDict[self.dataTagMaps[key]] += 1
            else:
                dataTagDict[self.dataTagMaps[key]] = 1
        if dataTagDict.get("OHLC",0) == 0:
            raise ValueError("Must define at least one OHLC-tagged data")
        if dataTagDict.get("PriceAdj",0) == 0 and dataTagDict.get("Return",0) == 0:
            raise ValueError("Must define at least one PriceAdj or Return-tagged data")
        if dataTagDict.get("Benchmark",0) == 0:
            raise ValueError("Must define at least one Benchmark-tagged data")
        return True
    
    
    def __isDataFrequencyValid(self, verbose = 0):
        dataFreqDictByTag = {}
        reverse_dataTagDict = self.reverse_dataTagMaps()
        for tag in reverse_dataTagDict.keys():
            for name in reverse_dataTagDict[tag]:
                if tag in dataFreqDictByTag:
                    if self.dataFrequencyMaps[name] != dataFreqDictByTag[tag]:
                        raise ValueError("data frequency must be the same for \
                                         market data of the same data tag.")
                else:
                    dataFreqDictByTag[tag] = self.dataFrequencyMaps[name]
        if verbose == 0:
            return True
        else:
            return(True, dataFreqDictByTag)
        
    def __isFeatureFinderValid(self):
        for name in self.featureFinderMaps.keys():
            if self.dataTagMaps[name] in ["OHLC", "Return", "PriceAdj", "Benchmark"]:
                if "TradingDate" not in list(self.featureFinderMaps[name].keys()):
                    raise ValueError("OHLC, Return, PriceAdj, Benchmark \
                                     must have TradeingDate:YourColumnName pair")
            if self.dataTagMaps[name] in ["FundamentalData"]:
                if "AnnouncementDate" not in list(self.featureFinderMaps[name].keys()):
                    raise ValueError("FundamentalData must have AnnouncementDate:YourColumnName pair")
            if self.dataTagMaps[name] in ["AlternativeData"]:
                if "Date" not in list(self.featureFinderMaps[name].keys()):
                    raise ValueError("AlternativeData must have Date:YourColumnName pair")
            if self.dataTagMaps[name] in ["ScreenReference"]:
                if "Date" not in list(self.featureFinderMaps[name].keys()) &\
                    "AnnouncementDate" not in list(self.featureFinderMaps[name].keys()):
                    raise ValueError("ScreenReference must have \
                                     Date/AnnouncementDate:YourColumnName pair")
        return True
                
        
    def reverse_dataTagMaps(self):
        """reverse the dataTagMaps dict"""
        reverse_dataTagMaps = {}
        for key in self.dataTagMaps.keys():
            if self.dataTagMaps[key] in reverse_dataTagMaps:
                reverse_dataTagMaps[self.dataTagMaps[key]].append(key)
            else:
                reverse_dataTagMaps[self.dataTagMaps[key]] = [key]
        return reverse_dataTagMaps
    
    def reverse_dataTagMapsByTag(self, tagName):
        reverse_dataTagMaps = self.reverse_dataTagMaps()
        try:
            tablesWithTagNames = reverse_dataTagMaps[tagName]
        except:
            raise ValueError("tag name not in OHLC, PriceAdj, Return, FundamentalData,\
                   AlternativeData, Benchmark, ScreenReference or tag name not defined.")
        return tablesWithTagNames
    
    
    def reverse_dataFreqByTableName(self):
        """reverse the name:frequency"""
        reverse_dataFreq = {}
        for name in self.dataFrequencyMaps.keys():
            if self.dataFrequencyMaps[name] in reverse_dataFreq:
                reverse_dataFreq[self.dataFrequencyMaps[name]].append(name)
            else:
                reverse_dataFreq[self.dataFrequencyMaps[name]] = [name]
        return reverse_dataFreq
                
    
    def drop_columnsByTag(self, tagName):
        # find tables with given tagName from dataTagMaps
        tablesWithTagNames = self.reverse_dataTagMapsByTag(tagName)
        # drop desired columns
        for name in tablesWithTagNames:
            columns2Drop = self.columnsToDropMaps[name]
            if len(columns2Drop) > 0:
                self.dataMaps[name].marketData.drop(columns = columns2Drop, inplace = True)
    
    
    def find_featureNamesByTag(self, tagName):
        # find tables with given tagName from dataTagMaps
        tablesWithTagNames = self.reverse_dataTagMapsByTag(tagName)
        # update feature names
        featureNames = set([])
        for name in tablesWithTagNames:
            featureNamesOneTable = list(self.dataMaps[name].marketData.columns)
            featuresForCrossTagMerge = list(self.featureFinderMaps[name].values())
            featuresToDrop = list(self.columnsToDropMaps[name])
            featureNamesOneTable = set(
                                       featureNamesOneTable
                                       ).difference(set(
                                                        featuresForCrossTagMerge
                                                        ).union(set(
                                                            featuresToDrop)))
            featureNames = featureNames.union(featureNamesOneTable)    
        return list(featureNames)


    def merge_marketDataByTag(self, tagName, axis=0, join="outer",
                                ignore_index = False,
                                keys=None,
                                levels=None,
                                names=None,
                                verify_integrity= False,
                                sort= False,
                                copy = True):
        if self.__isDataTagValid() and self.__isDataFrequencyValid()\
            and self.__isFeatureFinderValid():
            # get tables names of tables with given tagName
            tablesWithTagName = self.reverse_dataTagMapsByTag(tagName)           
            # drop columns
            try:
                self.drop_columnsByTag(tagName)
            except:
                Warning("Abundant columns in tag {} have been dropped, \
                         cannot drop again!".format(str(tagName)))            
            # update feature names
            featureNames = self.find_featureNamesByTag(tagName)
            self.featureNameByTag.update({tagName:featureNames})                  
            # for data of same tagName, merge by axis
            # merge step by step
            nameCacheQueue = []
            for name in tablesWithTagName:
                if len(nameCacheQueue) == 0:
                    nameCacheQueue.append(name)
                    dataFrame = self.dataMaps[name].marketData
                elif len(nameCacheQueue) < 2:
                    nameCacheQueue.append(name)
                if len(nameCacheQueue) == 2:
                    rightName = nameCacheQueue[-1]
                    dataFrame = pd.concat([dataFrame, self.dataMaps[rightName].marketData],
                                            axis, 
                                            join,
                                            ignore_index,
                                            keys,
                                            levels,
                                            names,
                                            verify_integrity,
                                            sort,
                                            copy)
                    nameCacheQueue.pop(0)
                if len(nameCacheQueue) > 2:
                    raise ValueError("name cache queue shouldn't be longer \
                                     than 2, mannual check required!")
                  
            self.dataMaps_mergedByTag.update({tagName:dataFrame})
            return True
    
    
    def merge_marketDataCrossTag(self, axis):
        if len(self.dataMaps_mergedByTag) > 0:
            # information needed to merge data:
            # tag: table merged by tag
            # tag: data frequency
            # when crossing tag merge, OHLC, FundamentalData and AlternativeData
            pass
            
    
