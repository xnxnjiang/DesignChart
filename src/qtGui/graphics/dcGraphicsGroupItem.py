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

class DC_GraphicsGroupItem(QGraphicsItemGroup, DC_GraphicsBaseItem):

    def __init__(self, parentItem=None):
        super(DC_GraphicsItemGroup, self).__init__(parentItem)
        self._initItem("GroupItem", "", None)
   
#end class DC_GraphicsItemGroup
