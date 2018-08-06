# -*- coding: utf-8 -*-
"""
Created on Mo May 28 2018

@author: xnjiang
"""

import sys
#import os

#from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#from PyQt5.QtOpenGL import *

from ..guiInterface.dcChartView import *
from ..qtGui.others.dcTabWidget import *
from ..qtGui.others.dcDockWidget import *

#class DC_BaseView(QWidget, object):
class DC_BaseView(DC_DockWidget, object):
    
    def __init__(self, parent, design, sType):
        super(DC_BaseView, self).__init__(parent, sType)
        self.setTitleBarWidget(QWidget())
#        self.setAllowedAreas(Qt.RightDockWidgetArea)
        
        self._sType = sType
        self._design = design
        
        #GUI layout and views
#        self.layout_container = QVBoxLayout()
#        self.layout_container.setSizeConstraint(QLayout.SetMaximumSize)
#        self.setLayout(self.layout_container)
        #frame main window for hierarchy dock
        self._frameMainWin = QMainWindow()
        self.buildChartView(sType)
#        self.layout_container.addWidget(self._frameMainWin)
        self.setWidget(self._frameMainWin)
        
    
    def getType(self):
        return self._sType
    
    def selectDesignItem(self, designObj, hasFocus):
        if designObj:
            if designObj.isPort():
                designObj = designObj.getModule()
            self.selectTreeItem(designObj.getDesignItem(), hasFocus)
            
    def selectTreeItem(self, item, hasFocus):
        if item:
            tree = item.treeWidget()
            tree.scrollToItem(item)
            tree.clearSelection()
            if hasFocus:
                tree.setFocus()
            item.setSelected(True)
            tree.setCurrentItem(item)

    def _addChildItem(self, parentModule, tree, parentItem, treeType):
        if parentItem:
            parentItem.setData(0, Qt.UserRole, parentModule)
            parentModule.setDesignItem(parentItem)
        for module in parentModule.getChildren():
#            if treeType == "hier" and module.isLink():
#                continue
            childItem = QTreeWidgetItem()
            childItem.setText(0, module.getName())
            if module.isLink():
                childItem.setIcon(0, QIcon("../src/resource/image/icon/link.png"))
            else:
                if parentModule.isLink():
                    childItem.setIcon(0, QIcon("../src/resource/image/icon/channel.png"))
                else:
                    childItem.setIcon(0, QIcon("../src/resource/image/icon/module.png"))
            if treeType == "hier" or treeType == "debug":
                checked = Qt.Checked
                if module.isVisible() == False:
                    checked = Qt.Unchecked
                childItem.setCheckState(0, checked)
            if parentItem:
                parentItem.addChild(childItem)
            else:
                tree.addTopLevelItem(childItem)
#                childItem.setExpanded(True)
            self._addChildItem(module, tree, childItem, treeType)
            
    def _hierTreeClickCB(self, item, column):
        if item is None:
            return
        module = item.data(0, Qt.UserRole)
#        self.showLinkInModule(module)
        chart = self.getCurrentChart()
        chart.setItemSelected(module, True)
        
    def buildChartView(self, sType):
        self._chartViewTab = chartViewTab = DC_TabWidget(self, sType+"'s chart")
#        chartViewTab.setStyleSheet("QGraphicsView {background: red }")
        chartViewTab.setPopupCB(self.chartTabPopupCB)
        chartViewTab.setDClickCB(self.chartTabDClickCB)

        module = self._design.getTopModule()
        self.addChart(sType, module)

        self._frameMainWin.setCentralWidget(chartViewTab)

    def getCurrentChart(self):
        return self._chartViewTab.currentWidget()
    
    def addChart(self, sType, module):
        chartView = DC_ChartView(self, self._design, sType)
        chartView.setTopLevelChangeCB(self.chartTopLevelChangeCB)
        fileName = self._design.getFile()
        chartView.setToolTip(os.path.abspath(fileName))
        name = module.getName()
        index = self._chartViewTab.addTab(chartView, name)
        self._chartViewTab.setCurrentWidget(chartView)
        self._chartViewTab.setTabToolTip(index, module.getFullName())
        return chartView
        
    def addViewToChartTab(self, view, tabName):
        tab = self._chartViewTab
        tab.addTab(view,tabName)
        tab.setCurrentWidget(view)
        index = tab.indexOf(view)
        tab.setTabToolTip(index, view.toolTip())
        
    def chartTopLevelChangeCB(self, view, bFloating):
        if bFloating:
            self.addViewToChartTab(view, view.windowTitle())
            view.setTitleBarWidget(QWidget())
        else:
            tab = self._chartViewTab
            index = tab.indexOf(view)
            tabName = tab.tabText(index)
            tab.removeTab(index)
            view.setParent(self._frameMainWin)
            view.setAllowedAreas(Qt.NoDockWidgetArea)
            view.setFeatures(QDockWidget.DockWidgetFeature(QDockWidget.AllDockWidgetFeatures&(~QDockWidget.DockWidgetFloatable)))
            view.setWindowTitle(tabName)
            view.setFloating(True)
            view.show()
            view.setTitleBarWidget(None)
            
    def undockChartViewCB(self):
        tab = self._chartViewTab
        view = tab.currentWidget()
        self.chartTopLevelChangeCB(view, False)
        
    def chartTabPopupCB(self, tab, index):
        popMenu = QMenu(self)
        act = popMenu.addAction("Undock")
        act.triggered.connect(self.undockChartViewCB)
        popMenu.popup(QCursor.pos())
        pass
    
    def chartTabDClickCB(self, tab, index):
        view = tab.widget(index)
        self.chartTopLevelChangeCB(view, False)
        pass
    
    def isDebug(self):
        return  self._design.isDebug()
    
    def getDesign(self):
        return self._design
    
    def getChartTab(self):
        return self._chartViewTab
    
    def getTopModule(self):
        return self._design.getTopModule()

    def getModule(self, fullName):
        return self._design.getModule(fulllName)
        
    def getPort(self, fullName):
        port = self._design.getPort(fullName)   
        return port
    
    def getLink(self, fullName):
        return self._design.GetLink(fullName)
    
    def saveDesignToFile(self, file=None):
        sFile = file
        if not sFile or not len(file):
            sTitle = "Save Design"
            if self.isDebug():
                sTitle = "Save Debug"
            sFile = os.path.abspath(self._design.getName())
            fileName = QFileDialog.getSaveFileName(self, sTitle, sFile, "Design Files (*.xml)")
            sFile = fileName[0]
            
        if sFile is not None and len(sFile):
            self._design.saveToFile(sFile)
#end class DC_ArchView
