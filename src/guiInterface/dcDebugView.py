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

from .dcBaseView import*

from ..guiInterface.dcChartView import *
from ..qtGui.others.dcTreeWidget import *
from ..qtGui.others.dcListWidget import *

class DC_DebugView(DC_BaseView):
    
    def __init__(self, parent, design):
        super(DC_DebugView, self).__init__(parent, design, "debug view")
        
        self._hierTree = self.buildDesginHier()
        
#        self._chartViewTab = self.buildChartView()
        self.getCurrentChart().drawDebugChart()
        
        self.show()
    
    def buildDesginHier(self):
        #design hierarchy dock
        hierDock = QDockWidget("Hierarchy", self._frameMainWin)
        hierDock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self._frameMainWin.addDockWidget(Qt.LeftDockWidgetArea, hierDock)
        
        splitter = QSplitter(Qt.Vertical)
        
        #module list
        self._hierTree = hierTree = DC_TreeWidget()
        hierTree.setStyle(QStyleFactory.create("Windows"))
        hierTree.setPalette(hierTree.style().standardPalette())
        treeHeader = hierTree.header()
        treeHeader.setStyle(QStyleFactory.create("Windows"))
        treeHeader.setPalette(treeHeader.style().standardPalette())
        hierTree.setHeader(treeHeader)
        treeHeader.setVisible(False)
        
        self.buildDesignTree(hierTree)
        
        splitter.addWidget(hierTree)
        
        hierDock.setWidget(splitter)
        
        hierTree.setPopupCB(self._hierTreePopupCB)
        hierTree.setClickCB(self._hierTreeClickCB)
        hierTree.setItemChangeCB(self._hierTreeItemChangeCB)
        
        return hierTree
        
    def buildDesignTree(self, tree):
        tree.clear()
#        hierTree.setColumnCnt(1)
        topModule = self.getTopModule()
#        topName = topModule.getName()
#        topItem = QTreeWidgetItem()
#        topItem.setText(0, topName)
##       topItem.setData(0, Qt.UserRole, topModule)
#        tree.addTopLevelItem(topItem)
#        self._addChildItem(topModule, topItem, "hier")
        self._addChildItem(topModule, tree, None, "debug")
#        tree.expandAll()
            
#    def _addChildItem(self, parentModule, tree, parentItem, treeType):
#        if parentItem:
#            parentItem.setData(0, Qt.UserRole, parentModule)
#        for module in parentModule.getChildren():
#            childItem = QTreeWidgetItem()
#            if treeType == "debug":
#                checked = Qt.Checked
#                if module.isVisible() == False:
#                    checked = Qt.Unchecked
#                childItem.setCheckState(0, checked)
#            childItem.setText(0, module.getName())
#            if module.isLink():
#                childItem.setIcon(0, QIcon("../src/resource/image/icon/link.png"))
#            else:
#                if parentModule.isLink():
#                    childItem.setIcon(0, QIcon("../src/resource/image/icon/channel.png"))
#                else:
#                    childItem.setIcon(0, QIcon("../src/resource/image/icon/module.png"))
#            if parentItem:
#                parentItem.addChild(childItem)
#            else:
#                tree.addTopLevelItem(childItem)
#            self._addChildItem(module, tree, childItem, treeType)
            
    def _hierTreePopupCB(self):
        pass
#        popMenu = QMenu(self)
#        act = popMenu.addAction("Show Chart")
#        act.triggered.connect(self._drawDebugChartCB)
#        popMenu.popup(QCursor.pos())
#
#    def _drawDebugChartCB(self):
#        chartView = DC_ChartView(self, self._design)# self._chartVie
#        curItem = self._hierTree.currentItem()
#        module = curItem.data(0, Qt.UserRole)
#        self._chartViewTab.addTab(chartView, module.getName())
#        self._chartViewTab.setCurrentWidget(chartView)
#        chartView.drawLinkConnection(module)
    
#    def _hierTreeClickCB(self, item, column):
#        pass

    def _hierTreeItemChangeCB(self, item, column):
        module = item.data(0, Qt.UserRole)
        bVisible = True
        parentItem = item.parent()
        if Qt.Checked == item.checkState(column):
            module.setGuiDataAttr(parentItem, "visible", "True")
        elif Qt.Unchecked == item.checkState(column):
            module.setGuiDataAttr(parentItem, "visible", "False")
            bVisible = False

        chartTab = self.getChartTab()
        nChart = chartTab.count()
        for i in range(0, nChart):
            chart = chartTab.widget(i)
            chart.setItemVisible(module, bVisible)
        
#end class DC_ArchView

#if __name__ == "__main__":
#    from ..database.dcArchDesign import *
#    if len(sys.argv)>1:
#        app = QCoreApplication.instance()
#        if app is not None:
#            pass
#        elif app is None:
#            app = QApplication(sys.argv)
#        design = DC_ArchDesign(sys.argv[1])
#        av = DC_DebugView(None, design)
#        av.resize(1200, 800)
#        av.show()
#        sys.exit(app.exec_())
#end main
