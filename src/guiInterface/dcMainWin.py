# -*- coding: utf-8 -*-
"""
Created on Mo May 17 14:29:50 2018

@author: xnjiang
"""
import sys
import os.path

sys.path.append("..")

#from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#from PyQt5.QtOpenGL import *

from src.database.dcArchDesign import *

from src.guiInterface.dcArchView import *
from src.guiInterface.dcDebugView import *

from src.qtGui.others.dcTabWidget import *

from api.dcApi import*

class DC_MainWindow(QMainWindow, object):
    central_widget = None
    layout_container = None

    def __init__(self, file):
        super(DC_MainWindow, self).__init__()

        #File
        self.menuFile = self.menuBar().addMenu("File")

        self.importAct = self.menuFile.addAction("Import Design")
        self.importAct.triggered.connect(self.importDesignFile)

        self.importAct = self.menuFile.addAction("Save")
        self.importAct.triggered.connect(self.saveCurrentDesignChart)
        
        self.importAct = self.menuFile.addAction("Save As")
        self.importAct.triggered.connect(self.saveCurrentDesignChartToFile)
        
        self.importAct = self.menuFile.addAction("Save All")
        self.importAct.triggered.connect(self.saveAllDesignChart)
        
        self.exitAct = self.menuFile.addAction("Exit")
        
        #Edit
        self.menuEdit = self.menuBar().addMenu("Edit")
        
        #Help
        self.menuHelp = self.menuBar().addMenu("Help")
        
        self.exitAct.triggered.connect(self.exitApp)

        self.designTab = DC_TabWidget(self, "view")
        self.designTab.setPopupCB(self.designTabPopupCB)
        self.designTab.setDClickCB(self.designTabDClickCB)

        self.setCentralWidget(self.designTab)
        
        if file is not None and len(file):
            self.addView(os.path.abspath(file))
            
#        #draw test item
#        self._addLatencyView(None,"TestItem")
#        self._curLatencyView.myGraphic.drawTestItem()
    #end def __init__

#    def importDebugFile(self):
#        fileName = QFileDialog.getOpenFileName(self, "Import Debug File", ".", "Debug Files (*.xml)")
#        if fileName[0] is not None and len(fileName[0]):
#            curPath = QDir.currentPath()
#            self._addDebugView(fileName[0][len(curPath)+1:], fileName[0])

    def importDesignFile(self):
        fileName = QFileDialog.getOpenFileName(self, "Import Design File", ".", "Design Files (*.xml)")
        self.addView(fileName[0])

    def _addDebugView(self, design):
        debugView = DC_DebugView(self.designTab, design)
        return debugView

    def _addArchView(self, design):
        archView = DC_ArchView(self.designTab, design)
        return archView

    def designTopLevelChangeCB(self, view, bFloating):
        if bFloating:
            self.addViewToDesignTab(view, view.windowTitle())
            view.setTitleBarWidget(QWidget())
        else:
            designTab = self.designTab
            index = designTab.indexOf(view)
            tabName = designTab.tabText(index)
            designTab.removeTab(index)
            view.setParent(self)
            view.setAllowedAreas(Qt.NoDockWidgetArea)
            view.setFeatures(QDockWidget.DockWidgetFeature(QDockWidget.AllDockWidgetFeatures&(~QDockWidget.DockWidgetFloatable)))
            view.setWindowTitle(tabName)
            view.setFloating(True)
            view.show()
            view.setTitleBarWidget(None)
            
    def undockDesignViewCB(self):
        designTab = self.designTab
        view = designTab.currentWidget()
        self.designTopLevelChangeCB(view, False)
    
    def designTabPopupCB(self, tab, index):
        popMenu = QMenu(self)
        act = popMenu.addAction("Undock")
        act.triggered.connect(self.undockDesignViewCB)
        popMenu.popup(QCursor.pos())
    
    def designTabDClickCB(self, tab, index):
        view = tab.widget(index)
        self.designTopLevelChangeCB(view, False)
    
    def addView(self, fileName):
        view = None
        if fileName is not None and len(fileName):
            design = DC_ArchDesign(os.path.abspath(fileName))
            curPath = QDir.currentPath()
            if design.isDebug():
                view = self._addDebugView(design)
            else:
                view = self._addArchView(design)
            view.setTopLevelChangeCB(self.designTopLevelChangeCB)
            view.setToolTip(os.path.abspath(fileName))
            tabName = os.path.basename(fileName)
            index = self.addViewToDesignTab(view, tabName)
            
        return view

    def addViewToDesignTab(self, view, tabName):
        designTab = self.designTab
        index = designTab.addTab(view,tabName)
        designTab.setCurrentWidget(view)
#        index = designTab.indexOf(view)
        fileName = view.getDesign().getFile()
        designTab.setTabToolTip(index, os.path.abspath(fileName))
        
    def exitApp(self):
        self.close()
        
    def closeEvent(self, event):
        isGuiModified = False
        designTab = self.designTab
        nView = designTab.count()
        for i in range(0, nView):
            view = designTab.widget(i)
            isGuiModified = view.getDesign().isGuiModified()
            if isGuiModified:
                break
        
        if isGuiModified:
            ret = QMessageBox.warning(self, "DC", "Design's GUI has been modified. Do you want to save the modification?", QMessageBox.Save | QMessageBox.No, QMessageBox.Save)
            if ret == QMessageBox.Save:
                self.saveAllDesignChart()

#        msgBox = QMessageBox(self)
#        msgBox.setInformativeText("Do you want to exit DC?");
#        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
#        msgBox.setDefaultButton(QMessageBox.Ok)
#        ret = msgBox.exec_()
        ret = QMessageBox.warning(self, "DC", "Do you want to exit DC?", QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
        if ret == QMessageBox.Ok:
#            self.saveAllDesignChart()
            event.accept()
            sys.exit(0)
        else:
            event.ignore()

    def saveCurrentDesignChart(self):
        designTab = self.designTab
        view = designTab.currentWidget()
        file = view.getDesign().getName()
        self.saveCurrentDesignChartToFile(file)
    
    def saveCurrentDesignChartToFile(self, file=""):
        designTab = self.designTab
        view = designTab.currentWidget()
        self.saveDesignChart(view, file)
    
    def saveDesignChart(self, view, file):
        if not view:
            return
        chartTab = view.getChartTab()
        nChart = chartTab.count()
        for j in range(0, nChart):
            chart = chartTab.widget(j)
            chart.saveGuiData()
        view.saveDesignToFile(file)
        view.getDesign().setGuiModified(False)
        
    def saveAllDesignChart(self):
        designTab = self.designTab
        nView = designTab.count()
        for i in range(0, nView):
            view = designTab.widget(i)
            file = view.getDesign().getName()
            self.saveDesignChart(view, file)
        
#API rountines
    def setChartItemData(self, dataType, view, moduleFullName, portName, data, level=0):
        designTab = self.designTab
        nView = designTab.count()
        for i in range(0, nView):
            viewTmp = designTab.widget(i)
            if not view or (view == viewTmp):
                design = viewTmp.getDesign()
                item = module = design.getModule(moduleFullName)
                if module and portName and len(portName):
                    item = port = module.getPort(portName)
                chartTab = viewTmp.getChartTab()
                nChart = chartTab.count()
                for j in range(0, nChart):
                    chart = chartTab.widget(j)
                    if dataType == "ItemState":
                        chart.setItemState(item, data, level)
                    elif dataType == "StateColor":
                        chart.setColorOfState(moduleFullName, portName)#moduleFullName is state, portName is color
                    elif dataType == "DebugData":
                        chart.setItemDebugData(item, data)
                    elif dataType == "Annotation":
                        chart.setItemAnnotation(item, data)
                    elif dataType == "ToolTip":
                        chart.setItemToolTip(item, data)
                if view == viewTmp:
                    break
        
    def setModuleState(self, view, moduleFullName, state, level):
        self.setChartItemData("ItemState", view, moduleFullName, "", state, level)
    
    def setPortState(self, view, moduleFullName, portName, state):
        self.setChartItemData("ItemState", view, moduleFullName, portName, state)
    
    def setColorOfState(self, state, color):
        self.setChartItemData("StateColor", None, state, color, None)
                
    def getCurView(self):
        return self.designTab.currentWidget()
    
    def setModuleDebugData(self, view, moduleFullName, data):#view -- returned by importDesign(), data -- pandas DataFrame
        self.setChartItemData("DebugData", view, moduleFullName, "", data)

    def setModuleAnnotation(self, view, moduleFullName, data):
        self.setChartItemData("Annotation", pView, moduleFullName, "", data)
    
    def setModuleToolTip(self, view, moduleFullName, data):
        self.setChartItemData("ToolTip", view, moduleFullName, "", data)

    def setPortToolTip(self, view, moduleFullName, portName, sToolTip):
        self.setChartItemData("ToolTip", view, moduleFullName, portName, sToolTip)

#API rountines end
    
if __name__ == "__main__":
    runDC()
#end __main__
