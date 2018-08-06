# -*- coding: utf-8 -*-
"""
Created on Mo May 28 2018

@author: xnjiang
"""
import sys
from math import *

#from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import *
from PyQt5.QtWidgets import *

from .dcGraphicsRectItem import *
from .dcGraphicsModuleItem import *
from .dcGraphicsTextItem import *
from .dcGraphicsLinkChannelItem import *
from .dcGraphicsFlyLineItem import *

#class DC_GraphicsLinkItem(DC_GraphicsRectItem):
class DC_GraphicsLinkItem(DC_GraphicsModuleItem):
    def __init__(self, module, x, y, w, h, name, color, font, direct, nChannel, bDebug, parentItem):
        super(DC_GraphicsLinkItem, self).__init__(module, x, y, w, h, name, color, font, bDebug, parentItem)
        self._initLinkItem(module, name, color, font, direct, nChannel, bDebug)

    def _initLinkItem(self, module, name, color, font, direct, nChannel, bDebug):
#        self.setContextMenuPolicy(Qt.CustomContextMenu)
#        self._initModuleItem(module, name, color, font, bDebug)
        self._initItem("LinkItem", name, module)

        self._direct = direct
        self._nChannel = nChannel
        self._bChannelLevelVisible = True
#        self._posOld = QPointF()
        self._rotateAngle = 0
        self._flowLineWidth = 5
        self._srcFlyLine = None
        self._destFlyLine = None
        self._srcFlyLineColor = Qt.blue
        self._flowLineStyle = Qt.SolidLine
#        self._srcFlyLinePen = QPen(self._srcFlyLineColor)
#        self._srcFlyLinePen.setWidth(3)
#        self._srcFlyLinePen.setStyle(Qt.DotLine)
        self._destFlyLineColor = Qt.red
#        self._destFlyLinePen = QPen(self._destFlyLineColor)
#        self._destFlyLinePen.setWidth(3)
#        self._destFlyLinePen.setStyle(Qt.DotLine)

        #link name
        self._nameItem = textItem = DC_GraphicsTextItem(name, self)
        textItem.setFont(font)
        textItem.setDefaultTextColor(color)
        self.adjustNamePos()
        
        toolTip = "Link: "+module.getFullName()
        self.setToolTip(toolTip)
        
        if bDebug:
            self.updateProxyWidgetSize()

    def getModule(self):
#        return self._module
        return self.getData()
    
    def getDirect(self):
        return self._direct
    
    def updateProxyWidget(self):
        if self._proxyWidget:
            widget = self._proxyWidget.widget()
            for channel in self.getData().getChildren():
#                hHeader = widget.horizontalHeader()
                for i in range(widget.columnCount()):
                    if widget.horizontalHeaderItem(i).text() == channel.getName():
                        bHidden = not channel.isVisible()
                        widget.setColumnHidden(i, bHidden)
                
    def updateChannelItem(self):
        if self.isDebug():
            self.updateProxyWidget()
        else:
            direct = self._direct.lower()
            nChannelVisible = 0
            linkSize = 0
            xChannel = 0
            yChannel = 0
            bFirstChannel = True
            for item in self.childItems():
                if item.isLinkChannel():
                    rect = item.rect()
                    if bFirstChannel:
                        bFirstChannel = False
                        xChannel = rect.x()
                        yChannel = rect.y()
                    if direct ==  "uptodown" or direct == "downtoup":
                        linkSize += item.getData().getW(self)
                        rect.setWidth(0)
                    else:
                        linkSize += item.getData().getH(self)
                        rect.height()
                        rect.setHeight(0)
                    if item.isVisible():
                        nChannelVisible += 1
                    else:
                        item.setRect(rect)
            
            if nChannelVisible > 0:
                channelSize = linkSize/nChannelVisible
                for item in self.childItems():
                    if item.isLinkChannel():
                        if item.isVisible():
                            rect = item.rect()
                            rect.setX(xChannel)
                            rect.setY(yChannel)
                            if direct ==  "uptodown" or direct == "downtoup":
                                rect.setWidth(channelSize)
                                xChannel += channelSize
                            else:
                                rect.setHeight(channelSize)
                                yChannel += channelSize
                            item.updateRect(direct, rect.x(), rect.y(), rect.width(), rect.height())
        
    def adjustNamePos(self):
        rect = self.rect()
        x = rect.x()
        y = rect.y()
        w = rect.width()
        h = rect.height()
        xText = x
        yText = y
        if self._bDebug == True:
            adjust = self._hotArea
            xText += adjust
            yText += adjust
        else:
            font = self._nameItem.font()
            direct = self._direct
#            rotation = 0
            if direct.lower() ==  "uptodown":
                xText += w
#                yText += h
#                rotation = 90
            elif direct.lower() == "downtoup":
                xText += w
                yText += h - QFontMetricsF(font).height()
#                rotation = -90
            elif direct.lower() == "lefttoright":
                yText -= QFontMetricsF(font).height() + 10
            elif direct.lower() == "righttoleft":
                xText += w - QFontMetricsF(font).width(self._nameItem.toPlainText())
                yText -= QFontMetricsF(font).height() + 10
#                rotation = 180
        self._nameItem.setPos(xText, yText)
    
    def adjustRectByAngle(self):
        angle = self._rotateAngle%360
        direct = "UpToDown"
        if -1 == angle//90 or 3 == angle//90:
            direct = "LeftToRight"
        elif 2 == abs(angle//90):
            direct = "DownToUp"
        elif 1 == angle//90 or -3 == angle//90:
            direct = "RightToLeft"
            
#        if self._rotateAngle%180 == 0:
#            if self._rotateAngle == 0:
#                direct = "UpToDown"
#            else:
#                direct = "DownToUp"
#        else:
#            if self._rotateAngle < 0:
#                if self._rotateAngle%270 == 90:
#                    direct = "LeftToRight"
#                else:
#                    direct = "RightToLeft"
#            else:
#                if self._rotateAngle%270 == 90:
#                    direct = "RightToLeft"
#                else:
#                    direct = "LeftToRight"
        self.setDirect(direct)
            
    def setDirect(self, direct):
        curDirect = "ToVer"
        if self._direct.lower() == "lefttoright" or self._direct.lower() == "righttoleft":
            curDirect = "ToHor"
        directChanged = False
        if self._direct.lower() != direct.lower():
            directChanged = True
        self._direct = direct;
        
        if not self._bDebug:
            linkModule = self.getModule()
            link = linkModule.getLink()
            link.setDirect(direct)
            
            toDirect = "ToVer"
            direct = direct.lower()
            if direct == "lefttoright" or direct == "righttoleft":
                toDirect = "ToHor"
            
            if directChanged:
                if curDirect != toDirect:
                    super().adjustRect(toDirect)
                rect = self.rect()
                x = rect.x()
                y = rect.y()
                w = rect.width()
                h = rect.height()
                self._module.setW(w)
                self._module.setH(h)
                xOffset = self.pen().width()
                yOffset = self.pen().width()
                for item in self.childItems():
                    if hasattr(item, "getType") and item.isLinkChannel():
                        rectItem = item.rect()
                        x0 = xItem = rectItem.x()
                        y0 = yItem = rectItem.y()
                        w0 = wItem = rectItem.width()
                        h0 = hItem = rectItem.height()
                        if curDirect != toDirect:
                            if toDirect == "ToVer":
                                xItem = x + xOffset
                                xOffset += hItem
                                wItem = h0
                                yItem = y + yOffset
                                hItem = w0
                            else:
                                yItem = y + yOffset
                                yOffset += wItem
                                hItem = w0
                                xItem = x + xOffset
                                wItem = h0
                        item.updateRect(direct, xItem, yItem, wItem, hItem)
                #adjust name pos
            self.adjustNamePos()
        self.drawFlyLine(False)
    
    def _rotate(self):
        centerPos = self.boundingRect().center()
        self.setTransformOriginPoint(centerPos)
        self._rotateAngle %= 360
#        self.setRotation(self._rotateAngle)
        #adjust link's rect and name's position
        self.adjustRectByAngle()
    
    def rotateRight90(self):
        self._rotateAngle += 90
        self._rotate()

    def rotateLeft90(self):
        self._rotateAngle -= 90
        self._rotate()
        
    def rotate180(self):
        self._rotateAngle += 180
        self._rotate()
            
    
    def setChannelLevelVisible(self, bVisible):
        self._bChannelLevelVisible = bVisible
        data = self.getData()
        if bVisible == True:
            data.setGuiDataAttr(self.parentItem(), "level_visible", "True")
        else:
            data.setGuiDataAttr(self.parentItem(), "level_visible", "False")
        for channelItem in self.childItems():
            for levelItem in channelItem.childItems():
                levelItem.setVisible(bVisible)
    
    def _showChannelLevel(self):
        self.setChannelLevelVisible(True)
        
    def _hideChannelLevel(self):
        self.setChannelLevelVisible(False)
    
    def contextMenuEvent(self, event):
#        super(DC_GraphicsLinkItem, self).contextMenuEvent(event)
        
        popMenu = QMenu()
        
        act = popMenu.addAction("Show Annotation")
        act.triggered.connect(self.showAnnotationCB)
       
        if not self.isDebug():
            if self._bChannelLevelVisible == True:
                act = popMenu.addAction("Hide Channel Level")
                act.triggered.connect(self._hideChannelLevel)
            else:
                act = popMenu.addAction("Show Channel Level")
                act.triggered.connect(self._showChannelLevel)

        if not self._isLockItemChange():
            popMenu.addSeparator()
            
            act = popMenu.addAction("Rotate Right 90")
            act.triggered.connect(self.rotateRight90)
    
            act = popMenu.addAction("Rotate Left 90")
            act.triggered.connect(self.rotateLeft90)
    
            act = popMenu.addAction("Rotate 180")
            act.triggered.connect(self.rotate180)

        self.addCommonPopupMenu(popMenu, "link")
        popMenu.exec(event.screenPos())
        
    def mousePressEvent(self, event):
        super(DC_GraphicsLinkItem, self).mousePressEvent(event)
#        self._posOld = event.pos()
        if self.flags() & QGraphicsItem.ItemIsMovable == QGraphicsItem.ItemIsMovable:
            cursorShape = Qt.ClosedHandCursor
            self.setCursorShape(cursorShape)
        self.drawFlyLine(True)

    def mouseReleaseEvent(self, event):
        super(DC_GraphicsLinkItem, self).mouseReleaseEvent(event)
        cursorShape = Qt.ArrowCursor
        self.setCursorShape(cursorShape)
#        items = self.childItems()
#        for item in items:
#            if item.isLinkChannel:
#                item.setCursorShape(cursorShape)
        self.drawFlyLine()
        
    def mouseMoveEvent(self, event):
#        modifier = event.modifiers()
#        if Qt.ControlModifier == modifier:
#            movePos = event.pos()
#            rotateAngle0 = atan(self._posOld.y()/self._posOld.x())*180/pi
#            rotateAngle1 = atan(movePos.y()/movePos.x())*180/pi
#            rotateAngle = int(rotateAngle0 - rotateAngle1)
#            self._rotateAngle += rotateAngle
##                print("rotate angle： ", rotateAngle, self._rotateAngle)
##                self._rotate()
#        else:
            super(DC_GraphicsLinkItem, self).mouseMoveEvent(event)
            
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            self.drawFlyLine(True)
#            self.scene().update()
        return super().itemChange(change, value)

    def drawFlyLine(self, bTmp=False):
        linkModule = self.getModule()
        link = linkModule.getLink()
        srcPort = link.getSrc()
        srcPortItem = None
        destPort = link.getDest()
        destPortItem = None
        items = self.scene().items()
        for item in items:
            if hasattr(item, "getType") and item.isPort():
                if item.getPort() == srcPort:
                    srcPortItem = item
                elif item.getPort() == destPort:
                    destPortItem = item
            if srcPortItem != None and destPortItem != None:
                break
        self._drawFlyLine(srcPortItem, destPortItem, bTmp)
#        self.scene().update()
        
    def _drawFlyLine(self, srcPortItem, destPortItem, bTmp):
        self.drawPortFlyLine(srcPortItem, bTmp)
        self.drawPortFlyLine(destPortItem, bTmp)
    
    def drawPortFlyLine(self, portItem, bTmp):
        if bTmp==True and self.isDebug()==False and self._isLockItemChange():
            return
        
        if portItem != None:
            posPort = self.getPortItemPos(portItem)
            xStart = posPort.x()
            yStart = posPort.y()
            posLink = self.getLinkItemPos()
            xEnd = posLink.x()
            yEnd = posLink.y()
            
            bSrc = True
            linkModule = self.getModule()
            link = linkModule.getLink()
            destPort = link.getDest()
            if portItem.getPort() == destPort:
                bSrc = False
                rect = self.rect()
                direct = self._direct
                if direct.lower() ==  "uptodown":
                    xStart = posLink.x()
                    yStart = posLink.y() + rect.height()
                elif direct.lower() == "downtoup":
                    xStart = posLink.x()
                    yStart = posLink.y() - rect.height()
                elif direct.lower() == "lefttoright":
                    xStart = posLink.x() + rect.width()
                    yStart = posLink.y()
                elif direct.lower() == "righttoleft":
                    xStart = posLink.x() - rect.width()
                    yStart = posLink.y()
                xEnd = posPort.x()
                yEnd = posPort.y()
            
            parentItem = self.parentItem()
            if bSrc:
                self._drawSrcFlyLine(xStart, yStart, xEnd, yEnd, parentItem, bTmp)
            else:
                self._drawDestFlyLine(xStart, yStart, xEnd, yEnd, parentItem, bTmp)

    def getLinkItemPos(self):
            rect = self.rect()
            x = rect.x()
            y = rect.y()
            direct = self._direct
            if direct.lower() ==  "uptodown":
                x += rect.width()/2
            elif direct.lower() == "downtoup":
                x += rect.width()/2
                y += rect.height()
            elif direct.lower() == "lefttoright":
                y += rect.height()/2
            elif direct.lower() == "righttoleft":
                x += rect.width()
                y += rect.height()/2
            posLink = self.mapToParent(x, y)
            return posLink
        
    def getPortItemPos(self, portItem):
            posRect = portItem.rect()
            x = posRect.x() + posRect.width()/2
            y = posRect.y() + posRect.height()/2
            posInModule = portItem.mapToParent(x, y)
            module = portItem.parentItem()
            posPort = module.mapToParent(posInModule)
            return posPort
        
    def _drawSrcFlyLine(self, xStart, yStart, xEnd, yEnd, parentItem, bTmp):
            if self._srcFlyLine == None:
                self._srcFlyLine = self._drawOneFlyLine(xStart, yStart, xEnd, yEnd, parentItem, bTmp)
                pen = self._srcFlyLine.pen()
                pen.setColor(self._srcFlyLineColor)
                if self.isDebug():
                    pen.setWidth(self._flowLineWidth)
                    pen.setStyle(self._flowLineStyle)
                self._srcFlyLine.setPen(pen)
            else:
                self._srcFlyLine.setLine(xStart, yStart, xEnd, yEnd)
            bShow = self._isShowFlyLine(bTmp)
            self._srcFlyLine.setVisible(bShow)
        
    def _drawDestFlyLine(self, xStart, yStart, xEnd, yEnd, parentItem, bTmp):
            if self._destFlyLine == None:
                self._destFlyLine = self._drawOneFlyLine(xStart, yStart, xEnd, yEnd, parentItem, bTmp)
                pen = self._destFlyLine.pen()
                pen.setColor(self._destFlyLineColor)
                if self.isDebug():
                    pen.setWidth(self._flowLineWidth)
                    pen.setStyle(self._flowLineStyle)
                self._destFlyLine.setPen(pen)
            else:
                self._destFlyLine.setLine(xStart, yStart, xEnd, yEnd)
            bShow = bShow = self._isShowFlyLine(bTmp)
            self._destFlyLine.setVisible(bShow)
            
    def _drawOneFlyLine(self, xStart, yStart, xEnd, yEnd, parentItem, bTmp):
        lineItem = DC_GraphicsFlyLineItem(xStart, yStart, xEnd, yEnd, parentItem)
        if parentItem == None:
            self.scene().addItem(lineItem)
        bShow = bShow = self._isShowFlyLine(bTmp)
        lineItem.setVisible(bShow)
        return lineItem

#    def boundingRect(self):
#        return super(DC_GraphicsRectItem, self).boundingRect()
    
#    def paint(self, painter, option, widget):
#        return super(DC_GraphicsRectItem, self).paint(painter, option, widget)

#end class DC_GraphicsRectItem
