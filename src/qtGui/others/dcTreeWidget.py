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


class DC_TreeWidget(QTreeWidget, object):

    def __init__(self):
        super(DC_TreeWidget, self).__init__()
        self.initTreeWidget()

    def initTreeWidget(self):
        self.popCB = None
        self.clickCB = None
        self.dclickCB = None
        self.itemChangeCB = None
        
        self.itemClicked.connect(self.itemClick)
        self.itemDoubleClicked.connect(self.itemDClick)
        self.itemChanged.connect(self.itemChange)

    def setPopupCB(self, cb):
        self.popCB = cb
    
    def setClickCB(self, cb):
        self.clickCB = cb

    def setDClickCB(self, cb):
        self.dclickCB = cb

    def setItemChangeCB(self, cb):
        self.itemChangeCB = cb
        
    def contextMenuEvent(self, event):
        super(DC_TreeWidget, self).contextMenuEvent(event)
        if self.popCB:
            self.popCB()

    def emitItemClick(self, item, column):
        self.itemClicked.emit(item, column)
        self.setCurrentItem(item)
#        item.setSelected(True)
        
    def itemClick(self, item, column):
        if self.clickCB:
            self.clickCB(item, column)

    def itemDClick(self, item, column):
        if self.dclickCB:
            self.dclickCB(item, column)
            
    def itemChange(self, item, column):
        if self.itemChangeCB:
            self.itemChangeCB(item, column)
            
#end class DC_TreeWidget
