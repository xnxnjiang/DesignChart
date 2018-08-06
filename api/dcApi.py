# -*- coding: utf-8 -*-
"""
Created on Mo May 17 14:29:50 2018

@author: xnjiang
"""
import sys
#import os.path

sys.path.append("..")

from bin.main import *
from src.common.dcGlobal import *

def runDC(file=""):
    runDesignChart(file)
    
def exitDC():
    exitDesignChart()

def showDC(file=""):
    return showDesignChartWin(file)
    
def hideDC():
    hideDesignChartWin()
    
#state: "busy" - violet, "fail" -- red, "pass" -- green, "standby" -- yellow, "ready" -- blue, "" -- orignal color; #level: -1 -- for channel's all level
def dcSetModuleState(view, moduleFullName, state="", level=-1):#view==None, set module in all views
    setModuleState(view, moduleFullName, state, level)

#state: "busy" - violet, "fail" -- red, "pass" -- green, "standby" -- yellow, "ready" -- blue, "" -- orignal color
def dcSetPortState(view, moduleFullName, portName, state=""):#view==None, set module in all views
    setPortState(view, moduleFullName, portName, state)
    
#custimize color of state
def dcSetColorOfState(state, color):
    setColorOfState(state, color)
    
def dcImportDesign(fileName):
    view = importDesign(fileName)
    return view

def dcGetCurrentView():
    getCurrentView()

def dcSetModuleDebugData(view, moduleFullName, data):#view -- returned by importDesign(), data -- pandas DataFrame
    setModuleDebugData(view, moduleFullName, data)

def dcSetModuleAnnotation(view, moduleFullName, data):
    setModuleAnnotation(view, moduleFullName, data)

def dcSetModuleToolTip(view, moduleFullName, data):
    setModuleToolTip(view, moduleFullName, data)

if __name__ == "__main__":#for testing
    file = "top.xml"
    if (len(sys.argv)>1):
        file = sys.argv[1]
    showDC(file)
    dcSetColorOfState("busy", "orange")
    dcSetModuleState(None, "top.inst_tcdx[0]", stateReady)#set module state
    dcSetPortState(None, "top.inst_tcdx[0]", "fti_inp_0", stateFail)
    dcSetPortState(None, "top.inst_tcdx[0]", "fti_out_0", statePass)
    dcSetPortState(None, "top.inst_tcdx[0]", "fti_inp_1", stateBusy)
    dcSetPortState(None, "top.inst_tcdx[0]", "fti_out_1", stateStandby)
    dcSetPortState(None, "top.inst_tcdx[0]", "fti_inp_2", stateReady)
    dcSetPortState(None, "top.inst_tcdx[0]", "fti_out_2", stateStandby)
    dcSetModuleState(None, "top.inst_tcdx[0]", "")#clear moudle state
    dcSetModuleToolTip(None, "top.inst_tcdx[0]", "Hello tooltip!")
    dcSetModuleToolTip(None, "top.inst_tcdx[0]", "Hello tooltipaasfsdfsdf!")
    importDesign("debug.xml")
    runDC()
#    exitDC()
#end __main__
