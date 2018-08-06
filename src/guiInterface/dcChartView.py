# -*- coding: utf-8 -*-
"""
Created on Mo May 28 2018

@author: xnjiang
"""
import os
import sys
from math import sqrt
from math import ceil

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import *
from PyQt5.QtWidgets import *

from ..common.dcGlobal import *
from ..qtGui.graphics.dcGraphicsView import *
from ..qtGui.graphics.dcGraphicsScene import *
from ..qtGui.others.dcDockWidget import *

#class DC_ChartView(QMainWindow):
class DC_ChartView(DC_DockWidget):

    def __init__(self, view, design, sType):
        super(DC_ChartView, self).__init__(view, sType+"'s chart")
        self._view = view
        self._design = design
        self.initChartView()

        self.setTitleBarWidget(QWidget())
        self.setAllowedAreas(Qt.RightDockWidgetArea)

        self._frameMainWin = QMainWindow()
        #chart toolbar
        graphicToolbar = self._frameMainWin.addToolBar("")
#        graphicToolbar.setFloatable(False)
#        graphicToolbar.setAllowedAreas(Qt.TopToolBarArea)
        graphicToolbar.setMovable(False)
        
        zoomFitAct = graphicToolbar.addAction("Zoom Fit")
        zoomFitAct.triggered.connect(self._zoomFitCB)
        
        self._flyLineCheckBox = QCheckBox("Show Fly Line")
        if self.isDebug():
            self._flyLineCheckBox.setText("Show Flow Line")
        self._flyLineCheckBoxAct = graphicToolbar.addWidget(self._flyLineCheckBox)
        self._flyLineCheckBox.stateChanged.connect(self._showFlyLineCB)
        
        self._lockCheckBox = QCheckBox("Lock")
        self._lockCheckBoxAct = graphicToolbar.addWidget(self._lockCheckBox)
#        self._lockCheckBox.setChecked(True)
        self._lockCheckBox.stateChanged.connect(self._lockItemPos)

#        self._saveAct = graphicToolbar.addAction("Save")
#        self._saveAct.triggered.connect(self.saveGui)
        
        #desgin graphic
        fileName = design.getFile()
        toolTip = os.path.abspath(fileName)
        self._graphic = DC_GraphicsView()
        self._graphic.setToolTip(toolTip)
        self._scene = DC_GraphicsScene(self)
        self._scene.setToolTip(toolTip)
#        self._scene.setBackgroundBrush(QColor("lightgray"))
#        self._scene.setBackgroundBrush(QBrush(Qt.black, Qt.Dense1Pattern))
        self._scene.setBackgroundBrush(QColor("black"))
        self._graphic.setScene(self._scene)
        self._frameMainWin.setCentralWidget(self._graphic)
        
        self.setWidget(self._frameMainWin)
        self.topItem = None
    #end def __init__
    
    def getDesign(self):
        return self._design
    
    def isDebug(self):
        return self._design.isDebug()
        
    def initChartView(self):
        self._rowCnt = 0
        self._colsW = {}
        
#        self._tableMinW = 500
#        self._tableMinH = 300
        self._moduleContentsMargin = 10.0
        self._moduleChannelSpace = 30.0

        self._linePen = QPen(Qt.black)
        self._linePen.setWidth(3)
        #module
        self._moduleFont = QApplication.font()
        self._moduleFont.setPointSize(12)
        self._modulePen = QPen(QColor("black"))
        self._modulePen.setWidth(3)
        self._modulePenDebug = QPen(QColor("lightgray"))
        self._modulePenDebug.setWidth(3)
        self._moduleBrush = QBrush(QColor("#d0d0d0d0"))
        self._moduleTextColor = QColor("black")
        #port
        self._portFont = QApplication.font()
        self._portFont.setPointSize(10)
        self._portPen = QPen(QColor("gray"))
        self._portPen.setWidth(3)
        self._portPenOutput = self._portPen
        self._portPenDebug = QPen(QColor("gray"))
        self._portPenDebug.setWidth(3)
        self._portPenInput = self._portPenDebug
        self._portOutputBrush = QBrush(QColor("lightblue"))
        self._portInputBrush = QBrush(QColor("dodgerblue"))
        self._portTextColor = QColor("black")
        #link
        self._linkFont = QApplication.font()
        self._linkFont.setPointSize(12)
        self._linkPen = QPen(Qt.black)
        self._linkPen.setWidth(2)
        self._linkPenDebug = QPen(QColor("skyblue"))
        self._linkPenDebug.setWidth(3)
        self._linkBrush = QBrush(QColor("black"))
        self._linkBrushDebug = QBrush(QColor("skyblue"))
        self._linkTextColor = QColor("black")
        #link channel
        self._linkChannelFont = QApplication.font()
        self._linkChannelFont.setPointSize(5)#####
        self._linkChannelPen = QPen(Qt.black)
        self._linkChannelPen.setWidth(1)
        self._linkChannelBrush = QBrush(QColor("skyblue"))
#        self._linkChannelBrush = QBrush(QColor("#d0d0d0d0"))
        self._linkChannelColor = QColor("black")
    #end def initChartView

    def selectDesignItem(self, item, hasFocus):
        if hasattr(item, "getData"):
            self._view.selectDesignItem(item.getData(), hasFocus)
        
    def setColorOfState(self, state, color):
        sState = state.lower()
        if "standby" == sState:
            standbyColor = color
        if "ready" == sState:
            readyColor = color
        if "busy" == sState:
            busyColor = color
        if "fail" == sState:
            failColor = color
        if "pass" == sState:
            passColor = color
            
    def getColorForState(self, state):
        color = ""
        sState = state.lower()
        if "standby" == sState:
            color = standbyColor
        if "ready" == sState:
            color = readyColor
        if "busy" == sState:
            color = busyColor
        if "fail" == sState:
            color = failColor
        if "pass" == sState:
            color = passColor
        return color
    
    def setItemData(self, dataType, designObj, data, level=-1):
        if designObj == None:
            return
        items = self._scene.items()
        if designObj.isChannel() and self.isDebug():
            linkObj = designObj.parent()
            for item in items:
                if hasattr(item, "getData") and linkObj == item.getData() and item.isLink():
                    item.updateChannelItem()
        else:
            for item in items:
                if hasattr(item, "getData") and designObj == item.getData():
                    if dataType == "ItemState":
                        brush = None
                        color = self.getColorForState(data)
                        if "" != color:
                            brush = QBrush(QColor(color))
                            item.setState(brush)
                    elif dataType == "DebugData":
                        if item.isModule() or item.isLink():
                            item.setDebugData(data)
                    elif dataType == "Annotation":
                        if item.isModule() or item.isLink() or item.isPort():
                            item.setAnnotationData(data)
                    elif dataType == "ToolTip":
                        item.setCustomToolTip(data)
                    elif dataType == "ItemVisible":
                        item.setVisible(data)
                        if item.isLink():
                            item.updateChannelItem()
                        elif item.isLinkChannel():
                            linkItem = item.parentItem()
                            linkItem.updateChannelItem()
                    elif dataType == "ItemSelected":
                        self._scene.clearSelection()
                        self._graphic.ensureVisible(item)
    #                    item.setSelected(data)
                        self._scene.selectItem(item, True)
        
    def setItemState(self, designObj, state, level=-1):#level: -1 -- for channel's all level
        self.setItemData("ItemState", designObj, state, level)

    def setItemDebugData(self, designObj, data):
        self.setItemData("DebugData", designObj, data)
    
    def setItemAnnotation(self, designObj, data):
        self.setItemData("Annotation", designObj, data)
    
    def setItemToolTip(self, designObj, data):
        self.setItemData("ToolTip", designObj, data)
        
    def setItemVisible(self, designObj, bVisible):
        self.setItemData("ItemVisible", designObj, bVisible)
        self.saveDesignFile()

    def setItemSelected(self, designObj, bSelected):
        self.setItemData("ItemSelected", designObj, bSelected)
        
    def saveGuiData(self):
        items = self._scene.items()
        for item in items:
            if hasattr(item, "getData") and (item.isModule() or item.isLink() or item.isPort()):
                item.saveGuiData()
    
#    def saveGui(self, file=""):
#        self.saveGuiData()
#        self.saveDesignToFile(file)
    
    def saveDesignFile(self):
        tmpName = "~"+os.path.basename(self.getDesign().getName())
#        nameL = self.getDesign().getName().rsplit('.', 1)
#        tmpName = nameL[0]+"~"
#        if len(nameL)>1:
#            tmpName += "."+nameL[1]
        file = os.path.abspath(tmpName)
        self.saveDesignToFile(file)
        self.getDesign().setGuiModified(True)
        
    def saveDesignToFile(self, file=None):
        if self._view:
            self._view.saveDesignToFile(file)
        else:
            if not file:
                tmpName = "~"+os.path.basename(self.getDesign().getName())
                file = os.path.abspath(tmpName)
            self._design.saveToFile(file)

    def isShowFlyLine(self):
        bVisible = False
        if self._flyLineCheckBox.isChecked():
            bVisible = True
        return bVisible
    
    def isLockItemChange(self):
        bLock = False
        if self._lockCheckBox.isChecked():
            bLock = True
        return bLock
    
    def _lockItemPos(self, checked):
        items = self._scene.items()
        for item in items:
            if hasattr(item, "getType"):
                if item.isModule() or item.isLink() or item.isPort():
                    item.setFlag(QGraphicsItem.ItemIsMovable, not checked)
        
    def _showFlyLineCB(self, checked):
        self._graphic.drawFlyLine()
    
    def _zoomFitCB(self):
        self.zoomFit()
        
    def zoomFit(self):
        w = w0 = self._graphic.width()
        h = h0 = self._graphic.height()
#        w1 = self._scene.sceneRect().width()
#        if w > w1:
#            w = w1
#        h1 = self._scene.sceneRect().height()
#        if h > h1:
#            h = h1
        self._graphic.fitInView(0, 0, w, h)
#        self._graphic.fitInView(0, 0, self._graphic.width(), self._graphic.height())
    
    def adjustSceneRect(self, topItem):
        self.topItem = topItem
        rect = self._scene.itemsBoundingRect()
        marginMin = 40
        x = rect.x()
        y = rect.y()
        w = rect.width()
        h = rect.height()
        w1 = self._graphic.width()
        h1 = self._graphic.height()
        wMargin = (w1 - w)/2
        if wMargin < marginMin:
            if wMargin < 0:
                wMargin = marginMin
            else:
                wMargin = marginMin - wMargin
        hMargin = (h1 -h)/2
        if hMargin < marginMin:
            if hMargin < 0:
                hMargin = marginMin
            else:
                hMargin = marginMin -hMargin 
        self._scene.setSceneRect(x, y, w+wMargin*2, h+hMargin*2)
#        self._scene.setSceneRect(x, y, w, h)
        self.topItem.moveBy(wMargin, hMargin)
        QApplication.processEvents()
#        if topItem:
#            topItem.moveBy(marginMin, marginMin)
        QTimer.singleShot(100, self.zoomFit)
        
    def clearChart(self):
        self._scene.clear()
        
    def drawDebugChart(self):
        self._scene.clear()
        
        top = self._design.getTopModule()
        x = 0.0
        y = 0.0
        self.drawDebugScope(x, y, self._design.getTopModule())
 
    def drawDebugModule(self, level, x, y, module, parentItem, bDrawPort=True):
        item = None
        if module.isLink():
            item = self.drawLink(level, x, y, module, "UpToDown", True, parentItem)
        else:
            item = self.drawModule(level, x, y, module, True, parentItem, bDrawPort)
        return item
    
    def drawDebugScope(self, x, y, module):
        if module.isLink() == False:
            level = 0
            item = self._scene.addDummyItem(None)
            
            channelSpace = module.getChannelSpace()#self._moduleChannelSpace
            childItem = None
            textH = QFontMetricsF(self._moduleFont).height()
            xChild = x0 = x1 = x + self._moduleContentsMargin + channelSpace
            yChild = y0 = y + textH + self._moduleContentsMargin + channelSpace

            childModules = module.getChildren()
            childModules.sort(key=self.getPortCnt, reverse=True)
            nChild = len(childModules)
            nCol = ceil(sqrt(nChild))
            i = 0
            hasGuiData = False
            for childModule in childModules:
                hasGuiData = childModule.hasGuiData(item)
                childItem = self.drawDebugModule(level+1,xChild, yChild, childModule, item)
#                childItem.move(childModule.x(), childModule.y())
                rect = childItem.boundingRect()
                xChild += rect.width() + channelSpace #+ self._moduleContentsMargin
                i += 1
                if i%nCol == 0:
                    if xChild >= x1:
                        x1 = xChild
                        xChild = x0
                        yChild += rect.height() + channelSpace
                    else:
                        i -= 1
                        
            self._flyLineCheckBox.setChecked(True)
            self.adjustSceneRect(item)
    #end def _drawModuleDebug
    
    def drawDesignChart(self):
        self._scene.clear()
        
        top = self._design.getTopModule()
        x = 0.0
        y = 0.0
        self.drawModuleScope(x, y, self._design.getTopModule())
 
    def getPortCnt(self, module):
        return module.getPortCnt()
    
    def drawModuleScope(self, x, y, module):
        level = 0
        item = self.drawModule(level, x, y, module, False, None, False)
        if module.isLink() == False:
            rect = item.rect()
            x = rect.x()
            y = rect.y()
            
            childModules = module.getChildren()
            nChild = len(childModules)
            nCol = ceil(sqrt(nChild))
            
            channelSpace = module.getChannelSpace()#self._moduleChannelSpace
            childItem = None
            textH = QFontMetricsF(self._moduleFont).height()
            xChild = x0 = x1 = x + self._moduleContentsMargin + channelSpace
            yChild = y0 = y + textH + self._moduleContentsMargin + channelSpace
            childModules.sort(key=self.getPortCnt, reverse=True)
            i = 0
            for childModule in childModules:
                childItem = self.drawModule(level+1,xChild, yChild, childModule, False, item)
#                childItem.move(childModule.x(), childModule.y())
                rect = childItem.boundingRect()
                xChild += rect.width() + channelSpace #+ self._moduleContentsMargin
                i += 1
                if i%nCol == 0:
                    if xChild >= x1:
                        x1 = xChild
                        xChild = x0
                        yChild += rect.height() + channelSpace
                    else:
                        i -= 1

#        self._flyLineCheckBox.setChecked(True)
#        if module.hasGuiData(None):
#            self._flyLineCheckBox.setChecked(False)
        self._graphic.drawFlyLine()
                
        #adjust module rect size
        rect0 = item.boundingRect()
        w0 = rect0.width()
        h0 = rect0.height()
        rect1 = item.childrenBoundingRect()
        w1 = rect1.width()
        h1 = rect1.height()
        x1 = rect1.x()
        y1 = rect1.y()
        rect0.setX(x1)
        rect0.setY(y1)
        if w0 < w1:
            w0 = w1 + self._moduleContentsMargin*1 + channelSpace*1
            rect0.setWidth(w0)
            module.setW(w0)
        if h0 < h1:
            h0 = h1 + self._moduleContentsMargin*1 + channelSpace*1
            rect0.setHeight(h0)
            module.setH(h0)
        item.setRect(rect0)
        item.updateNameItem()
        
        self.drawModulePort(x1, y1, module,item)
        
        self.adjustSceneRect(item)
    #end def _drawModuleScope
    
    def drawLinkConnection(self, link, direct="UpToDown"):
        if link == None or link.isLink() == False:
            return

#        parentItem = self.addGroupItem(None)
        parentItem = self._scene.addDummyItem(None)
        
        level = 0
        x = 0
        y = 0
#        parentModule = link.parent()
#        topModuleItem = self.drawModule(level, x, y, parentModule, False, None, True)
#        parentItem = topModuleItem
#        level += 1
        
        linkItem = self.drawLink(level, x, y, link, direct.lower(), False, parentItem)
#        linkItem = link.getGraphicsItem()
#        parentItem.addToGroup(linkItem)

        
        srcPort = link.getLink().getSrc()
        srcModule = srcPort.getModule()
        srcModuleItem = self.drawModule(level, x, y, srcModule, False, parentItem, True)
#        parentItem.addToGroup(srcModuleItem)
        
        destPort = link.getLink().getDest()
        destModule= destPort.getModule()
        destModuleItem = self.drawModule(level, x, y, destModule, False, parentItem, True)
#        parentItem.addToGroup(destModuleItem)
        
#        self._flyLineCheckBox.setChecked(True)
#        if link.hasGuiData(parentItem):
#            self._flyLineCheckBox.setChecked(False)
        self._graphic.drawFlyLine()
        
        self._scene.setBackgroundBrush(QColor("lightgray"))
        self.adjustSceneRect(parentItem)
#end def drawLinkConnection
        

    #for sorting ports by name
    def _getPortName(self, port):
        return port.getName()
    
    def drawModulePort(self, x, y, module, moduleItem):
        if len(module.getPorts()) == 0:
            return
        
        moduleNameW = QFontMetricsF(self._moduleFont).width(module.getName())
        xPort = x + moduleNameW
        yPort = y
        w = module.getW(moduleItem.parentItem()) - moduleNameW
        h = module.getH(moduleItem.parentItem())
        
        #input
        nPort = module.getInputCnt()
        if nPort > 0:
            nCnt = 0
            nUpPort = module.getInputUpCnt()
            nLeftPort = module.getInputLeftCnt()
            ports = list(module.getPorts().values())
            ports.sort(key=self._getPortName)
            for i, port in enumerate(ports):
                if port.isInput():
                    nCnt += 1
                    portItem = self.drawPort(port, xPort+w/(nUpPort+1)*nCnt-port.getW()/2, yPort-port.getH()/2, "up", moduleItem)
#                    portItem.move(port.x(), port.y())
#                    if nUpPort > nCnt:#up
#                        nCnt += 1
#                        portItem = self.drawPort(xPort+w/(nUpPort+1)*nCnt-port.getW()/2, y-port.getH()/2, port, "up", moduleItem)
#                    else:#left
#                        nCnt += 1
#                        portItem = self.drawPort(x-port.getW()/2, y+h/(nLeftPort+1)*(nCnt-nUpPort)-port.getH()/2, port, "left", moduleItem)

        #output
        nPort = module.getOutputCnt()
        if nPort > 0:
            nCnt = 0
            nDownPort = module.getOutputDownCnt()
            nRightPort = module.getOutputRightCnt()
            ports = list(module.getPorts().values())
            ports.sort(key=self._getPortName)
            for i, port in enumerate(ports):
                if port.isOutput():
                    nCnt += 1
                    portItem = self.drawPort(port, xPort+w/(nDownPort+1)*nCnt-port.getW()/2, yPort+h-port.getH()/2, "down", moduleItem)
#                    portItem.move(port.x(), port.y())
#                    if nDownPort > nCnt:#down
#                        nCnt += 1
#                        portItem = self.drawPort(x+w/(nDownPort+1)*nCnt-port.getW()/2, y+h-port.getH()/2, port, "down", moduleItem)
#                    else:#right
#                        nCnt += 1
#                        portItem = self.drawPort(x+w-port.getW()/2, y+h/(nRightPort+1)*(nCnt-nDownPort)-port.getW()/2, port, "right", moduleItem)
    #end def drawModulePort
    
    def drawPort(self, port, x, y, pos, moduleItem):
#        guiData = port.getGuiData(moduleItem.parentItem())
#        if len(guiData):
        if port.hasGuiData(moduleItem.parentItem()):
            x = port.x(moduleItem.parentItem())#float(guiData.get("x", x))
            y = port.y(moduleItem.parentItem())#float(guiData.get("y", y))
        w = port.getW()
        h = port.getH()
        name = port.getName()
        portItem = self.drawPortItem(port, x, y, w, h, name, pos.lower(), moduleItem)
        port.setGraphicsItem(portItem)
        if port.hasGuiData(moduleItem.parentItem()):
            xPos = port.xPos(moduleItem.parentItem())#float(guiData.get("xPos",0))
            yPos = port.yPos(moduleItem.parentItem())#float(guiData.get("yPos", 0))
            portItem.setPos(xPos,yPos)
            portItem.adjustNamePos()
        return portItem
        
    def drawModule(self, level, x, y, module, bDebug, parentItem, bDrawPort=True):
        if module.hasGuiData(parentItem):
            self._lockCheckBox.setChecked(True)
            
        if module.isLink():#link module
            return self.drawLink(level, x, y, module, "UpToDown", bDebug, parentItem)
            
#        guiData = module.getGuiData(parentItem)
#        if len(guiData):
        if module.hasGuiData(parentItem):
            x = module.x(parentItem)#float(guiData.get("x", x))
            y = module.y(parentItem)#float(guiData.get("y", y))

        w = module.getW(parentItem)
        h = module.getH(parentItem)
#        if bDebug:
#            if w < self._tableMinW:
#                w = self._tableMinW
#            if h < self._tableMinH:
#                h = self._tableMinH
        name = module.getName()
        moduleItem = self.drawModuleItem(level, module, x, y, w, h, name, bDebug, parentItem)
#        if len(guiData):
        if module.hasGuiData(parentItem):
            xPos = module.xPos(parentItem)#float(guiData.get("xPos",0))
            yPos = module.yPos(parentItem)#float(guiData.get("yPos", 0))
            moduleItem.setPos(xPos,yPos)
#        item.setTransformOriginPoint(x, y)
        
        #module port
        if bDrawPort:
            self.drawModulePort(x, y, module, moduleItem)
        
        module.setGraphicsItem(moduleItem)
        return moduleItem
    
    def drawLink(self, level, x, y, link, direct, bDebug, parentItem):
        linkW = 0
        channels = link.getChildren()
        nChannel = len(channels)
        for channel in channels:
            linkW += channel.getW(parentItem)
        linkH = link.getH(parentItem)
        if bDebug:
            linkW = link.getW(parentItem)
#            if linkW < self._tableMinW:
#                linkW = self._tableMinW
#            if linkH < self._tableMinH:
#                linkH = self._tableMinH
                
        if link.hasGuiData(parentItem):
            x = link.x(parentItem)
            y = link.y(parentItem)
        linkName = link.getName()
        direct = link.getDirect(parentItem)
        linkItem = self.drawLinkItem(level, link, x, y, linkW, linkH, linkName, direct, nChannel, bDebug, parentItem)
        if link.hasGuiData(parentItem):
            xPos = link.xPos(parentItem)
            yPos = link.yPos(parentItem)
            linkItem.setPos(xPos,yPos)
            linkItem.adjustNamePos()
            
        return linkItem
    #end def drawLink
    
    def _drawLinkChannel(self, col, channel, x, y, w, h, name, direct, linkItem, bDebug, brush, color):
#        w = channel.getW(linkItem)
        channelItem = None
        nLevel = channel.getChannelLevel()
        if bDebug:
            proxy = linkItem.getProxy()
            table = proxy.widget()           
            nRow = table.rowCount()
            if nLevel > nRow:
                table.setRowCount(nLevel)
            for row in range(nLevel):
                tableItem = QTableWidgetItem("level: "+str(row+1))
                table.setItem(row,col,tableItem);
                tableItem.setToolTip("      Level: "+str(row+1)+"\n"+"Channel: "+name+"\n    Levels: "+str(nLevel)+"\n       "+linkItem.toolTip())
        else:
            channelItem = self.drawLinkChannelItem(channel, x, y, w, h, name, direct.lower(), nLevel, linkItem, brush, color)
        return channelItem
    

    def drawModuleItem(self, level, module, x, y, w, h, name, bDebug, parentItem=None):
        pen = self._modulePen
        if bDebug:
            pen = self._modulePenDebug
        brush = self._moduleBrush
        val = 15 - level*2
        color = "#%x0%x0%x0"%(val, val, val)
        brush =QBrush(QColor(color))
        color = self._moduleTextColor
        font = self._moduleFont
        item = self._scene.addModuleItem(module, x, y, w, h, name, bDebug, parentItem, pen, brush, color, font)
        
        bVisible = module.isVisible()#True
#        guiData = module.getGuiData(parentItem)
#        visible = guiData.get("visible")
#        if visible and len(visible):
#            if visible.lower() == "false":
#                bVisible = False
        item.setVisible(bVisible)
        return item
 
    def drawPortItem(self, port, x, y, w, h, name, pos, moduleItem):
        pen = self._portPenOutput
#        if moduleItem.isDebug():
#            pen = self._portPenDebug
        brush = self._portOutputBrush
        if port.isInput():
            pen = self._portPenInput
            brush = self._portInputBrush
        color = self._portTextColor
        font = self._portFont
        textColor = self._portTextColor
        item = self._scene.addPortItem(port, x, y, w, h, name, moduleItem, pos.lower(), pen, brush, color, font)
        return item
    
    def drawLinkItem(self, level, link, x, y, w, h, name, direct, nChannel, bDebug, parentItem=None):
        pen = self._linkPen
        brush = self._linkBrush
        if bDebug:
            pen = self._linkPenDebug
            brush = self._linkBrushDebug
#        val = 15 - level*2
#        color = "#%x0%x0%x0"%(val, val, val)
#        brush =QBrush(QColor(color))
        color = self._linkTextColor
        font = self._linkFont
#        direct = "UpToDown"
        newDirect = link.getDirect(parentItem)
        if newDirect and newDirect != direct:
            direct = newDirect
        penW = pen.widthF()
        item = self._scene.addLinkItem(link, x, y, w+penW*2, h+penW*2, name, direct, nChannel, bDebug, parentItem, pen, brush, color, font)
        
        channels = link.getChildren()
        sHeaderL = []
        if bDebug == True:
            proxy = item.getProxy()
            table = proxy.widget()
            table.setColumnCount(len(channels))

        rect = item.rect()
        xChannel = rect.x()+penW
        yChannel = rect.y()+penW
#        isHor = False
#        if direct.lower() == "lefttoright" or direct.lower() == "righttoleft":
#            isHor = True
        wChannel = w/len(channels)
        for i, channel in enumerate(channels):
#                hChannel = rect.height()
#            wChannel = channel.getW(item)
            hChannel = channel.getH(item)
#                if isHor:
#                    hChannel = channel.getW()
#                    wChannel = rect.width()
            channelName = channel.getName()
            brush = self._linkChannelBrush
            color = self._linkChannelColor
            channelItem = self._drawLinkChannel(i, channel, xChannel, yChannel, wChannel, hChannel, channelName, direct, item, bDebug, brush, color)
            xChannel += wChannel
#            if channelItem:
#                xChannel += channelItem.boundingRect().width()
            channel.setGraphicsItem(channelItem)
            if bDebug:
                sHeaderL.append(channel.getName())
        else:
            if bDebug:
                proxy = item.getProxy()
                table = proxy.widget()
                table.setHorizontalHeaderLabels(sHeaderL)
        
        bLevelVisible = False
        if link.hasGuiData(parentItem):
            guiData = link.getGuiData(parentItem)
            levelVisible = guiData.get("level_visible")
            if levelVisible and len(levelVisible):
                if levelVisible.lower() == "true":
                    bLevelVisible = True
            
            bVisible = True
            visible = guiData.get("visible")
            if visible and len(visible):
                if visible.lower() == "false":
                    bVisible = False
            item.setVisible(bVisible)
            
        item.updateChannelItem()
        item.setChannelLevelVisible(bLevelVisible)
        return item

    def drawLinkChannelItem(self, channel, x, y, w, h, name, direct, nLevel, linkItem, brush, color):
        pen = self._linkChannelPen
        font = self._linkChannelFont
        item = self._scene.addLinkChannelItem(channel, x, y, w, h, name, direct.lower(), nLevel, linkItem, pen, brush, color, font)
        if channel.hasGuiData(linkItem):
            bVisible = True
            guiData = channel.getGuiData(linkItem)
            visible = guiData.get("visible")
            if visible and len(visible):
                if visible.lower() == "false":
                    bVisible = False
            item.setVisible(bVisible)
#            linkItem.updateChannelItem()
        return item
                
    def drawRectItem(self, x, y, w, h, parent=None, pen=QPen(), brush=QBrush()):
        item = self._scene.addRectItem(x, y, w, h, parent, pen, brush)
#        item.setFlag(QGraphicsItem.ItemIsMovable, True)
        return item
    
    def drawTextItem(self, text, x, y, parent=None, color=QColor()):
        item = self._scene.addTextItem(text, x, y, parent, color)
        return item

    def drawLineItem(self, xStart, yStart, xEnd, yEnd, parent=None, pen=QPen()):
        item = self._scene.addLineItem(xStart, yStart, xEnd, yEnd, parent, pen)
        return item
    
    def addGroupItem(self, parentItem=None):
        return self._scene.addGroupItem(parentItem)
    
    def addWidget(self, x, y, widget, flags):
        return self._scene.addWidget(x, y, widget, flags)

#    #draw connection for all children in module
#    def drawModuleFullConnection(self, x, y, module):
#        groupItem = self._scene.addGroupItem()
##        groupItem.setParentItem(parentItem)
#        self._scene.addItem(groupItem)
#        module.setGraphicsItem(groupItem)
#        if module.isLink() == False and len(module.getChildren())>0:
#            #sort module by port number
#            children = module.getChildren()
#            children.sort(key=self.getPortCnt, reverse=True)
#            
#            childModules = []#module list
#            childLinks = []#link list
#            child = children.pop()
#            while child:
#                if child.isLink():
#                    childLinks.append(child)
#                else:
#                    childModules.append(child)
#                if len(children) > 0:
#                    child = children.pop()
#                else:
#                    child = None
#
#            #top module
#            item = self.drawModule(x, y, module, None)
#            groupItem.addToGroup(item)
#
#            channelSpace = module.getChannelSpace()#self._moduleChannelSpace
#            xChild = x + self._moduleContentsMargin + channelSpace
#            yChild = y + self._moduleContentsMargin + channelSpace
#            
#            #first to draw module and its connection which has most port
#            if len(childModules) > 0:
#                childModule = childModules.pop(0)
#                childItem = self.drawModule(xChild, yChild, childModule, item)
#            
#                self.drawModuleLink(childModule, item, childLinks)
#            
#            childModules2 = []#module no connection
#            if len(module.getChildren()) > 0:
#                childModule = childModules.pop()
#                while childModule:
#                    link = self.getLinkByModule(childModule)
#                    if link != None:
#                        childItem = self.connectModule(xChild, yChild, childModule, item, childLinks)
#                    elif len(childLinks) > 0:
#                        children.append(childModule)
#                    else:
#                        childModules2.append(childModule)
#                    
#                    rect = childItem.boundingRect()
#                    xChild += rect.width() + channelSpace
#                    
#                    if len(childModules) > 0:
#                        childlModule = childModules.pop()
#                    else:
#                        childModule = None
#            
#            #draw module that no connection
#            if len(childModules2) > 0:
#                childModule = childModules2.pop()
#                while childModule:
#                    if len(childModules2) > 0:
#                        childModule = childModules2.pop()
#                    else:
#                        childModule = None
#        else:
#            drawLink(self, x, y, module, None, False)
#                
#        #adjust module rect size
#        rect0 = item.rect()
#        rect1 = item.childrenBoundingRect()
#        w = rect1.width() + self._moduleContentsMargin*1 + channelSpace*1
#        h = rect1.height() + self._moduleContentsMargin*1 + channelSpace*1
#        rect0.setWidth(w)
#        rect0.setHeight(h)
#        item.setRect(rect0)
##        module.setW(w)
##        module.setH(h)
#        
##        self.drawModulePort(item.pos().x(), item.pos().y(), module,item)

#    def drawOneModule(self, x, xOffset, y, yOffset, module, parentModule, parentItem):
#        pen = self._modulePen
#        brush = self._moduleBrush
#        textColor = self._moduleTextColor
#        xText = x + xOffset
#        yText = y + yOffset
#        w = module.getW()
#        h = module.getH()
#        
#        bLink = False
#        if len(module.getLink()) > 0:
#            bLink = True
#            pen = self._linkPen
#            brush = self._linkBrush
#            textColor = self._linkTextColor
##            xText += w
#            yText -= h
#        
#        print(x+xOffset, y+yOffset, w, h)
#        item = self.drawRectItem(x+xOffset, y+yOffset, w, h, parentItem, pen, brush)
##        item.setPos(x, y)
##        item.setTransformOriginPoint(x, y)
#        text = self.drawTextItem(module.getName(), xText, yText, item, textColor)
#
#        if bLink:
#            self._drawOneLink(x+xOffset, y+yOffset, module, item, False)
#        else:
#            nChild = len(module.getChildren())
#            nRow = 1
##            if nChild > 2:
##                for i in range(nRow,nChild//2):
##                    if nChild%i < i:
##                        nRow = i
##                        break
##            wOffset = 0.0
##            hOffset = 0.0
#            xOffsetChild = self._moduleContentsMargin + self._moduleChannelSpace#0
#            yOffsetChild = self._moduleContentsMargin + self._moduleChannelSpace#0
#            xChild = x# + self._moduleContentsMargin + self._moduleChannelSpace
#            yChild = y# + self._moduleContentsMargin + self._moduleChannelSpace
#            for i, childModule in enumerate(module.getChildren()):
#                childItem = self.drawOneModule(xChild, xOffsetChild, yChild, yOffsetChild, childModule, module, item)
#                rect = childItem.rect()
#                if i>0 and (0==i%nRow):
##                    wOffset = 0.0
#                    xOffsetChild = self._moduleContentsMargin + self._moduleChannelSpace
#                    yOffsetChild = rect.height() + self._moduleChannelSpace
#                else:
#                    xOffsetChild += rect.width() + self._moduleChannelSpace
#                    yOffsetChild = self._moduleContentsMargin + self._moduleChannelSpace
##                childItem.setPos(xChild, yChild)
#                    
#        if parentModule and parentItem:
#            rect = parentItem.childrenBoundingRect()
#            pX = parentItem.x()
#            pY = parentItem.y()
#            pW = rect.width() + self._moduleContentsMargin*1 + self._moduleChannelSpace*1
#            pH = rect.height() + self._moduleContentsMargin*1 + self._moduleChannelSpace*1
#            rect.setX(pX)
#            rect.setY(pY)
#            rect.setWidth(pW)
#            rect.setHeight(pH)
#            parentItem.setRect(rect)
##            parentModule.setW(pW)
##            parentModule.setH(pH)
#        
#        return item
#    #end def _drawOneModule
#    
#    def _drawOneLink(self, x, y, link, parentItem, bHor):
#        groupItem = self._scene.addGroupItem()
#        groupItem.addToGroup(parentItem)
#        
#        w = 0
#        h = 0
#        for child in link.getChildren():
#            item = self.drawRectItem(x, y, child.getW(), child.getH(), parentItem, self._linkPen, self._linkBrush)
#            self.drawTextItem(child.getName(), x+child.getW(), y, item, self._linkTextColor)
##            self.drawTextItem(child.getName(),child.getW(),child.getH()/2, item, self._linkTextColor)
#            groupItem.addToGroup(item)
#            if bHor:
#                x += child.getW()
##                w += child.getW()
#            else:
#                y += child.getH()
##                h += child.getH()
#        
#        if w>0 and h>0:
#            link.setW(w)
#            link.setH(h)
##            parentItem.update(x, y, w, h)
#            
#        self._scene.addItem(groupItem)
##        groupItem.setPos(x, y)
#        return groupItem


#    def mousePressEvent(self, event):
#        super(QGraphicsView, self).mouseEvent(self, event)
#    #enddef mousePressEvent

#    def mouseMoveEvent(self, event):
#        super(QGraphicsView, self).mouseMoveEvent(self, event)
#    #end def mouseMoveEvent

    def drawTestItem(self):
        #button
        self.myBtn = QPushButton("Test")
        self.myBtnProxy = self._scene.addWidget(self.myBtn);
        self.myBtnProxy.setPos(50, 50)
#        self.myBtnProxy.setFlag(QGraphicsItem.ItemIsMovable, True)
#        self.myBtnProxy.setFlags((QGraphicsItem.GraphicsItemFlag)(1|2|4|8))
        self.myBtn.resize(self.myBtn.sizeHint())
        #button proxy rect
        btnRect = self.drawRectItem(50, 30, self.myBtn.width(), self.myBtn.height()+20, None, self._modulePen, self._moduleBrush)
        btnRect.setFlag(QGraphicsItem.ItemIsMovable, True)
#        btnRect.setFlags((QGraphicsItem.GraphicsItemFlag)(1|2|4|8))
        self.myBtnProxy.setParentItem(btnRect)
        btnRect.setParentItem(None)
        
        #line
#        line = self._scene.addLine(0,0,100,100, self._linePen);
#        line.setFlag(QGraphicsItem.ItemIsMovable, True)
#        line.setFlags((QGraphicsItem.GraphicsItemFlag)(1|2|4|8))
        
#        rect = self._drawRectItem(200,200, 100, 100, None, self._headPen, self._headBrush)
        #rect
        rect = self.drawRectItem(0,0, 100, 100, None, self._modulePen, self._moduleBrush)
        rect.setPos(0,0)
        rect.setFlag(QGraphicsItem.ItemIsMovable, True)
        rect.setFlags((QGraphicsItem.GraphicsItemFlag)(1|2|4|8))
        textItem = self.drawTextItem("1", 0, 0, rect, QColor(Qt.blue))
        
        rect = self.drawRectItem(110,0, 100, 100, None, self._modulePen, self._moduleBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable, True)
        rect.setFlags((QGraphicsItem.GraphicsItemFlag)(1|2|4|8))
        textItem = self.drawTextItem("2", 50, 0, rect, QColor(Qt.blue))
        
        
        rect = self.drawRectItem(220,0, 100, 100, None, self._modulePen, self._moduleBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable, True)
        rect.setFlags((QGraphicsItem.GraphicsItemFlag)(1|2|4|8))
        textItem = self.drawTextItem("3", 100, 0, rect, QColor(Qt.blue))
        
        #text
        textItem = self.drawTextItem("Hello!", 150, 150, rect, QColor(Qt.blue))
        textItem.setTextWidth(3)
    #end def _drawTestItem
    
#end class AW_ChartView

#if __name__ == "__main__":
#    from ..database.dcArchDesign import *
#    app = QCoreApplication.instance()
#    if app is not None:
#        pass
#    elif app is None:
#        app = QApplication(sys.argv)
#        
#    dcView = DC_ChartView(None, None)
#    dcView.resize(1200, 800)
#    dcView._graphic.setSceneRect(300, 300, 0, 0)
#    dcView.drawTestItem()
#    dcView.show()
#        
#    sys.exit(app.exec_())
#end main
