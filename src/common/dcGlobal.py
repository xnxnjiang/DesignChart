# -*- coding: utf-8 -*-
"""
Created on Mo May 28 2018

@author: xnjiang
"""

global stateBusy
stateBusy = "busy"
global busyColor
busyColor = "orange"

global stateFail
stateFail = "fail"
global failColor
failColor = "red"

global statePass
statePass = "pass"
global passColor
passColor = "limegreen"

global stateStandby
stateStandby = "standby"
global standbyColor
standbyColor = "yellow"

global stateReady
stateReady = "ready"
global readyColor
readyColor = "blue"

#global dcMainWin
dcMainWin = None

def dcSetMainWin(win):
    global dcMainWin
    dcMainWin = win
    
def dcGetMainWin():
    global dcMainWin
    return dcMainWin
