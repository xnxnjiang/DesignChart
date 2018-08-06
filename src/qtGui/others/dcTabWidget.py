# -*- coding: utf-8 -*-
"""
Created on Mo May 28 2018

@author: xnjiang
"""
#import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import *
from PyQt5.QtWidgets import *


class DC_TabWidget(QTabWidget, object):

    def __init__(self, parent=None, sType="tab"):
        super(DC_TabWidget, self).__init__()
        self.initTabWidget(sType)

    def getType(self):
        return self._sType
    
    def initTabWidget(self, sType):
        self._sType = sType
        
        self.setMovable(True)
        self.setTabsClosable(True)
        
        self.popCB = None
        self.currentChangeCB = None
        self.clickCB = None
        self.dclickCB = None
        
        self.currentChanged.connect(self.currentChange)
        self.tabBarClicked.connect(self.tabClick)
        self.tabBarDoubleClicked.connect(self.tabDClick)
        self.tabCloseRequested.connect(self.tabClose)
        
    def setPopupCB(self, cb):
        self.popCB = cb
    
    def setCurrentChangeCB(self, cb):
        self.currentChangeCB = cb
        
    def setClickCB(self, cb):
        self.clickCB = cb

    def setDClickCB(self, cb):
        self.dclickCB = cb
        
    def contextMenuEvent(self, event):
        super(DC_TabWidget, self).contextMenuEvent(event)
        if self.popCB:
            index = self.tabBar().tabAt(event.pos())
            if -1 != index:
                self.setCurrentIndex(index)
                self.popCB(self, index)

    def currentChange(self, index):
        if self.currentChangeCB:
            self.currentChangeCB(self, index)
            
    def tabClick(self, index):
        if self.clickCB:
            self.clickCB(self, index)

    def tabDClick(self, index):
        if self.dclickCB:
            self.dclickCB(self, index)
            
    def tabClose(self, index):
        self.setCurrentIndex(index)
        
#        msgBox = QMessageBox()
        sType = self.getType()
        widget = self.widget(index)
        if hasattr(widget, "getType"):
            sType = widget.getType()
        sInfo = "Do you want to delete %s \"%s\"?" % (sType, self.tabText(index))
#        msgBox.setInformativeText(sInfo)
#        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
#        msgBox.setDefaultButton(QMessageBox.Cancel)
#        ret = msgBox.exec_()
        ret = QMessageBox.warning(self, "DC", sInfo, QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
        if ret == QMessageBox.Ok:
            self.removeTab(index)
            del widget
        
#end class DC_TabWidget
