# -*- coding: utf-8 -*-
"""
Created on Mo May 28 2018

@author: xnjiang
"""
#import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import *
from PyQt5.QtWidgets import *


class DC_DockWidget(QDockWidget, object):

    def __init__(self, parent, sType):
        super(DC_DockWidget, self).__init__(parent)
        self.initDockWidget(sType)

    def initDockWidget(self, sType):
        self._sType = sType
        self.popCB = None
        self.topLevelChangeCB = None
        act = self.toggleViewAction()
        act.setEnabled(False)
    
    def getType(self):
        return self._sType
    
    def setPopupCB(self, cb):
        self.popCB = cb
    
    def setTopLevelChangeCB(self, cb):
        self.topLevelChangeCB = cb
        
    def contextMenuEvent(self, event):
        super(DC_DockWidget, self).contextMenuEvent(event)
        if self.popCB:
            self.popCB()
    
    def event(self, event):
#        print(event.type())
        if QEvent.NonClientAreaMouseButtonDblClick == event.type() or (QEvent.MouseButtonDblClick == event.type() and self.isFloating() and event.pos().y<20):
            bFloating = self.isFloating()
            self.topLevelChange(bFloating)
            return True
        elif QEvent.Close == event.type():
#            msgBox = QMessageBox()
            sInfo = "Do you want to delete %s \"%s\"?" % (self.getType(), self.windowTitle())
#            msgBox.setInformativeText(sInfo)
#            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
#            msgBox.setDefaultButton(QMessageBox.Cancel)
#            ret = msgBox.exec_()
            ret = QMessageBox.warning(self, "DC", sInfo, QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
            if ret == QMessageBox.Ok:
                self.deleteLater()
            else:
                QTimer.singleShot(0, self.show)
            return True
        return super().event(event)
    
    def topLevelChange(self, bFloating):
        if self.topLevelChangeCB:
            self.topLevelChangeCB(self, bFloating)

#end class DC_DockWidget
