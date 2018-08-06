# -*- coding: utf-8 -*-
"""
Created on Mo May 17 14:29:50 2018

@author: xnjiang
"""
import sys
import os.path

sys.path.append("..")

from api.dcApi import*

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.guiInterface.dcMainWin import *
from src.common.dcGlobal import *
__dcApp = None
__dcMainWin = None

def hideDesignChartWin():
    if __dcMainWin:
        __dcMainWin.hide()
        
def showDesignChartWin(file=""):
    global __dcApp
    app = __dcApp
    if __dcApp == None:
       __dcApp = app = QApplication(sys.argv)
#    app = QCoreApplication.instance()
#    if app is not None:
#        pass
#    elif app is None:
#        app = QApplication(sys.argv)
        
#    app.setStyle(QStyleFactory.create("Windows"))
#    app.setPalette(app.style().standardPalette())
    global __dcMainWin
    if __dcMainWin == None:
        if (len(sys.argv)>1):
            file = sys.argv[1]
        __dcMainWin = DC_MainWindow(file)
        dcSetMainWin(__dcMainWin)
        __dcMainWin.resize(1200, 800)
        __dcMainWin.show()
    else:
        __dcMainWin.show()
#    app.processEvents()
    return app

def runDesignChart(file=""):
    app = showDesignChartWin(file)
    if app:
        sys.exit(app.exec_())
        
def exitDesignChart():
    if __dcApp:
        __dcApp.exit()

def setModuleState(view, moduleFullName, state="", level=-1):
    if __dcMainWin != None:
        __dcMainWin.setModuleState(view, moduleFullName, state, level)
        
def setPortState(view, moduleFullName, portName, state="", level=-1):
    if __dcMainWin != None:
        __dcMainWin.setPortState(view, moduleFullName, portName, state)
        
def setColorOfState(state, color):
    if __dcMainWin != None:
        __dcMainWin.setColorOfState(state, color)
        
def importDesign(fileName):
    view = None
    if __dcMainWin != None:
        view = __dcMainWin.addView(fileName)
    return view


def getCurrentView():
    view = None
    if __dcMainWin != None:
        view = __dcMainWin.getCurView()
    return view

def setModuleDebugData(view, moduleFullName, data):#view -- returned by importDesign(), data -- pandas DataFrame
    if __dcMainWin != None:
        __dcMainWin.setModuleDebugData(view, moduleFullName, data)

def setModuleAnnotation(view, moduleFullName, data):
    if __dcMainWin != None:
        __dcMainWin.setModuleAnnotation(view, moduleFullName, data)

def setModuleToolTip(view, moduleFullName, data):
    if __dcMainWin != None:
        __dcMainWin.setModuleToolTip(view, moduleFullName, data)

if __name__ == "__main__":
    runDC()
#end __main__
