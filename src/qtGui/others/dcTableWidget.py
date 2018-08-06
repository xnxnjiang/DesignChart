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


class DC_TableWidget(QTableWidget, object):

    def __init__(self):
        super(DC_TableWidget, self).__init__()
        self.setStyle(QStyleFactory.create("Windows"))
        self.setPalette(self.style().standardPalette())
        
        hHeader = self.horizontalHeader()
        hHeader.setStyle(QStyleFactory.create("Windows"))
        hHeader.setPalette(hHeader.style().standardPalette())
#        hHeader.setSectionResizeMode(QHeaderView.Stretch)
#        hHeader.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setHorizontalHeader(hHeader)
#        hHeader.setVisible(False)
        
        vHeader = self.verticalHeader()
        vHeader.setStyle(QStyleFactory.create("Windows"))
        vHeader.setPalette(vHeader.style().standardPalette())
        self.setVerticalHeader(vHeader)
        vHeader.setVisible(False)
        
        self.initTableWidget()

    def initTableWidget(self):
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
        super(DC_TableWidget, self).contextMenuEvent(event)
        if self.popCB:
            self.popCB()

    def itemClick(self, item):
        if self.clickCB:
            self.clickCB(item)

    def itemDClick(self, item):
        if self.dclickCB:
            self.dclickCB(item)
            
#end class DC_TableWidget
