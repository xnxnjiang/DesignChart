# -*- coding: utf-8 -*-
"""
Created on Mo May 28 2018

@author: xnjiang
"""
#import sys

#from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import *
from PyQt5.QtWidgets import *

#from dcGraphicsRectItem import *
#from dcGraphicsTextItem import *
#from dcGraphicsModuleItem import *
#from dcGraphicsPortItem import *
#from dcGraphicsLinkItem import *
#from dcGraphicsLinkChannelItem import *

class DC_GraphicsView(QGraphicsView, object):

    def __init__(self):
        super(DC_GraphicsView, self).__init__()
        self._initView()

    def _initView(self):
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setRubberBandSelectionMode(Qt.ContainsItemShape)
#        self.setRubberBandSelectionMode(Qt.ContainsItemBoundingRect)
#        self.setRubberBandSelectionMode(Qt.IntersectsItemShape)
#        self.setRubberBandSelectionMode(Qt.IntersectsItemBoundingRect)

    
    def drawFlyLine(self):
        items = self.scene().items()
        for item in items:
            if hasattr(item, "getData") and item.isLink():
                item.drawFlyLine()
                
    def mousePressEvent(self, event):
#        print("view press")
        modifier = event.modifiers()
        if Qt.ControlModifier == modifier:
            item = self.itemAt(self.mapFromGlobal(QCursor.pos()))
            if item == None:
                self.setDragMode(QGraphicsView.RubberBandDrag)
            else:
                self.setDragMode(QGraphicsView.ScrollHandDrag)
        else:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
#        print("view release")
        super().mouseReleaseEvent(event)
        self.drawFlyLine()

    def mouseMoveEvent(self, event):
        super(DC_GraphicsView, self).mouseMoveEvent(event)
    
    def wheelEvent(self, event):
#        scaleFactor = self.matrix().m11()#current zoom 
        modifier = event.modifiers()
        if Qt.ControlModifier == modifier:
            wheelDeltaValue = event.angleDelta().y()/8
            if wheelDeltaValue != 0:
                if wheelDeltaValue > 0:#scroll up, zoom in
                    self.scale(1.2, 1.2)
                else:#scroll down, zoom out
                    self.scale(1.0 / 1.2, 1.0 / 1.2)
#            self.centerOn(event.pos());
#            self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        else:
            super(QGraphicsView, self).wheelEvent(event)


#    def _drawTestItem(self):
#        self.scene().drawTestItem();
    
#end class AW_GraphicsView
