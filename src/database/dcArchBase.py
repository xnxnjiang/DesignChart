# -*- coding: utf-8 -*-
"""
Created on Mo May 28 2018

@author: xnjiang
"""

#import sys
#import os


class DC_ArchBase(object):
    
    def __init__(self, name, parent):
        self._name = name
        self._parent = parent
        self._fullName = ""
        self._graphicsItem = None
        self._designItem = None
        self._guiData = {}
        self._guiData["top"] = "false"
        self._guiDataTop = {}
        self._guiDataTop["top"] = "true"
        self._guiDataModified = False
    
    def isModule(self):
        return False
    
    def isPort(self):
        return False

    def isLink(self):
        return False
    
    def isChannel(self):
        return False
    
    def setFullName(self, fullName):
        self._fullName = fullName

    def getFullName(self):
        return self._fullName
    
    def parent(self):
        return self._parent

    def setGuiData(self, data):#for loading gui data from design file
        top = data.get("top")
        if top and top.lower()=="true":
            self._guiDataTop = data
            self._guiDataTop["top"] = "true"
        else:
            self._guiData = data
            self._guiData["top"] = "false"
        
    def getGuiData(self, parent):
        if parent == None:
            return self._guiDataTop
        else:
            return self._guiData
        
    def setGuiDataAttr(self, parent, key, val):
        guiData = self.getGuiData(parent)
        guiData[key] = str(val)
    
    def hasGuiData(self, parent):
        guiData = self.getGuiData(parent)
        if guiData and len(guiData)>1:
            return True
        return False
    
    def isVisible(self):
        bVisible = True
        guiData = self.getGuiData(self)
        visible = guiData.get("visible")
        if visible and len(visible):
            if visible.lower() == "false":
                bVisible = False
        return bVisible
                
    def xPos(self, parent):
        xPos = 0.0
        guiData = self.getGuiData(parent)
        data = guiData.get("xPos")
        if data != None:
            xPos = float(data)
        return xPos
    
    def yPos(self, parent):
        yPos = 0.0
        guiData = self.getGuiData(parent)
        data = guiData.get("yPos")
        if data != None:
            yPos = float(data)
        return yPos
    
    def x(self, parent):
        xRect = 0.0
        guiData = self.getGuiData(parent)
        data = guiData.get("x")
        if data != None:
            xRect = float(data)
        return xRect
    
    def y(self, parent):
        yRect = 0.0
        guiData = self.getGuiData(parent)
        data = guiData.get("y")
        if data != None:
            yRect = float(data)
        return yRect
        
    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name
        
    def setGraphicsItem(self, item):
        self._graphicsItem = item
            
    def getGraphicsItem(self):
        return self._graphicsItem

    def setDesignItem(self, item):
        self._designItem = item
        
    def getDesignItem(self):
        return self._designItem