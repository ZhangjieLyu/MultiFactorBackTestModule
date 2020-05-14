# -*- coding: utf-8 -*-
"""
Created on Thu May 14 2020

@author: Robert
"""
class NameObj:
    """
    NameObj is a class used to name objects in the module
    """
    def __init__(self, nickname):
        self.objName = nickname
    
    def set_objName(self, nickname):
        self.objName = nickname

    def get_objName(self):
        return self.objName
