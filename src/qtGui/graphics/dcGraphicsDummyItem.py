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

from .dcGraphicsBaseItem import *

class DC_GraphicsDummyItem(QGraphicsItem, DC_GraphicsBaseItem):

    def __init__(self, parentItem=None):
        super(DC_GraphicsDummyItem, self).__init__(parentItem)
        self._initItem("DummyItem", "", None)

    def boundingRect(self):
        return QRectF(0, 0, 0, 0)

    def paint(self, painter, option, widget):
        return
#end class DC_GraphicsDummyItem
