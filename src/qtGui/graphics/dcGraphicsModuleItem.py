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

sys.path.append("../../")
from src.common.dcGlobal import *
#from src.common.dcGlobal import __dcApp
#from src.common.dcGlobal import dcMainWin
#global dcMainWin
        
from .dcGraphicsRectItem import *
from .dcGraphicsPortItem import *
from .dcGraphicsProxyWidget import *
from ..others.dcTableWidget import *

class DC_GraphicsModuleItem(DC_GraphicsRectItem):

    def __init__(self, module, x, y, w, h, name, color, font, bDebug, parentItem=None):
        super(DC_GraphicsModuleItem, self).__init__(x, y, w, h, parentItem)
        self.setAcceptHoverEvents(True)
        self._w = w
        self._h = h
        self._initModuleItem(module, name, color, font, bDebug)

    def getMinWidth(self):
        minW = 50
        if self._proxyWidget:
            table = self._proxyWidget.widget()
            size = table.sizeHint()
            minW = size.width()/2 + self._hotArea*2
        return minW
    
    def getMinHeight(self):
        minH = 50
        if self._proxyWidget:
            table = self._proxyWidget.widget()
            size = table.sizeHint()
            fontH = 0
            if self._nameItem:
                fontH = QFontMetricsF(self._nameItem.font()).height()
            minH = size.height()/2 + (self._hotArea*2 + fontH + 10)
            
        return minH
        
        
    def updateProxyWidgetSize(self):
        if self._proxyWidget:
            fontH = 0
            if self._nameItem:
                fontH = QFontMetricsF(self._nameItem.font()).height()
            
            rect = self.rect()
#            xWidget = rect.x() + self._hotArea
#            yWidget = rect.y() + self._hotArea + QFontMetricsF(font).height() + 10
            wWidget = rect.width() - self._hotArea*2
            hWidget = rect.height() - (self._hotArea*2 + fontH + 10)
            
            widget = self._proxyWidget.widget()
            widget.resize(wWidget, hWidget)

    def isDebug(self):
        return self._bDebug
    
    def getProxy(self):
        return self._proxyWidget
    
    def setToolTip(self, toolTip):
        super().setToolTip(toolTip)
        if self._nameItem:
            self._nameItem.setToolTip(toolTip)
        
    def _initModuleItem(self, module, name, color, font, bDebug):
        self._initItem("ModuleItem", name, module)
        self._module = module
        self._resizeMode = ""
        self._hotArea = 5.0
        self._nameItem = None
        self._bDebug = bDebug
        self._proxyWidget = None
        
        if not module.isLink():
            #moudle name
            self._nameItem = textItem = DC_GraphicsTextItem(name, self)
            textItem.setDefaultTextColor(color)
            textItem.setFont(font)
            self.setNameItem(textItem)
        toolTip = "Module: "+module.getFullName()
        self.setToolTip(toolTip)
        
        if self._bDebug:
            self._proxyWidget = proxy = DC_GraphicsProxyWidget(self, name, module)
            proxy.setParentItem(self)
            
            myTable = DC_TableWidget()
            proxy.setWidget(myTable)
 
            self.updateProxyWidgetSize()
            rect = self.boundingRect()
            xWidget = rect.x() + self._hotArea
            yWidget = rect.y() + self._hotArea + QFontMetricsF(font).height() + 10
            proxy.setPos(xWidget, yWidget)
    #end def _initModuleItem
        
    def setDebugData(self, data):
        if self.isDebug():
            proxy = self.getProxy()
            table = proxy.widget()
            #TODO: build table by data
            
    def setNameItem(self, textItem):
        self._nameItem = textItem
        self.updateNameItem()
        
    def updateNameItem(self):
        if self._nameItem != None:
            adjust = self._hotArea
            rect = self.rect()
            x = rect.x()
            y = rect.y()
            xText = x + adjust
            yText = y + adjust
            self._nameItem.setPos(xText, yText)
        
    def getModule(self):
#        return self._module
        return self.getData()
    
    def drawFlyLine(self, bTmp):
        for item in self.childItems():
            if hasattr(item, "getType") and item.isPort():
                item.drawFlyLine(bTmp, True)
                
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            self.drawFlyLine(True)
            self.scene().update()
#            for view in self.scene().views():
#                view.updateSceneRect(self.scene().rect())
        return super(DC_GraphicsModuleItem, self).itemChange(change, value)

    def _getResizePos(self, x, y):
        if self.scene().itemAt(self.mapToScene(x, y), QTransform()) != self:
            return ""
        
        adjust = self._hotArea
        rect = self.rect()#self.boundingRect()
        resizeMode = ""
        if x > (rect.left() + adjust) and x < (rect.right() - adjust) and y < (rect.bottom() + adjust) and y > (rect.bottom() - adjust):
            resizeMode = "Down"
        elif x > (rect.right() - adjust) and x < (rect.right() + adjust) and (y < rect.bottom() + adjust) and y > (rect.bottom() - adjust):
            resizeMode = "DownRight"
        elif (x > (rect.right() - adjust)) and (x < (rect.right() + adjust)) and (y < (rect.bottom() - adjust)) and (y > (rect.top() + adjust)):
            resizeMode = "Right"
        elif (x > (rect.left() - adjust)) and (x < (rect.left() + adjust)) and (y > (rect.top() - adjust)) and (y < (rect.top() + adjust)):
            resizeMode = "UpLeft"
        elif (x > (rect.left() - adjust)) and (x < (rect.left() + adjust)) and (y < (rect.bottom() - adjust)) and (y > (rect.top() + adjust)):
            resizeMode = "Left"
        elif (x > (rect.left() - adjust)) and (x < (rect.left() + adjust)) and (y < (rect.bottom() + adjust)) and (y > (rect.bottom() - adjust)):
            resizeMode = "DownLeft"
        elif (x > (rect.left() + adjust)) and (x < (rect.right() - adjust)) and (y < (rect.top() + adjust)) and (y > (rect.top() - adjust)):
            resizeMode = "Up"
        elif (x < (rect.right() + adjust)) and (x > (rect.right() - adjust)) and (y < (rect.top() + adjust)) and (y > (rect.top() - adjust)):
            resizeMode = "UpRight"
        resizeMode = self.reviseResizeMode(resizeMode)
        return resizeMode

    def reviseResizeMode(self, resizeMode):
        if not self.isDebug() and self.isLink():
            if resizeMode.startswith("Down"):
                resizeMode = "Down"
            elif resizeMode.startswith("Up"):
                resizeMode = "Up"
            else:
                resizeMode = ""
#        print(resizeMode)
        return resizeMode
        
    def _getCursorShapeByResizeMode(self, resizeMode):
        cursorShape = Qt.ArrowCursor
        if self._isLockItemChange() == False:
            if resizeMode == "Down":
                cursorShape = Qt.SizeVerCursor
            if resizeMode == "DownRight":
                cursorShape = Qt.SizeFDiagCursor
            if resizeMode == "Right":
                cursorShape = Qt.SizeHorCursor
            if resizeMode == "UpLeft":
                cursorShape = Qt.SizeFDiagCursor
            if resizeMode == "Left":
                cursorShape = Qt.SizeHorCursor
            if resizeMode == "DownLeft":
                cursorShape = Qt.SizeBDiagCursor
            if resizeMode == "Up":
                cursorShape = Qt.SizeVerCursor
            if resizeMode == "UpRight":
                cursorShape = Qt.SizeBDiagCursor
        return cursorShape
#    
#    def showAnnotationCB(self):
#        #TODO： show annotation data in dialog
#        dcMainWin = dcGetMainWin()
#        dlg = QDialog(dcMainWin)
#        dlg.setModal(False)
#        dlg.setWindowTitle("Annotation"+" - %s" % self.getName())
#        dlg.resize(500, 300)
##        dlg.exec_()
#        dlg.show()
    
    def contextMenuEvent(self, event):
#        super(DC_GraphicsModuleItem, self).contextMenuEvent(event)
#        if not self.isLink():
        popMenu = QMenu()
        act = popMenu.addAction("Show Annotation")
        act.triggered.connect(self.showAnnotationCB)
        self.addCommonPopupMenu(popMenu, "module")
        popMenu.exec(event.screenPos())
        
    def hoverEnterEvent(self, event):
        super(DC_GraphicsModuleItem, self).hoverEnterEvent(event)
        pos = event.pos()
        x = pos.x()
        y = pos.y()
        cursor = self.cursor()
        resizeMode = self._getResizePos(x, y)
        cursorShape = self._getCursorShapeByResizeMode(resizeMode)
        self.setCursorShape(cursorShape)
            
    def hoverMoveEvent(self, event):
        super(DC_GraphicsModuleItem, self).hoverMoveEvent(event)
        pos = event.pos()
        x = pos.x()
        y = pos.y()
        resizeMode = self._getResizePos(x, y)
        cursorShape = self._getCursorShapeByResizeMode(resizeMode)
        self.setCursorShape(cursorShape)

    def hoverLeaveEvent(self, event):
        super(DC_GraphicsModuleItem, self).hoverLeaveEvent(event)
        cursor = self.cursor()
        cursorShape = self._getCursorShapeByResizeMode("")
        self.setCursorShape(cursorShape)

    def mousePressEvent(self, event):
#        print(self)
        super(DC_GraphicsModuleItem, self).mousePressEvent(event)
        pos = event.pos()
        x = event.pos().x()
        y = event.pos().y()
        self._resizeMode = self._getResizePos(x, y)
        if self._resizeMode != "":
            self.setFlag(QGraphicsItem.ItemIsMovable, False)
            cursorShape = self._getCursorShapeByResizeMode(self._resizeMode)
            self.setCursorShape(cursorShape)
        else:
            self.drawFlyLine(True)
#            cursorShape = Qt.ClosedHandCursor
#            self.setCursorShape(cursorShape)
            
    def mouseReleaseEvent(self, event):
#        print(self)
        super(DC_GraphicsModuleItem, self).mouseReleaseEvent(event)
        self._resizemode = ""
#        cursorShape = Qt.ArrowCursor
#        self.setCursorShape(cursorShape)
        if not self._isLockItemChange():
            self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.drawFlyLine(False)
        
    def mouseMoveEvent(self, event):
        super(DC_GraphicsModuleItem, self).mouseMoveEvent(event)
        
        posMouse = event.scenePos()
        xMouse = posMouse.x()
        yMouse = posMouse.y()
        posMouseOld = event.lastScenePos()
        xMouseOld = posMouseOld.x()
        yMouseOld = posMouseOld.y()
        
        xOffset = 0.0
        yOffset = 0.0
        wOffset = 0.0
        hOffset = 0.0
        self.prepareGeometryChange()
        if self._resizeMode == "Down":
            hOffset = yMouse - yMouseOld
        elif self._resizeMode == "DownRight":
            wOffset = xMouse -xMouseOld
            hOffset = yMouse - yMouseOld
        elif self._resizeMode == "Right":
            wOffset = xMouse -xMouseOld
        elif self._resizeMode == "UpLeft":
            xOffset = xMouse - xMouseOld
            wOffset = xMouseOld - xMouse
            yOffset = yMouse - yMouseOld
            hOffset = yMouseOld - yMouse
        elif self._resizeMode == "Left":
            xOffset = xMouse - xMouseOld
            wOffset = xMouseOld - xMouse
        elif self._resizeMode == "DownLeft":
            xOffset = xMouse - xMouseOld
            wOffset = xMouseOld - xMouse
            hOffset = yMouse - yMouseOld
        elif self._resizeMode == "Up":
            yOffset = yMouse - yMouseOld
            hOffset = yMouseOld - yMouse
        elif self._resizeMode == "UpRight":
            wOffset = xMouse -xMouseOld
            yOffset = yMouse - yMouseOld
            hOffset = yMouseOld - yMouse
        
#        if self._resizeMode != "" and (xOffset!=0 or yOffset!=0 or wOffset!=0 or hOffset!=0):
#            self._updateItemSize(xOffset, yOffset, wOffset, hOffset)
        for item in self.scene().selectedItems():
            if item.isModule() or item.isLink():
                item._updateItemSize(self._resizeMode, xOffset, yOffset, wOffset, hOffset)
    #end def mouseMoveEvent
    
    def _updateItemSize(self, resizeMode, xOffset, yOffset, wOffset, hOffset):
        resizeMode = self.reviseResizeMode(resizeMode)
        if resizeMode == "" or (xOffset==0 and yOffset==0 and wOffset==0 and hOffset==0):
            return
        
        if self.isModule() or self.isLink():
            if self.isLink():
                xOffset = 0
                wOffset = 0
            rect = self.rect()
            w = rect.width()
            h = rect.height()
            wMin = self.getMinWidth()
            hMin = self.getMinHeight()
            w += wOffset
            h += hOffset
            if w < wMin:
                w = wMin
                xOffset = 0
                wOffset = 0
            if h < hMin:
                h = hMin
                yOffset = 0
                hOffset = 0
            rect.setWidth(w)
            rect.setHeight(h)
            self.setRect(rect)
            self.moveBy(xOffset, yOffset)
            self._adjustChildItemPos(resizeMode, xOffset, yOffset, wOffset, hOffset)
            self.update()
#            if not self._isLockItemChange():
#                QTimer.singleShot(100, self.saveGuiData)
        
    def _adjustChildItemPos(self, resizeMode, xOffset, yOffset, wOffset, hOffset):
        items = self.childItems()
        for item in items:
            if hasattr(item, "getType"):
                if item.isPort():
                    self._adjustPortPos(item, resizeMode, xOffset, yOffset, wOffset, hOffset)
                elif item.isModule() or item.isLink():
                    self._adjustChildModuleItemPos(item, resizeMode, xOffset, yOffset, wOffset, hOffset)
                elif item.isProxyWidget():
                    self._adjustChildProxyWidgetSize(item, xOffset, yOffset, wOffset, hOffset)
                elif item.isLinkChannel():
                    self._adjustChannelItemSize(item, xOffset, yOffset, wOffset, hOffset)
    
    def _adjustChildProxyWidgetSize(self, item, xOffset, yOffset, wOffset, hOffset):
        if hasattr(item, "getType") and item.isProxyWidget():
             self.updateProxyWidgetSize()
            
    def _adjustChannelItemSize(self, item, xOffset, yOffset, wOffset, hOffset):
        if hasattr(item, "getType") and item.isLinkChannel():
            rect = item.rect()
            h = rect.height()
            h += hOffset
            rect.setHeight(h)
            item.updateRect(self.getDirect(), rect.x(), rect.y(), rect.width(), rect.height())
             
    def _adjustChildModuleItemPos(self, item, resizeMode, xOffset, yOffset, wOffset, hOffset):
        if hasattr(item, "getType") and (item.isModule() or item.isLink()):
            moduleRect = item.rect()
            xModule = moduleRect.x()
            yModule = moduleRect.y()
            wModule = moduleRect.width()
            hModule = moduleRect.height()
            if resizeMode == "Left" or resizeMode == "UpLeft" or resizeMode == "DownLeft":
                item.moveBy(wOffset, 0)
            if resizeMode == "Up" or resizeMode == "UpLeft" or resizeMode == "UpRight":
                item.moveBy(0, hOffset)
            
    def getPortPos(self, portItem):
        pos = ""
        if hasattr(portItem, "getType") and portItem.isPort():
            moduleRect = self.rect()
            xModule = moduleRect.x()
            yModule = moduleRect.y()
            wModule = moduleRect.width()
            hModule = moduleRect.height()
            portRect = portItem.rect()
            xPort = portRect.x() + portItem.pos().x()
            yPort = portRect.y() + portItem.pos().y()
            wPort = portRect.width()
            hPort = portRect.height()
            
            if xPort+wPort/2 == xModule and yPort+hPort/2 == yModule:
                pos = "UpLeft"
            elif xPort+wPort/2 == xModule+wModule and yPort+hPort/2 == yModule:
                pos = "UpRight"
            elif xPort+wPort/2 == xModule and yPort+hPort/2 == yModule+hModule:
                pos = "DownLeft"
            elif xPort+wPort/2 == xModule+wModule and yPort+hPort/2 == yModule+hModule:
                pos = "DownRight"
            elif xPort+wPort/2 <= xModule and xPort <= xModule:
                pos = "Left"
            elif yPort+hPort/2 <= yModule and yPort <= yModule:
                pos = "Up"
            elif xPort+wPort/2+5 >= xModule+wModule and xPort <= xModule+wModule:
                pos = "Right"
            elif yPort+hPort/2+5 >= yModule+hModule and yPort <= yModule+hModule:
                pos = "Down"
        return pos
                
    def getPortArea(self, portItem):
        portPos = ""
        if hasattr(portItem, "getType") and portItem.isPort():
            moduleRect = self.rect()
            xModule = moduleRect.x()
            yModule = moduleRect.y()
            wModule = moduleRect.width()
            hModule = moduleRect.height()
            portRect = portItem.rect()
            xPort = portRect.x() + portItem.pos().x()
            yPort = portRect.y() + portItem.pos().y()
            wPort = portRect.width()
            hPort = portRect.height()
            
            pos = 0
            if yPort+hPort <= yModule+hModule/2:
                pos |= 1
            if yPort >= yModule+hModule/2:
                pos |= 2
            if xPort+wPort <= xModule+wModule/2:
                pos |= 4
            if xPort >= xModule+wModule/2:
                pos |= 8
            
            if pos&1 == 1 and pos&4==4:
                portPos = "UpLeft"
            elif pos&1==1 and pos&8==8:
                portPos = "UpRight"
            elif pos&2==2 and pos&4==4:
                portPos = "DownLeft"
            elif pos&2==2 and pos&8==8:
                portPos = "DownRight"
            elif pos == 1:
                portPos = "Up"
            elif pos == 2:
                portPos = "Down"
            elif pos == 4:
                portPos = "Left"
            elif pos == 8:
                portPos = "Right"
        return portPos
    
    def _adjustPortPos(self, item, resizeMode, xOffset, yOffset, wOffset, hOffset):
        if hasattr(item, "getType") and item.isPort():
            portArea = self.getPortArea(item)
            portPos = self.getPortPos(item)
            moduleRect = self.boundingRect()
            xModule = moduleRect.x()
            yModule = moduleRect.y()
            wModule = moduleRect.width()
            hModule = moduleRect.height()
            portRect = item.rect()
            xPort = portRect.x() + item.pos().x()
            yPort = portRect.y() + item.pos().y()
            wPort = portRect.width()
            hPort = portRect.height()
            if resizeMode == "Down" or resizeMode == "DownLeft" or resizeMode == "DownRight":
                if portPos == "Down":
                    item.moveBy(0, hOffset)
                elif (portPos == "Left" or portPos == "Right") and (yPort+hPort >= yModule+hModule):
                    item.moveBy(0, hOffset)
                elif portPos=="" and portArea.count("Down"):
                    item.moveBy(0, hOffset)
            if resizeMode == "Right" or resizeMode == "UpRight" or resizeMode == "DownRight":
                if portPos  == "Right":
                    item.moveBy(wOffset, 0)
                elif (portPos == "Up" or portPos == "Down") and (xPort+wPort/2 > xModule+wModule):
                    item.moveBy(wOffset, 0)
                elif portPos=="" and portArea.count("Right"):
                    item.moveBy(wOffset, 0)
            if resizeMode == "Left" or resizeMode == "UpLeft" or resizeMode == "DownLeft":
                if portPos != "Left":
                    adjust = 0
                    if portPos != "Right" and (portPos == "Up" or portPos == "Down"):
                        if xPort+wOffset < xModule:
                            adjust = xModule - xPort - wOffset
                    if portPos != "" or portArea.count("Left") == 0:
                        item.moveBy(wOffset+adjust, 0)
            if resizeMode == "Up" or resizeMode == "UpLeft" or resizeMode == "UpRight":
                if portPos != "Up":
                    adjust = 0
                    if portPos != "Down" and (portPos == "Left" or portPos == "Right"):
                        if yPort+hOffset < yModule:
                            adjust = yModule - yPort - hOffset
                    if portPos != "" or portArea.count("Up") == 0:
                        item.moveBy(0, hOffset+adjust)
            item.adjustRect()
                
#    def boundingRect(self):
#        rect = super(DC_GraphicsRectItem, self).boundingRect()
#        x = rect.x()
#        y = rect.y()
#        w = rect.width()
#        h = rect.height()
#        rect1 = QRectF(x-self._hotArea, y-self._hotArea, w+self._hotArea*2, h+self._hotArea*2)
#        return rect1
    
    
#    def paint(self, painter, option, widget):
#        return super(DC_GraphicsRectItem, self).paint(painter, option, widget)

#end class DC_GraphicsRectItem
