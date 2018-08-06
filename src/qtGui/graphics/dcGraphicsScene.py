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

from .dcGraphicsRectItem import *
from .dcGraphicsTextItem import *
from .dcGraphicsModuleItem import *
from .dcGraphicsPortItem import *
from .dcGraphicsLinkItem import *
from .dcGraphicsLinkChannelItem import *
from .dcGraphicsDummyItem import *
from .dcGraphicsGroupItem import *

class DC_GraphicsScene(QGraphicsScene, object):

    def __init__(self, parent):
        super(DC_GraphicsScene, self).__init__(parent)
        self._focusItem = None
        self._initScene()

    def _initScene(self):
        self.selectionChanged.connect(self.updateItemsZValue)
        pass

    def _isLockItemChange(self):
        bLock = False
        chartView = self.parent()
        if chartView.isLockItemChange():
            bLock = True
        return bLock
    
    def setToolTip(self, toolTip):
        self._toolTip = toolTip
        
    def toolTip(self):
        return self._toolTip
    
    def setItemToolTip(self, item):
        toolTip = item.toolTip()+"\n"+self.toolTip()
        item.setToolTip(toolTip)
        
    def addModuleItem(self, module, x, y, w, h, name, bDebug, parentItem=None, pen=QPen(), brush=QBrush(), color=QColor(), font=QFont()):
        #module rect
        item =  DC_GraphicsModuleItem(module, x, y, w, h, name, color, font, bDebug, parentItem)
        item.setPen(pen)
        item.setBrush(brush)
        item.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemSendsGeometryChanges)# | QGraphicsItem.ItemContainsChildrenInShape)# | QGraphicsItem.ItemClipsToShape)# | QGraphicsItem.ItemClipsChildrenToShape)
        if self._isLockItemChange() == False:
            item.setFlag(QGraphicsItem.ItemIsMovable, True)
        if parentItem == None:
            self.addItem(item)
        self.setItemToolTip(item)
        return item
    
    def addPortItem(self, port, x, y, w, h, name, moduleItem, pos, pen=QPen(), brush=QBrush(), color=QColor(), font=QFont()):
        #port rect
        item =  DC_GraphicsPortItem(port, x, y, w, h, name, color, font, pos, moduleItem)
        item.setPen(pen)
        item.setBrush(brush)
        item.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemSendsGeometryChanges)
        if self._isLockItemChange() == False:
            item.setFlag(QGraphicsItem.ItemIsMovable, True)
        if moduleItem == None:
            self.addItem(item)
        return item

    def addLinkItem(self, link, x, y, w, h, name, direct, nChannel, bDebug, parentItem=None, pen=QPen(), brush=QBrush(), color=QColor(), font=QFont()):
        item = DC_GraphicsLinkItem(link, x, y, w, h, name, color, font, direct, nChannel, bDebug, parentItem)
        item.setPen(pen)
        item.setBrush(brush)
        item.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemSendsGeometryChanges)# | QGraphicsItem.ItemContainsChildrenInShape)# | QGraphicsItem.ItemClipsToShape)# | QGraphicsItem.ItemClipsChildrenToShape)
        if self._isLockItemChange() == False:
            item.setFlag(QGraphicsItem.ItemIsMovable, True)
        if parentItem == None:
            self.addItem(item)
        self.setItemToolTip(item)
        return item
    
    def addLinkChannelItem(self, channel, x, y, w, h, name, direct, nLevel, linkItem, pen=QPen(), brush=QBrush(), color=QColor(), font=QFont()):
        item = DC_GraphicsLinkChannelItem(channel, x, y, w, h, name, direct, nLevel, linkItem)
#        item.setFlags(QGraphicsItem.ItemIsSelectable)
#        item.setFocusProxy(linkItem)
        item.setPen(pen)
        item.setBrush(brush)
        
        xLevel = x
        yLevel = y
        wLevel = w
        hLevel = h/nLevel
        for level in range(nLevel):
            levelItem = self.addRectItem(xLevel, yLevel, wLevel, hLevel, item, pen, brush)
            yLevel += hLevel
#            if direct.lower() ==  "uptodown" or 
#            direct.lower() == "downtoup":
            toolTip = "      Level: "+str(level+1)+"\n"+item.toolTip()
            levelItem.setToolTip(toolTip)
        return item
            
    def addTextItem(self, text, x, y, parent=None, color=QColor()):
        item = DC_GraphicsTextItem(text, parent)
        item.setDefaultTextColor(color)
        item.setPos(x, y)
        return item
    
    def addLineItem(self, xStart, yStart, xEnd, yEnd, parent=None, pen=QPen()):
        item = DC_GraphicsLineItem(xStart, yStart, xEnd, yEnd, parentItem)
        item.setPen(pen)
        if parent == None:
            self.addItem(item)
        return item

    def addRectItem(self, x, y, w, h, parent=None, pen=QPen(), brush=QBrush()):
        item = DC_GraphicsRectItem(x, y, w, h, parent)
        item.setPen(pen)
        item.setBrush(brush)
        if parent == None:
            self.addItem(item)
#        item.setFlags((QGraphicsItem.GraphicsItemFlag)(1|2|4|8|QGraphicsItem.ItemSendsGeometryChanges))
        return item
    
    def addGroupItem(self, parent=None):
        item = DC_GraphicsGroupItem();
        item.setFlags(QGraphicsItem.ItemIsSelectable)
        if self._isLockItemChange() == False:
            item.setFlag(QGraphicsItem.ItemIsMovable, True)
        if parent == None:
            self.addItem(item)
        return item
    
    def addDummyItem(self, parent=None):
        item = DC_GraphicsDummyItem();
#        group.setFlags(QGraphicsItem.ItemIsSelectable)
#        if self._isLockItemChange() == False:
#            item.setFlag(QGraphicsItem.ItemIsMovable, True)
        if parent == None:
            self.addItem(item)
        return item
    
    def addWidget(self, x, y, widget, flags):
        proxy = super().addWidget(widget, flags)
        proxy.setPos(x, y)
        return proxy
    
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

    def showOnTop(self, item):
        parentItem = item
        while parentItem != None:
            parentItem.setZValue(1)
            parentItem = parentItem.parentItem()
    
    def updateItemsZValue(self):
        items = self.items()
        for item in items:
            if not hasattr(item, "getType") or not item.isFlyLine():
                item.setZValue(0)
            
        items = self.selectedItems()
        for i, item in enumerate(items):
            self.showOnTop(item)
#            item.setZValue(1)
    def itemIsSelected(self, item):
        bSelected = False
        if item:
            if (item.flags() & QGraphicsItem.ItemIsSelectable) == QGraphicsItem.ItemIsSelectable:
                return item.isSelected()
            else:
                item = item.parentItem()
                self.itemIsSelected(item)
        return bSelected
        
    def selectItem(self, item, bSelected):
        if item:
            if item.isModule() or item.isLink() or item.isPort():
#            if (item.flags() & QGraphicsItem.ItemIsSelectable) == QGraphicsItem.ItemIsSelectable:
                item.setSelected(bSelected)
            else:
                item = item.parentItem()
                self.selectItem(item, bSelected)
                
    def mousePressEvent(self, event):
        super(DC_GraphicsScene, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton or event.button() == Qt.RightButton:
            item = self.focusItem()
#            print("scene press %s" % item)
            if item == None:
                items = self.items(event.scenePos())
                if len(items):
                    for item in items:
                        if item.isText():
                            item = item.parentItem()
#                        if item.isModule() or item.isLink() or item.isPort() or item.isProxyWidget():
                        if item.isModule() or item.isLink() or item.isPort():
#                        if item.isUnderMouse() and (item.isModule() or item.isLink() or item.isPort() or item.isProxyWidget()):
#                        if item.isUnderMouse():
                            break
            self._focusItem = item
#            print(item)
            if self._isLockItemChange():
                if item != None:
                    modifier = event.modifiers()
                    if Qt.ControlModifier != modifier:
                        self.clearSelection()
                        self.selectItem(item, True)
                    else:
                        QApplication.processEvents()
#            self._focusItem = self.focusItem()
            if self._focusItem:# and (self._focusItem.isModule() or self._focusItem.isLink() or self._focusItem.isPort() or self._focusItem.isProxyWidget()):
                view = self.parent()
                hasFocus = True
                if event.button() == Qt.RightButton:
                    hasFocus = False
                view.selectDesignItem(self._focusItem, hasFocus)
    
    def mouseReleaseEvent(self, event):
        super(DC_GraphicsScene, self).mouseReleaseEvent(event)
#        items = self.items(event.scenePos())
#        if len(items):
#            for item in items:
#                if item.isUnderMouse():
#                    break
#        item = self.focusItem()#None
        item = self._focusItem
#        print("scene release %s" % item)
        if item:
            if self._isLockItemChange():
                z = item.zValue()
                item.setZValue(z+1)
                modifier = event.modifiers()
                if Qt.ControlModifier != modifier:
                    self.clearSelection()
#                    self.update()
                    self.selectItem(item, True)
                else:
                    QApplication.processEvents()
                    items = self.selectedItems()
                    bSelected = not self.itemIsSelected(item)
                    self.selectItem(item, bSelected)
                    for item in items:
                        item.setSelected(True)
#                    event.ignore()
            cursorShape = Qt.ArrowCursor
            if hasattr(item, "setCursorShape"):
                item.setCursorShape(cursorShape)
            else:
                item.setCursor(cursorShape)

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        item = self.itemAt(event.scenePos().x(), event.scenePos().y(), QTransform())
        if hasattr(item, "getType") and item.isText():
            item.setTextInteractionFlags(Qt.TextEditorInteraction)
            item.setSelected(True)
            item.setFocus()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

#    def drawTestItem(self):
#        self.myBtn = QPushButton("Test")
#        self.myBtnProxy = self.addWidget(self.myBtn);
#        self.myBtnProxy.setPos(0, 20)
#        btnRect = self.addRect(QRectF(0, 0, self.myBtn.width(), self.myBtn.height()+20), QPen(), self.brush)
#        btnRect.setFlag(QGraphicsItem.ItemIsMovable, True)
#        btnRect.setFlags((QGraphicsItem.GraphicsItemFlag)(1|2|4|8))
#        self.myBtn.resize(self.myBtn.sizeHint())
#
#        self.myBtnProxy.setFlag(QGraphicsItem.ItemIsMovable, True)
#        self.myBtnProxy.setFlags((QGraphicsItem.GraphicsItemFlag)(1|2|4|8))
#        self.myBtnProxy.setParentItem(btnRect)
#
#        line = self.addLine(0,0,100,100, self.pen);
#        line.setFlag(QGraphicsItem.ItemIsMovable, True)
#        line.setFlags((QGraphicsItem.GraphicsItemFlag)(1|2|4|8))
#
#        rect = self.addRect(QRectF(100,100, 100, 100), self.pen, self.brush)
#        rect.setFlag(QGraphicsItem.ItemIsMovable, True)
#        rect.setFlags((QGraphicsItem.GraphicsItemFlag)(1|2|4|8))
#        rect.setParentItem(line)
#
#        textItem = self.addTextItem("hello!")
#        textItem.setParentItem(rect)
#        textItem.setPos(150,150)
#        textItem.setTextWidth(1)
#    #end def _drawTestItem
    
#end class AW_GraphicsView
