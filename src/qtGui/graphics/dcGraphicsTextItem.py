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

from .dcGraphicsBaseItem import *

class DC_GraphicsTextItem(QGraphicsTextItem, DC_GraphicsBaseItem):

    def __init__(self, text, parentItem):
        super(DC_GraphicsTextItem, self).__init__(text, parentItem)
#        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.initTextItem(text)

    def initTextItem(self, text):
        self._initItem("TextItem", text, None)
        self._origText = text

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        
#    def mousePressEvent(self, event):
#        super(DC_GraphicsTextItem, self).mousePressEvent(event)
#
#    def mouseMoveEvent(self, event):
#        super(DC_GraphicsTextItem, self).mouseMoveEvent(event)
    
#end class DC_GraphicsRectItem
