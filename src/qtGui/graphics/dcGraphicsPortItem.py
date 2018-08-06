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

from .dcGraphicsRectItem import *
from .dcGraphicsTextItem import *


class DC_GraphicsPortItem(DC_GraphicsRectItem):

    def __init__(self, port, x, y, w, h, name, color, font, pos, parentItem):
        super(DC_GraphicsPortItem, self).__init__(x, y, w, h, parentItem)
#        parentItem.stackBefore(self)
        proxyItem = parentItem.getProxy()
        if proxyItem:
            proxyItem.stackBefore(self)
        self._initPortItem(port, name, pos)
        toolTip = "       Port: "+name+"\n"+parentItem.toolTip()
        self.setToolTip(toolTip)
        #port name
        self._nameItem = textItem = DC_GraphicsTextItem(name, self)
        textItem.setFont(font)
        textItem.setDefaultTextColor(color)
        textItem.setToolTip(toolTip)
        self.adjustNamePos()
    
    def _initPortItem(self, port, name, pos):
        self._initItem("PortItem", name, port)
#        self._port = port
        self._pos = pos
    
    def getPort(self):
#        return self._port
        return self.getData()
    
    def drawFlyLine(self, bTmp, bOnlySelf=True):
        moduleItem = self.parentItem()
        items = self.scene().items()
        for item in items:
            if hasattr(item, "getType") and item.isLink():
                linkModule = item.getModule()
                link = linkModule.getLink()
                if link.getSrc() == self.getPort() or link.getDest() == self.getPort():
                    if bOnlySelf:
                        item.drawPortFlyLine(self, bTmp)
                    else:
                        item.drawFlyLine(bTmp)
                    break
        self.scene().update()

    def adjustNamePos(self):
        if self._nameItem != None:
            moduleItem = self.parentItem()
            if moduleItem != None:
                rect = self.rect()
                x = rect.x()
                y = rect.y()
                w = rect.width()
                h = rect.height()
                xText = x
                yText = y
                pos = moduleItem.getPortPos(self)
                font = self._nameItem.font()
                if pos.lower() ==  "up":
                    yText += h - 3
                elif pos.lower() == "down":
                    yText -= h/2 + QFontMetricsF(font).height()/2
                elif pos.lower() == "left":
                    xText += w
                elif pos.lower() == "right":
                    xText -= QFontMetricsF(font).width(self._nameItem.toPlainText()) + QFontMetricsF(font).height()/2
            self._nameItem.setPos(xText, yText)

    def adjustRect(self):
        moduleItem = self.parentItem()
        if moduleItem != None:
            portPos = moduleItem.getPortPos(self)
            rect = self.rect()
            w = rect.width()
            h = rect.height()
            if portPos == "Left" or portPos == "Right":
                if w > h:
                    x = rect.x()
                    y = rect.y()
#                    if portPos == "Left":
#                        x += (w-h)/2
#                    else:
#                        x += (w-h)/2
                    x += (w-h)/2
                    y -= (w-h)/2
                    w = h
                    h = rect.width()
                    self.setRect(x, y, w, h)
            elif portPos == "Up" or portPos == "Down":
                if h > w:
                    x = rect.x()
                    y = rect.y()
#                    if portPos == "up":
#                        x -= (h-w)/2
#                    else:
#                        x -= (h-w)/2
                    x -= (h-w)/2
                    y += (h-w)/2
                    w = h
                    h = rect.width()
                    self.setRect(x, y, w, h)
            #adjust name pos
            self.adjustNamePos()
            
    def itemChange(self, change, value):
        newPos = value
        moduleItem = self.parentItem()
        if moduleItem and change == QGraphicsItem.ItemPositionChange:
            #adjust port's rect
            self.adjustRect()
            #Keep port inside the module rect.
            rectParent = moduleItem.rect()
            rect = self.boundingRect()
            xOffset = rect.x()+rect.width()/2
            yOffset = rect.y()+rect.height()/2
            pos = QPointF(value.x()+xOffset, value.y()+yOffset)
            if not rectParent.contains(pos):
                pos.setX(min(rectParent.right(), max(pos.x(), rectParent.left())))
                pos.setY(min(rectParent.bottom(), max(pos.y(), rectParent.top())))
                newPos = QPointF(pos.x()-xOffset, pos.y()-yOffset)
                    
            self.drawFlyLine(True)
        return newPos

    def contextMenuEvent(self, event):
#        super(DC_GraphicsPortItem, self).contextMenuEvent(event)
        popMenu = QMenu()
        act = popMenu.addAction("Show Annotation")
        act.triggered.connect(self.showAnnotationCB)
        self.addCommonPopupMenu(popMenu, "port")
        popMenu.exec(event.screenPos())
            
    def mousePressEvent(self, event):
        super(DC_GraphicsPortItem, self).mousePressEvent(event)
        self.drawFlyLine(True)
#        cursorShape = Qt.ClosedHandCursor
#        self.setCursorShape(cursorShape)
        
    def mouseReleaseEvent(self, event):
        super(DC_GraphicsPortItem, self).mouseReleaseEvent(event)
        self.drawFlyLine(False)
#        cursorShape = Qt.ArrowCursor
#        self.setCursorShape(cursorShape)

#    def mouseMoveEvent(self, event):
#        super(DC_GraphicsRectItem, self).mouseMoveEvent(event)
#    #end def mouseMoveEvent
    
#    def boundingRect(self):
#        return super(DC_GraphicsRectItem, self).boundingRect()
    
    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        
        moduleItem = self.parentItem()
        if moduleItem != None:
            p1 = None
            p2 = None
            p3 = None
            pen = self.pen()
            pW = pen.width()
            rect = self.rect()
            x = rect.x() + pW/2
            y = rect.y() + pW/2
            w = rect.width() - pW
            h = rect.height() - pW
                
            portPos = moduleItem.getPortPos(self)
            if portPos == "" or portPos == "Up" or portPos == "UpLeft" or portPos == "UpRight":
                if self.getPort().isInput():
                    p1 = QPointF(x, y)
                    p2 = QPointF(x+w, y)
                    p3 = QPointF(x+w/2, y+h/2)
                else:
                    p1 = QPointF(x, y+h)
                    p2 = QPointF(x+w, y+h)
                    p3 = QPointF(x+w/2, y+h/2)
            elif portPos == "Down" or portPos == "DownLeft" or portPos == "DownRight":
                if self.getPort().isInput():
                    p1 = QPointF(x, y+h)
                    p2 = QPointF(x+w, y+h)
                    p3 = QPointF(x+w/2, y+h/2)
                else:
                    p1 = QPointF(x, y)
                    p2 = QPointF(x+w, y)
                    p3 = QPointF(x+w/2, y+h/2)
            if portPos == "Left":
                if self.getPort().isInput():
                    p1 = QPointF(x, y)
                    p2 = QPointF(x, y+h)
                    p3 = QPointF(x+w/2, y+h/2)
                else:
                    p1 = QPointF(x+w, y)
                    p2 = QPointF(x+w, y+h)
                    p3 = QPointF(x+w/2, y+h/2)
                pass
            elif portPos == "Right":
                if self.getPort().isInput():
                    p1 = QPointF(x+w, y)
                    p2 = QPointF(x+w, y+h)
                    p3 = QPointF(x+w/2, y+h/2)
                else:
                    p1 = QPointF(x, y)
                    p2 = QPointF(x, y+h)
                    p3 = QPointF(x+w/2, y+h/2)

            if p1 and p2 and p3:
                pen.setWidth(1)
                pen.setColor(QColor("black"))
                painter.setPen(pen)
                brush = QBrush(pen.color())
                painter.setBrush(brush)
                painter.drawPolygon(p1, p2, p3)
                
#            self.drawFlyLine(False)
    #end def paint
#end class DC_GraphicsRectItem
