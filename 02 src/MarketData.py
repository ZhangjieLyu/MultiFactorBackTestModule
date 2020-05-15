# -*- coding: utf-8 -*-
"""
Created on Thu May 14 2020

@author: Robert
"""
from NameObj import NameObj
DATA_FREQUENCY = 1
class MarketData(NameObj):
    """
    MarketData is a type to store OHLC, fundamental data and alternative data
    Require data's columns to be features, which is one type of data from WIN.D API.
    """
    DATA_FREQUENCY = ["D","W","M","Q","S","A","X"]
    DATA_TAG = ["OHLC", "PriceAdj", "Return", "FundamentalData",
                "AlternativeData", "Benchmark", "ScreenReference",
                "SectorClassifier"]
    
    def __init__(self, marketData):
        self.marketData = marketData
        
    def set_dataFreqency(self, dataFrequency):
        if dataFrequency in self.DATA_FREQUENCY:
            self.dataFrequency = dataFrequency
        else:
            raise ValueError("data frequency can only be 'Q'-Quarter, 'S'-SemiYear, 'D'-Daily, 'M'-Month\
                             'W'-weekly, 'A'-Annual, 'X'-not a fixed frequency but refresh rate is no shorter\
                                 than 1 day")

    def set_objName(self, nickname):
        super().__init__(nickname)
        
    def set_dataTag(self, tagName):
        if tagName in self.DATA_TAG:
            self.dataTag = tagName
        else:
            raise ValueError("data tag can only be OHLC, PriceAdj, Return,\
                             FundamentalData, AlternativeData, Benchmark,\
                             ScreenReference,SectorClassifier")
                             
                             
    def set_featureFinder(self, columnDict):
        if set(list(columnDict.keys())).issubset(["TradingDate","Date",\
                                             "AnnouncementDate","AssetID",\
                                                 "TickName"]) \
            and len(list(columnDict.keys()))>=1:
            self.featureFinder = columnDict
        else:
            raise ValueError("feature must be in range of 'TradingDate','Date',\
                             'AnnouncementDate','AssetID','TickName'.")
                             
    
    def set_columnsToDrop(self, columnNames):
        self.columnsToDrop = [col for col in columnNames if \
                              col in list(self.marketData.columns)]
            

    def describe(self):
        print("Data Frequency is {} \n".format(self.dataFrequency))
        print("Data Tag is {} \n".format(self.dataTag))
        print("Data Short summary is: \n")
        print(self.marketData.info())
            
    