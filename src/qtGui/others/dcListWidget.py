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


class DC_ListWidget(QListWidget, object):

    def __init__(self):
        super(DC_ListWidget, self).__init__()
        self.initListWidget()

    def initListWidget(self):
        self.popCB = None
        self.clickCB = None
        self.dclickCB = None
        
        self.itemClicked.connect(self.itemClick)
        self.itemDoubleClicked.connect(self.itemDClick)

    def setPopupCB(self, cb):
        self.popCB = cb
    
    def setClickCB(self, cb):
        self.clickCB = cb

    def setDClickCB(self, cb):
        self.dclickCB = cb
        
    def contextMenuEvent(self, event):
        super(DC_ListWidget, self).contextMenuEvent(event)
        if self.popCB:
            self.popCB()

    def itemClick(self, item, column):
        if self.clickCB:
            self.clickCB(item, column)

    def itemDClick(self, item, column):
        if self.dclickCB:
            self.dclickCB(item, column)
            
#end class DC_ListWidget
