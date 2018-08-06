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

class DC_GraphicsFlyLineItem(QGraphicsLineItem, DC_GraphicsBaseItem):

    def __init__(self, xStart, yStart, xEnd, yEnd, parentItem):
        super().__init__(xStart, yStart, xEnd, yEnd, parentItem)
        self._initItem("FlyLineItem", "", None)
        
        self.setZValue(10000)
#        self.setFlags(QGraphicsItem.ItemIsSelectable)
        pen = QPen(Qt.red)
        pen.setWidth(3)
        pen.setStyle(Qt.DotLine)
        self.setPen(pen)
        self._arrowL = 10 + self.pen().width()
        self._lenOffset = 0
        self.adjustLineLength()
    
    def adjustLineLength(self):
        if self._arrowL > 0:
            line = self.line()
            self._lenOffset = length = line.length() - self._arrowL
#            if length > 0
            line.setLength(length)
            super().setLine(line)
        
    def setLine(self, x1, y1, x2, y2):
        super().setLine(x1, y1, x2, y2)
        self.adjustLineLength()
        
    def drawLineWithArrow(self, painter):
        arrowL = self._arrowL
        line = self.line()
        v = line.unitVector()
        if self._lenOffset < 0:
            v.setP2(line.p2())
            p1 = v.p1()
            p2 = v.p2()
            v.setP1(p2)
            v.setP2(p1)
        else:
            v.translate(QPointF(line.dx(), line.dy()))
        v.setLength(arrowL)
        
        n = v.normalVector()#normal line
        n.setLength(arrowL/2)#arrow width
        n2 = n.normalVector().normalVector()#reversed normal line
        
        p1 = v.p2()
        p2 = n.p2()
        p3 = n2.p2()        
        
        pen = painter.pen()
        pen.setWidth(1)
        pen.setStyle(Qt.SolidLine)
        painter.setPen(pen)
        brush = QBrush()
        brush.setColor(pen.color())
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        painter.drawPolygon(p1, p2, p3)
    #end def drawArrow
    
    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        self.drawLineWithArrow(painter)
        
#    def boundingRect(self):
#        rect = super().boundingRect()
##        line = self.line()
##        p1 = line.p1()
##        p2 = line.p2()
##        x1 = p1.x()
##        y1 = p1.y()
##        x2 = p2.x()
##        y2 = p2.y()
##        x = x1
##        y = y1
##        w = x2 - x1 + self._arrowL
##        h = y2 - y1 + self._arrowL
#        x = rect.x()
#        y = rect.y()
#        w = rect.width() + self._arrowL
#        h = rect.height() + self._arrowL
#        print(x, y, w, h)
#        return QRectF(x, y, w, h)
    
#end class DC_GraphicsFlyLineItem
