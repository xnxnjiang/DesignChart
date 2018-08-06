# -*- coding: utf-8 -*-
"""

@author: xnjiang
"""
import sys

#from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import *
from PyQt5.QtWidgets import *

from .dcGraphicsBaseItem import *
#from ....common.dcGlobal import *

class DC_GraphicsProxyWidget(QGraphicsProxyWidget, DC_GraphicsBaseItem):

    def __init__(self, parentItem, name="", module=None):
        super(DC_GraphicsProxyWidget, self).__init__(parentItem)
        self._initItem("ProxyWidget", name, module)

    def _showOnTop(self, bOnTop):
        self.scene().clearSelection()
        parentItem = self.parentItem()
        while parentItem != None:
            parentItem.setSelected(True)
            parentItem = parentItem.parentItem()
        self.scene().updateItemsZValue()
        item = self.scene().activePanel()
        if item:
            z = item.ZValue()
            item.setZValue(z+1)    
        
    def mousePressEvent(self, event):      
        super(DC_GraphicsProxyWidget, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
#            if not self._isLockItemChange():
                bIgnore = True
                widget = self.widget()
                if widget:
                    child = widget.childAt(event.pos().x(), event.pos().y())
                    if child and child.metaObject().className() == "QScrollBar":
                        bIgnore = False
                if bIgnore:
                    event.ignore()
                cursorShape = Qt.ClosedHandCursor
                self.setCursorShape(cursorShape)
            
#        if  event.button() == Qt.RightButton:#not self._isLockItemChange():
#            event.ignore()
#            modifier = event.modifiers()
#            if Qt.ControlModifier != modifier:
#                self.setSelected(True)
#            else:
#                bSelected = True
#                self.setSelected(bSelected)
#            self._showOnTop(True)      
    
    def mouseReleaseEvent(self, event):    
        super(DC_GraphicsProxyWidget, self).mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            event.ignore()
            super(DC_GraphicsProxyWidget, self).mouseReleaseEvent(event)
            
#        if event.button() == Qt.RightButton:#True:#not self._isLockItemChange():
#            event.ignore()
#            modifier = event.modifiers()
#            if Qt.ControlModifier != modifier:
#                self.setSelected(True)
#            else:
#                bSelected = True
#                self.setSelected(bSelected)
#        cursorShape = Qt.ArrowCursor
#        self.setCursorShape(cursorShape)
 
    def mouseMoveEvent(self, event):
        if self._isLockItemChange():
            modifier = event.modifiers()
            if Qt.ControlModifier == modifier:
                #select item
                event.ignore()
            else:
                #move view
#                event.ignore()
                super(DC_GraphicsProxyWidget, self).mouseMoveEvent(event)
        else:
            super(DC_GraphicsProxyWidget, self).mouseMoveEvent(event)
            
#end class DC_GraphicsProxyWidget
