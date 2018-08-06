# -*- coding: utf-8 -*-
"""
Created on Mo May 28 2018

@author: xnjiang
"""

#import sys
#import os

from .dcArchBase import *
from .dcArchPort import *

class DC_ArchLink(DC_ArchBase):
    
    def __init__(self, module, source, dest):
        super().__init__(module.getName(), module)
        
        self._module = module
        self._source = source
        self._dest = dest
        self._direct = "UpToDown"
                     
    def isHor(self):
        if self.getDirect().lower() == "lefttoright" or self.getDirect().lower() == "righttoleft":
            return True
        else:
            return False
        
    def getDirect(self):
        return self._direct
    
    def setDirect(self, direct):
        self._direct = direct
        
    def getSrc(self):
        return self._source

    def setSrc(self, source):
        self._source = source
        self.updateSrc()
        
    def getDest(self):
        return self._dest

    def setDest(self, dest):
        self._dest = dest
        self.updateDest()
    
    def updatePort(self):
        self.updateSrc()
        self.updateDest()
     
    def updateSrc(self):
        if self._direct.lower() == "lefttoright" or self._direct.lower() == "righttoleft":
            H0 = self._source.getH()
            H1 = self.getH()
            self._source.setH(H0+H1)
        else:
            w0 = self._source.getW()
            w1 = self.getW()
            self._source.setW(w0+w1)
    
    def updateDest(self):
        if self._direct.lower() == "lefttoright" or self._direct.lower() == "righttoleft":
            h0 = self._dest.getH()
            h1 = self.getH()
            self._dest.setH(h0+h1)
        else:
            w0 = self._dest.getW()
            w1 = self.getW()
            self._dest.setW(w0+w1)
    
    def getW(self):
        return self._module.getW(self)
    
    def getH(self):
        return self._module.getH(self)
        
