# -*- coding: utf-8 -*-
"""
Created on Mo May 28 2018

@author: xnjiang
"""
import sys

#from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import *
from PyQt5.QtWidgets import *

from .dcGraphicsRectItem import *
#from dcGraphicsFlyLineItem import *

class DC_GraphicsLinkChannelItem(DC_GraphicsRectItem):

    def __init__(self, channel, x, y, w, h, name, direct, nLevel, parentItem):
        super(DC_GraphicsLinkChannelItem, self).__init__(x, y, w, h, parentItem)
        self._initLinkChannelItem(channel, name, direct, nLevel)
        toolTip = "Channel: "+name+"\n    Levels: "+str(nLevel)+"\n       "+parentItem.toolTip()
        self.setToolTip(toolTip)

    def _initLinkChannelItem(self, channel, name, direct, nLevel):
        self._initItem("LinkChannelItem", name, channel)
        self._channel = channel
#        self._direct = direct
        self._nLevel = nLevel

    def getChannel(self):
        return self._channel
    
    def getLinkItem(self):
        return self.parentItem()
    
    def updateRect(self, direct, x, y, w, h):
        self.setRect(x, y, w, h)
        
        #get level item's start data
        xLevel = x
        yLevel = y
        wLevel = w
        hLevel = h/self._nLevel
        items = self.childItems()
        if direct.lower() ==  "uptodown":
            pass
        elif direct.lower() == "downtoup":
            items.reverse()
        elif direct.lower() == "lefttoright":
            wLevel = w/self._nLevel
            hLevel = h
        elif direct.lower() == "righttoleft":
            items.reverse()
            wLevel = w/self._nLevel
            hLevel = h
        #update level item's rect    
        for item in items:
            item.setRect(xLevel, yLevel, wLevel, hLevel)
            if direct.lower() ==  "uptodown" or direct.lower() == "downtoup":
                yLevel += hLevel
            else:
                xLevel += wLevel
        
#    def mousePressEvent(self, event):
#        super(DC_GraphicsLinkChannelItem, self).mousePressEvent(event)
#        linkItem = self.getLinkItem()
#        linkItem.mousePressEvent(event)
##        linkItem.setSelected(True)
##        linkItem.drawFlyLine();
#
#    def mouseReleaseEvent(self, event):
#        super(DC_GraphicsLinkChannelItem, self).mouseReleaseEvent(event)
#        linkItem = self.getLinkItem()
#        linkItem.mouseReleaseEvent(event)
#        linkItem.setSelected(True)
        
#    def mouseMoveEvent(self, event):
#        super(DC_GraphicsLinkChannelItem, self).mouseMoveEvent(event)
    
#end class DC_GraphicsRectItem
