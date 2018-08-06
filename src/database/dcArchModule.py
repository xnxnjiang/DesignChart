# -*- coding: utf-8 -*-
"""
Created on Mo May 28 2018

@author: xnjiang
"""

#import sys
#import os

from .dcArchBase import *
from .dcArchPort import *
from .dcArchLink import *

class DC_ArchModule(DC_ArchBase):
    
    def __init__(self, design, name, parent):
        super().__init__(name, parent)
        
        self._design = design
        self.setParent(parent)
        self._w = 150.0
        self._h = 150.0
        self._portW = 30
        self._portH = 30
        self._ports = {}
        self._nInputPort = 0
        self._nOutputPort = 0
#        self._parent = parent
        self._children = []
        self._link = None
        self._linkChannelSize = 5
        self._linkChannelLevel = 10
#        self._graphicsItem = None
#        self._guiData = {}

    def isDebug(self):
        return self._design.isDebug()
    
    def setParent(self, parent):
        if parent:
            self._parent = parent
            parent._addChild(self)
    
    def setGuiData(self, guiData):
        super().setGuiData(guiData)
        
#        wModule = 0
#        data = guiData.get("width")
#        if data != None:
#            wModule = float(data)
#        if wModule > 0:
#            self._w = wModule
#        
#        hModule = 0
#        data = guiData.get("height")
#        if data != None:
#            hModule = float(data)
#        if hModule > 0:
#            self._h = hModule
        
        link = self._link
        if link != None:
            direct = guiData.get("direct")
            if direct != None:
                link.setDirect(direct)
    
    def getW(self, parent):
        w = self._w
        guiData = self.getGuiData(parent)
        guiW = guiData.get("width")
        if guiW != None:
            w = float(guiW)
        elif self.isLink() == False:
            nPort = nPortIn = self._nInputPort#//2 + self._nInputPort%2
            nPortOut = self._nOutputPort#//2 + self._nOutputPort%2
            if nPortOut > nPort:
                nPort = nPortOut
            if nPort > 1:
#                w += w * nPort
                w += w * (nPort - 1)
        return w
    
    def setW(self, w):
        self._w = w
        
    def getH(self, parent):
        h = self._h
        guiData = self.getGuiData(parent)
        guiH = guiData.get("height")
        if guiH != None:
            h = float(guiH)
#        if self.isLink() == True:
#            pass
#        else:
#            nPort = nPortIn = self._nInputPort//2
#            nPortOut = self._nOutputPort//2
#            if nPortOut > nPort:
#                nPort = nPortOut
#            if nPort > 0:
#                h += h * (nPort -1)
        return h
    
    def setH(self, h):
        self._h = h
        
    def addPort(self, name, direct):
        port = DC_ArchPort(self, name, direct)
        port.setFullName(self.getFullName()+":"+name)
        self._ports[name] = port
        if direct.lower() == "dest":
            self._nInputPort += 1
        elif direct.lower() == "source":
            self._nOutputPort += 1
        return port
    
    def addInputCnt(self):
        self._nInputPort += 1
    
    def addOutputCnt(self):
        self._nOutputPort += 1
        
    def getInputCnt(self):
        return self._nInputPort
    
    def getInputUpCnt(self):
         nPort = self._nInputPort#//2 + self._nInputPort%2
         return nPort
     
    def getInputLeftCnt(self):
        nPort =  self._nInputPort - self.getInputUpCnt()
        return nPort
    
    def getOutputDownCnt(self):
         nPort = self._nOutputPort#//2 + self._nOutputPort%2
         return nPort
     
    def getOutputRightCnt(self):
        nPort =  self._nOutputPort - self.getOutputDownCnt()
        return nPort
    
    def getOutputCnt(self):
        return self._nOutputPort
    
    def getPort(self, name):
        port = self._ports.get(name)   
        return port
    
    def getPorts(self):
        return self._ports
    
    def getPortCnt(self):
        return len(self._ports)
    
    def getPortW(self):
        return self._portW
    
    def getPortH(self):
        return self._portH

    def _addChild(self, child):
        self._children.append(child)
        
    def getChildren(self):
        return self._children
        
    def removeChild(self, child):
        self._children.remove(child)

    def setLink(self):
        if self._link is None:
            link = DC_ArchLink(self, None, None)
            self._link = link
            #adjust size
        size = self._linkChannelSize
        for child in self._children:
            if self._link.isHor():
                child.setW(self.getW(self._link))
                child.setH(self._linkChannelSize)
            else:
                child.setW(self._linkChannelSize)
                child.setH(self.getH(self._link))
        
        if self._link.isHor():
            self._h = size * len(self._children)
        else:
            self._w = size * len(self._children)
            
        return self._link

    def getLink(self):
        return self._link
    
    def removeLink(self):
        self._link = None

    def getDirect(self, parent=None):
        direct = "UpToDown"
        if self.isLink():
#            guiData = self.getGuiData(parent)
#            direct = guiData.get("direct","UpToDown")
            direct = self._link.getDirect()
        return direct
    
    def isModule(self):
        return not self.isLink()
    
    def isLink(self):
        if self._link == None:
            return False
        else:
            return True

    def isChannel(self):
        parent = self.parent()
        if parent and parent.isLink():
            return True
        else:
            return False
        
    def getChannelLevel(self):
        return self._linkChannelLevel
        
    def getChannelSpace(self):
        return 50
#        return self.getH()
#        size = 0
#        for child in self._children:
#            if child.isLink():
#                h = child.getH() * len(child.getChildren())
#                if h > size:
#                    size = h
#        return size
