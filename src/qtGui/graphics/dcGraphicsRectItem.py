# -*- coding: utf-8 -*-
"""

@author: xnjiang
"""
import os
import sys

#from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import *
from PyQt5.QtWidgets import *

from src.common.dcGlobal import *
from .dcGraphicsBaseItem import *
#from ....common.dcGlobal import *

class DC_GraphicsRectItem(QGraphicsRectItem, DC_GraphicsBaseItem):
#class DC_GraphicsRectItem(QGraphicsObject, DC_GraphicsBaseItem):

    def __init__(self, x, y, w, h, parentItem):
        super(DC_GraphicsRectItem, self).__init__(x, y, w, h, parentItem)
        self._initItem("RectItem", "", None)
        self._nameItem = None
#        super(DC_GraphicsRectItem, self).__init__(parentItem)
#        self._x = x
#        self._y = y
#        self._w = w
#        self._h = h
#        self._pen = QPen()

        self._flash = False
        self._brush = None#orignal brush
        self._flashBrush = None
#        self.startTimer(1000)

        self._timer = QTimer()
        self._timer.timeout.connect(self.updateState)
    
    def setToolTip(self, toolTip):
        self.setItemToolTip(toolTip)
        super().setToolTip(toolTip)
    
    def setCustomToolTip(self, myToolTip):
        toolTip = self.itemToolTip()+"\n\n"+str(myToolTip)
        super().setToolTip(toolTip)
        if self._nameItem:
            self._nameItem.setToolTip(toolTip)
        
    def setBrush(self, brush):
        super().setBrush(brush)
        if None == self._brush:
            self._brush = brush
    
    def setState(self, brush):
        self._flashBrush = brush
        if None != brush:
            self._timer.start(1000)
            self._flash = True
        else:
            self._timer.stop()
            self._flash = False
            self.updateState()
        
    def updateState(self):
        if self._flash == True:
            self.setBrush(self._flashBrush)
        else:
            self.setBrush(self._brush)
        self._flash = not self._flash
#        self.update()
    
    def setAnnotationData(self, data):
        self._annotation = data
    
    def showAnnotationCB(self):
        #TODO： show annotation data in dialog
        dcMainWin = dcGetMainWin()
        dlg = QDialog(dcMainWin)
        dlg.setModal(False)
        dlg.setWindowTitle("Annotation"+" - %s" % self.getName())
        dlg.resize(500, 300)
#        dlg.exec_()
        dlg.show()
    
    def copyToClipboard(self, text):
        QApplication.clipboard().setText(text)
        
    def copyNameCB(self):
        data = self.getData()
        self.copyToClipboard(data.getName())
    
    def copyFullNameCB(self):
        data = self.getData()
        self.copyToClipboard(data.getFullName())
    
    def copyToolTipCB(self):
        toolTip = self.toolTip()
        self.copyToClipboard(toolTip)
    
    def addCommonPopupMenu(self, popMenu, sType):
        if popMenu:
            popMenu.addSeparator()
            #copy name
            act = popMenu.addAction("Copy "+"Name")
            act.triggered.connect(self.copyNameCB)
            #copy fullname
            act = popMenu.addAction("Copy "+"Fullname")
            act.triggered.connect(self.copyFullNameCB)
            #copy tooltip
            act = popMenu.addAction("Copy "+"Tooltip")
            act.triggered.connect(self.copyToolTipCB)
        
    def adjustRect(self, direct):
        rect = self.rect()
        w = rect.width()
        h = rect.height()
        direct = direct.lower()
        if direct == "tover":
            if w > h:
                x = rect.x()
                y = rect.y()
                x += (w-h)/2
                y -= (w-h)/2
                w = h
                h = rect.width()
                self.setRect(x, y, w, h)
        elif direct == "tohor":
            if h > w:
                x = rect.x()
                y = rect.y()
                x -= (h-w)/2
                y += (h-w)/2
                w = h
                h = rect.width()
                self.setRect(x, y, w, h)
    
    def itemChange(self, change, value):
        parentItem = self.parentItem()
        if parentItem and hasattr(parentItem, "rect") and change == QGraphicsItem.ItemPositionChange:
#            if not self._isLockItemChange():
#                QTimer.singleShot(100, self.saveGuiData)

            rectParent = parentItem.rect()
            rect = self.boundingRect()
            xOffset = rect.x()
            yOffset = rect.y()
            posL = QPointF(value.x()+xOffset, value.y()+yOffset)
            w = rect.width()
            h = rect.height()
            posR = QPointF(posL.x()+w, posL.y()+h)
            if not rectParent.contains(posL) or not rectParent.contains(posR):
                #Keep the module inside the parent module's rect.
                posL.setX(min(rectParent.right()-w, max(posL.x(), rectParent.left())))
                posL.setY(min(rectParent.bottom()-h, max(posL.y(), rectParent.top())))
                newPos = QPointF(posL.x()-xOffset, posL.y()-yOffset)
                return newPos
        return super(DC_GraphicsRectItem, self).itemChange(change, value)
    
    def mousePressEvent(self, event):      
        if self._isLockItemChange():
            super(DC_GraphicsRectItem, self).mousePressEvent(event)
            if event.button() == Qt.LeftButton:
                event.ignore()
            modifier = event.modifiers()
            if Qt.ControlModifier != modifier:
                self.setSelected(True)
            else:
                bSelected = True
                self.setSelected(bSelected)
        else:
            super(DC_GraphicsRectItem, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton and (self.flags() & QGraphicsItem.ItemIsMovable) == QGraphicsItem.ItemIsMovable:
            cursorShape = Qt.ClosedHandCursor
            self.setCursorShape(cursorShape)
    
    def mouseReleaseEvent(self, event):
        if self._isLockItemChange():
            if event.button() == Qt.LeftButton:
                event.ignore()
            self.setSelected(True)
        else:
            super(DC_GraphicsRectItem, self).mouseReleaseEvent(event)
            chartView = self.scene().parent()
            chartView.saveDesignFile()
        cursorShape = Qt.ArrowCursor
        self.setCursorShape(cursorShape)
        if self._bGuiModified:#not self._isLockItemChange():
            self._bGuiModified = False
            QTimer.singleShot(100, self.saveGuiDataToFile)
    
    def mouseMoveEvent(self, event):
        if self._isLockItemChange():
            modifier = event.modifiers()
            if Qt.ControlModifier == modifier:
                #select item
                event.ignore()
            else:
                #move view
                event.ignore()
#                super(DC_GraphicsRectItem, self).mouseMoveEvent(event)
        else:
            self._bGuiModified = True
            super(DC_GraphicsRectItem, self).mouseMoveEvent(event)
    
    def saveGuiDataToFile(self):
        items = self.scene().selectedItems()
        for item in items:
            item.saveGuiData()
        chartView = self.scene().parent()    
        chartView.saveDesignFile()
        
    def saveGuiData(self):
        rect = self.rect()
        x = rect.x()# + pos.x()
        y = rect.y()# + pos.y()
        w = rect.width()
        h = rect.height()
        if self.isLink():
            w -= self.pen().width()*2
            h -= self.pen().width()*2

        data = self.getData()
        parentModuleItem = self.parentItem()
        if self.isPort():
            parentModuleItem = parentModuleItem.parentItem()
        data.setGuiDataAttr(parentModuleItem, "x", x)
        data.setGuiDataAttr(parentModuleItem, "y", y)
        data.setGuiDataAttr(parentModuleItem, "width", w)
        data.setGuiDataAttr(parentModuleItem, "height", h)

        pos = self.pos()
        xPos = pos.x()
        yPos = pos.y()
        data.setGuiDataAttr(parentModuleItem, "xPos", xPos)
        data.setGuiDataAttr(parentModuleItem, "yPos", yPos)
        
#        if self.isModule() or self.isLink():
#            visible = data.isVisible()
#            data.setGuiDataAttr(parentModuleItem, "visible", visible)

        if self.isPort() or self.isLink() :
            direct = data.getDirect().lower()
            data.setGuiDataAttr(parentModuleItem, "direct", direct)
                
#    def timerEvent(self, event):
#        self.flash())
#    
#    def setRect(self, x, y, w, h):
#        self._x = x
#        self._y = y
#        self._w = w
#        self._h = h
#    
#    def setRect(self, rect):
#        self._x = rect.x()
#        self._y = rect.y()
#        self._w = rect.width()
#        self._h = rect.height()
#  
#    def setPen(self, pen):
#        self._pen = pen
#    
#    def pen(self):
#        return self._pen
#        
#    def boundingRect(self):
#        penWidth = self.pen().width()
#        x = self._x
#        y = self._y
#        w = self._w
#        h = self._h
#        return QRectF(x-penWidth/2, y-penWidth/2, w+penWidth, h+penWidth)
#    
#    def rect(self):
#        x = self._x
#        y = self._y
#        w = self._w
#        h = self._h
#        return QRectF(x, y, w, h)

    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        if self.isSelected():
            color = QColor("violet")
            pen = QPen(color)
            pen.setWidth(5)
            painter.setPen(pen)
#            painter.setBrush(QBrush(color))
            x = self.rect().x()
            y = self.rect().y()
#            x = self.boundingRect().x()
#            y = self.boundingRect().y()
#            w = self.boundingRect().width()
#            h = self.boundingRect().height()
            w = self.rect().width()
            h = self.rect().height()
            painter.drawRect(x, y, w, h)
            
#end class DC_GraphicsRectItem
