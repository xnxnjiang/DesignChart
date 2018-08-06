# -*- coding: utf-8 -*-
"""
Created on Mo May 28 2018

@author: xnjiang
"""

#import sys
#import os

from .dcArchBase import *

class DC_ArchPort(DC_ArchBase):
    
    def __init__(self, module, name, direct):
        super().__init__(name, module)
        
#        self._module = module
        self._direct = direct
        self._w = module.getPortW()
        self._h = module.getPortH()
    
    def isPort(self):
        return True
    
    def getModule(self):
#        return self._module
        return self._parent
    
    def isInput(self):
        if self.isOutput():
            return False
        else:
            return True

    def isOutput(self):
        if self.getDirect().lower() == "output":
            return True
        else:
            return False
        
    def getDirect(self):
        if "dest" == self._direct.lower():
            return "Input"
        elif "source" == self._direct.lower():
            return "Output"
        elif "inout" == self._direct.lower():
            return "Inout"
        else:
            return self._direct
        
    def setDirect(self, direct):
        self._direct = direct
        if direct.lower() == "dest":
            self.getModule().addInputCnt()
        elif direct.lower() == "source":
            self.getModule().addOutputCnt()
    
    def setW(self, w):
        if self.getModule().isDebug() == False:
            self._w = w
        
    def getW(self):
        return self._w
    
    def setH(self, h):
        if self.getModule().isDebug() == False:
            self._h = h
        
    def getH(self):
        return self._h

