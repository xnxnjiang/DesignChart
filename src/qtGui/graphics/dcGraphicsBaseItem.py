# -*- coding: utf-8 -*-
"""
Created on Mo May 28 2018

@author: xnjiang
"""
import sys

#from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import *
from PyQt5.QtWidgets import *


class DC_GraphicsBaseItem(object):

    def __init__(self):
        self._initItem("BaseItem", "", userData=None)
        
    def _initItem(self, type, name, userData):
        self._type = type
        self._name = name
        self._userData = userData
        self._toolTip = ""
        self._bGuiModified = False

    def setName(self, name):
        self._name = name
    
    def getName(self):
        return self._name
    
    def getType(self):
        return self._type
    
    def getData(self):
        return self._userData
    
    def isModule(self):
        return self.getType() == "ModuleItem"
    
    def isPort(self):
        return self.getType() == "PortItem"
    
    def isLink(self):
        return self.getType() == "LinkItem"
    
    def isLinkChannel(self):
        return self.getType() == "LinkChannelItem"
    
    def isFlyLine(self):
        return self.getType() == "FlyLineItem"
    
    def isText(self):
        return self.getType() == "TextItem"
    
    def isRect(self):
        return self.getType() == "RectItem"
        
    def isProxyWidget(self):
        return self.getType() == "ProxyWidget"
        
    def isGroupItem(self):
        return self.getType() == "GroupItem"
        
    def isDummylItem(self):
        return self.getType() == "DummyItem"
    
    def setItemToolTip(self, toolTip):
        self._toolTip = toolTip

    def itemToolTip(self):
        return self._toolTip
    
    def _isShowFlyLine(self, bTmp):
        bShow = False
        chartView = self.scene().parent()
        if bTmp or chartView.isShowFlyLine():
            bShow = True
        return bShow
    
    def _isLockItemChange(self):
        return self.scene()._isLockItemChange()
    
    def setCursorShape(self, cursorShape):
        if Qt.ClosedHandCursor == cursorShape:
            pass
        elif Qt.ArrowCursor == cursorShape:
            pass
#        QApplication.restoreOverrideCursor()
#        cursor = self.cursor()
#        cursor.setShape(cursorShape)
        self.setCursor(cursorShape)
#        QApplication.setOverrideCursor(cursor)
        self.update()
    
#end class DC_GraphicsBaseItem
