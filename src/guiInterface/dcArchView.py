# -*- coding: utf-8 -*-
"""
Created on Mo May 28 2018

@author: xnjiang
"""

import sys
#import os
sys.path.append("..")

#from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#from PyQt5.QtOpenGL import *


from .dcBaseView import*

#from ..guiInterface.dcChartView import *
from ..qtGui.others.dcTreeWidget import *
from ..qtGui.others.dcListWidget import *

class DC_ArchView(DC_BaseView):
    
    def __init__(self, parent, design):
        super(DC_ArchView, self).__init__(parent, design, "design view")
        self._hierTree = self.buildDesginHier()
        self.getCurrentChart().drawDesignChart()
        self.show()
    
    def buildDesginHier(self):
        #design hierarchy dock
        hierDock = QDockWidget("Hierarchy", self._frameMainWin)
        hierDock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self._frameMainWin.addDockWidget(Qt.LeftDockWidgetArea, hierDock)
        
        splitter = QSplitter(Qt.Vertical)
        
        #design hierarchy tree
        self._hierTree = hierTree = DC_TreeWidget()
        hierTree.setStyle(QStyleFactory.create("Windows"))
        hierTree.setPalette(hierTree.style().standardPalette())
        treeHeader = hierTree.header()
        treeHeader.setStyle(QStyleFactory.create("Windows"))
        treeHeader.setPalette(treeHeader.style().standardPalette())
        hierTree.setHeader(treeHeader)
        treeHeader.setVisible(False)
        
        topItem = self.buildDesignTree(hierTree)
        
        splitter.addWidget(hierTree)
        
#        self._linkTree = linkTree = DC_TreeWidget()
#        linkTree.setStyle(QStyleFactory.create("Windows"))
#        linkTree.setPalette(hierTree.style().standardPalette())
#        treeHeader = linkTree.header()
#        treeHeader.setStyle(QStyleFactory.create("Windows"))
#        treeHeader.setPalette(treeHeader.style().standardPalette())
#        linkTree.setHeader(treeHeader)
#        treeHeader.setVisible(False)
#        self._linkTree.setPopupCB(self._linkTreePopupCB)
##        self._linkTree.setDClickCB(self._linkTreeDClickCB)
#        
#        splitter.addWidget(linkTree)
        
        hierDock.setWidget(splitter)
                
        hierTree.setPopupCB(self._hierTreePopupCB)
        hierTree.setClickCB(self._hierTreeClickCB)
        hierTree.setItemChangeCB(self._hierTreeItemChangeCB)
        hierTree.emitItemClick(topItem, 0)
#        self.showLinkInModule(self.getTopModule())
        
        return hierTree
        
    def buildDesignTree(self, tree):
        tree.clear()
#        hierTree.setColumnCnt(1)
        topModule = self.getTopModule()
        topName = topModule.getName()
        topItem = QTreeWidgetItem()
        topItem.setText(0, topName)
#       topItem.setData(0, Qt.UserRole, topModule)
        tree.addTopLevelItem(topItem)
        topItem.setExpanded(True)
        self._addChildItem(topModule, tree, topItem, "hier")
#        tree.expandAll()
        return topItem
            
#    def _addChildItem(self, parentModule, tree, parentItem, treeType):
#        if parentItem:
#            parentItem.setData(0, Qt.UserRole, parentModule)
#            parentModule.setDesignItem(parentItem)
#        for module in parentModule.getChildren():
##            if treeType == "hier" and module.isLink():
##                continue
#            childItem = QTreeWidgetItem()
#            childItem.setText(0, module.getName())
#            if module.isLink():
#                childItem.setIcon(0, QIcon("../src/resource/image/icon/link.png"))
#            else:
#                if parentModule.isLink():
#                    childItem.setIcon(0, QIcon("../src/resource/image/icon/channel.png"))
#                else:
#                    childItem.setIcon(0, QIcon("../src/resource/image/icon/module.png"))
#            if treeType == "hier":
#                checked = Qt.Checked
#                if module.isVisible() == False:
#                    checked = Qt.Unchecked
#                childItem.setCheckState(0, checked)
#            if parentItem:
#                parentItem.addChild(childItem)
#            else:
#                tree.addTopLevelItem(childItem)
##                childItem.setExpanded(True)
#            self._addChildItem(module, tree, childItem, treeType)
            
    def _drawModuleConnectionCB(self):
        curItem = self._hierTree.currentItem()
        module = curItem.data(0, Qt.UserRole)
        chartView = self.addChart(self.getType(), module)
        chartView.drawModuleConnection(0, 0, module)
            
    def _drawModuleScopeCB(self):
        curItem = self._hierTree.currentItem()
        module = curItem.data(0, Qt.UserRole)
        chartView = self.addChart(self.getType(), module)
#        chartView.drawOneModule(0, 0, 0, 0, module, None, None)
        chartView.drawModuleScope(0, 0, module)
        
    def _drawLinkConnectionCB(self, link):
#        curItem = self._linkTree.currentItem()
        curItem = self._hierTree.currentItem()
        module = curItem.data(0, Qt.UserRole)
        chartView = self.addChart(self.getType(), module)
#        chartView.drawOneModule(0, 0, 0, 0, module, None, None)
        chartView.drawLinkConnection(module)
    
    def _linkTreePopupCB(self):
        curItem = self._linkTree.currentItem()
        module = curItem.data(0, Qt.UserRole)
        if module.isLink():
            popMenu = QMenu(self)
            act = popMenu.addAction("Show Connection")
            act.triggered.connect(self._drawLinkConnectionCB)
            curItem = self._hierTree.currentItem()
            module = curItem.data(0, Qt.UserRole)
            popMenu.popup(QCursor.pos())
            
#    def _linkTreeDClickCB(self, item, column):
#        if item is None:
#            return
#        link = item.data(0, Qt.UserRole)
#        if link.isLink():
#            self._drawLinkConnectionCB(link)
        
    def _hierTreePopupCB(self):
        popMenu = QMenu(self)
        curItem = self._hierTree.currentItem()
        module = curItem.data(0, Qt.UserRole)
        if module.isLink():
            act = popMenu.addAction("Show Link Connection")
            act.triggered.connect(self._drawLinkConnectionCB)
        else:
            act = popMenu.addAction("Show Module Chart")
            act.triggered.connect(self._drawModuleScopeCB)
#            act.triggered.connect(self._drawModuleConnectionCB)
        popMenu.popup(QCursor.pos())
#        
#    def _hierTreeClickCB(self, item, column):
#        if item is None:
#            return
#        module = item.data(0, Qt.UserRole)
##        self.showLinkInModule(module)
#        chart = self.getCurrentChart()
#        chart.setItemSelected(module, True)
        
    def showLinkInModule(self, module):
        self._linkTree.clear()
        
        if module:
            for child in module.getChildren():
                if child.isLink():
                    linkName = child.getName()
                    linkItem = QTreeWidgetItem()
                    linkItem.setText(0, linkName)
                    checked = Qt.Checked
                    if module.isVisible() == False:
                        checked = Qt.Unchecked
                    linkItem.setCheckState(0, checked)
                    self._linkTree.addTopLevelItem(linkItem)
                    self._addChildItem(child, self._linkTree, linkItem, "link")

    def _hierTreeItemChangeCB(self, item, column):
        if 0 == column:
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
#        av = DC_ArchView(None, design)
#        av.resize(1200, 800)
#        av.show()
#        sys.exit(app.exec_())
#end main
