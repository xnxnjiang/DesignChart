# -*- coding: utf-8 -*-
"""
Created on Mo May 28 2018

@author: xnjiang
"""

#import sys
#import os


#import xml.dom.minidom as xmldom
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree,Element 

from .dcArchBase import *
from .dcArchModule import *
from .dcArchLink import *

_hierType = "hier"
_debugType = "debug"

class DC_ArchDesign(DC_ArchBase):
    
    def __init__(self, file):
        super().__init__(file, self)
        
        self._type = _hierType
        self._file = file
        self._topModule = None
        self._modules = {}
#        self._ports = {}
#        self._links = {}
        self._bGuiModified = False
        
        self._buildDesignHier(file)

    
    def setGuiModified(self, bModified):
        self._bGuiModified = bModified
    
    def isGuiModified(self):
        return self._bGuiModified
    
    def isDebug(self):
        if self._type == _debugType:
            return True
        else:
            return False
        
    def traverseXml(self, element, parentModule, bLink, nLevel):
        if len(element)>0:
            for child in element:
                tag = child.tag
                attrDict = dict(child.attrib)
                module = None
                if tag == "instance":
                    isLink = False
#                    moduleType = attrDict.get("type")
                    name = attrDict.get("name")
                    hier_name = self._getHierName(attrDict.get("hier_name"))
                    source_port = attrDict.get("source_port")
                    source_module = self._getHierName(attrDict.get("source_module"))
                    dest_port = attrDict.get("dest_port")
                    dest_module = self._getHierName(attrDict.get("dest_module"))
                                
                    module = self._modules.get(hier_name)
                    if module == None:
                        module = self._modules[hier_name] = DC_ArchModule(self, name, parentModule)
                        module.setFullName(hier_name)
                    else:
                        module.setName(name)
                        module.setFullName(hier_name)
                        module.setParent(parentModule)
                        
                    if source_port or source_module or dest_port or dest_module:#link
                        isLink = True
                        link = module.setLink()
                        
                        srcModule = self._modules.get(source_module)
                        port = None
                        if srcModule == None:
                            srcModule = self._modules[source_module] = DC_ArchModule(self, "", None)
                        port = srcModule.getPort(source_port)
                        if port == None:
                            port = srcModule.addPort(source_port, "")
                        link.setSrc(port)
                            
                        destModule = self._modules.get(dest_module)
                        if destModule == None:
                            destModule = self._modules[dest_module] = DC_ArchModule(self, "", None)
                        port = destModule.getPort(dest_port)
                        if port == None:
                            port = destModule.addPort(dest_port, "")
                        link.setDest(port)
                    else:#module
                        if self._topModule == None:
                            self._topModule = module
                    
                    self.traverseXml(child, module, isLink, nLevel+1)
                elif tag == "port":
                    direction = attrDict.get("direction")
                    port_name = attrDict.get("port_name")
                    if len(port_name) > 0:
                        port = parentModule.getPort(port_name)
                        if port == None:
                            port = parentModule.addPort(port_name, direction)
                        else:
                            port.setName(port_name)
                            port.setDirect(direction)
                            port.setFullName(parentModule.getFullName()+":"+port_name)

                        self.traverseXml(child, port, False, nLevel+1)
                elif tag == "gui":
                    parentModule.setGuiData(attrDict)
            else:    
                if bLink: 
                    link = parentModule.setLink()
                    link.updatePort()

    def _buildDesignData(self, file):
        self._xmlTree = tree = ET.parse(file) 
        root = tree.getroot()
        attr = root.attrib
        designType = attr.get("design")
        if designType and len(designType):
            self._type = designType
        self.traverseXml(root, None, False, 0)

    def _getHierName(self, origName):
        hier_name = origName
        if origName != None and origName.startswith("runtime.design_manager."):
            if len(origName)>len("runtime.design_manager."):
                hier_name = origName[len("runtime.design_manager."):]
            else:
                hier_name = ""
        return hier_name
                            
    def saveToFile(self, name):
        root = self._xmlTree.getroot()
        for element in root.iter():
            tag = element.tag
            if tag == "instance":
                self._updateModuleGuiData(element)
        self._xmlTree.write(name)

    def _updateModuleGuiData(self, element):
        tag = element.tag
        if tag == "instance":
            attr = element.attrib
            hier_name = self._getHierName(attr.get("hier_name"))
            module = self._modules.get(hier_name)
            if module:
                for child in element:
                    childTag = child.tag
                    if childTag == "gui":
                        element.remove(child)
                    elif childTag == "port":
                        self._updatePortGuiData(module, child)
                
                #top chart item gui data
                guiData = module.getGuiData(None)
                guiElement = Element("gui", guiData)
                guiElement.text = module.getName()+":top pos"
                element.append(guiElement)
                #child chart item gui data
                guiData = module.getGuiData("child")
                guiElement1 = Element("gui", guiData)
                guiElement1.text = module.getName()+":child pos"
                element.append(guiElement1)
    
    def _updatePortGuiData(self, module, element):
        tag = element.tag
        if tag == "port":
            attr = element.attrib
            portName = attr.get("port_name")
            port = module.getPort(portName)
            if port:
                for child in element:
                    childTag = child.tag
                    if childTag == "gui":
                        element.remove(child)

                #top chart item gui data
                guiData = port.getGuiData(None)
                guiElement = Element("gui", guiData)
                guiElement.text = portName+":top pos"
                element.append(guiElement)
                #child chart item gui data
                guiData = port.getGuiData("child")
                guiElement = Element("gui", guiData)
                guiElement.text = portName+":child pos"
                element.append(guiElement)
        
    def _buildDesignHier(self, file):
        return self._buildDesignData(file)
    
#    def _buildDesignHierByLog(self, file):
#        #runtime.design_manager.top
#        fp = open(file)
#        if fp is not None:
#            module = None
#            while True:
#                sLine = str(fp.readline())
#                if not sLine:#file end
#                    break
#                elif sLine.startswith("[info] Module"):#module info
#                    module = None
#                    sTokens = sLine[len("[info] Module"):].split()
#                    for sToken in sTokens:
#                        if sToken.startswith("runtime.design_manager."):
#                            if len(sToken)>len("runtime.design_manager."):
#                                sFullName = sToken[len("runtime.design_manager."):]
#                                module = self._modules.get(sFullName)
#                            break
#                elif sLine.startswith("[info]  + Port ") and not sLine.startswith("[info]  + Port Count "):#module port info
#                    if module:
#                        sPortTokens = sLine[len("[info]  + Port "):].split()
#                        nToken = len(sPortTokens)
#                        if nToken > 0:
#                            sPortName = sPortTokens[0]
#                            sDirect = "inout"
#                            if nToken > 2:
#                                sDirect = sPortTokens[2]
#                            module.addPort(sPortName, sDirect)
#                elif sLine.startswith("[info] ==== run"):#end design info
#                    break
#                elif sLine.startswith("[info]"):#design hierarchy info
#                    sTokens = sLine[len("[info]"):].split()
#                    for sToken in sTokens:
#                        if sToken.startswith("runtime.design_manager."):
#                            if len(sToken)>len("runtime.design_manager."):
#                                parent =  None
#                                module = None
#                                #hierarchy full name
#                                sFullName = sToken[len("runtime.design_manager."):]
#                                sModuleFullName = ""
#                                for i, sName in enumerate(sFullName.split('.')):
#                                    if 0 == i:#top module
#                                        sModuleFullName = sName
#                                        module = self._topModule#self._topModules.get(sName)
#                                        if module is None:
#                                            module = DC_ArchModule(sName, None)
#                                            self._topModule = module
##                                            self._topModules[sName] = module
#                                            self._modules[sModuleFullName] = module
#                                        parent = module
#                                    else:
#                                        sModuleFullName = sModuleFullName + "." + sName
#                                        module = self._modules.get(sModuleFullName)
#                                        if not module:
#                                            module = DC_ArchModule(sName, parent)
#                                            self._modules[sModuleFullName] = module
#                                        parent = module
#                            break
#            fp.close()
#            
#        #link
#        fp = open(file)
#        if fp is not None:
#            link = None
#            while True:
#                sLine = str(fp.readline())
#                if not sLine:#file end
#                    break
#                if sLine.startswith("[info] Link"):#link info
#                    link = None
#                    sTokens = sLine[len("[info] Line"):].split()
#                    for sToken in sTokens:
#                        if sToken.startswith("runtime.design_manager."):
#                            if len(sToken)>len("runtime.design_manager."):
#                                sFullName = sToken[len("runtime.design_manager."):]
#                                module = self._modules.get(sFullName)
#                                if module:
#                                    link = module.setLink()
#                                    self._links[sFullName] = link
#                            break
#                elif sLine.startswith("[info]  + Source Port :"):#source port of link
#                    if link:
#                        sPortTokens = sLine[len("[info]  + Source Port :"):].split()
#                        nToken = len(sPortTokens)
#                        if nToken > 2:
#                            sPortName = sPortTokens[0]
#                            sFullName = sPortTokens[2]
#                            if sFullName.startswith("runtime.design_manager."):
#                                sFullName = sFullName[len("runtime.design_manager."):]
#                            portModule = self._modules.get(sFullName)
#                            port = portModule.getPort(sPortName)
#                            if port:
#                                link.setSrc(port)
#                elif sLine.startswith("[info]  + Dest   Port :"):#destination port of link
#                    if link:
#                        sPortTokens = sLine[len("[info]  + Dest   Port :"):].split()
#                        nToken = len(sPortTokens)
#                        if nToken > 2:
#                            sPortName = sPortTokens[0]
#                            sFullName = sPortTokens[2]
#                            if sFullName.startswith("runtime.design_manager."):
#                                sFullName = sFullName[len("runtime.design_manager."):]
#                            portModule = self._modules.get(sFullName)
#                            port = portModule.getPort(sPortName)
#                            if port:
#                                link.setDest(port)
#            fp.close()
                            

    def getFile(self):
        return self._file
    
    def getTopModule(self):
        return self._topModule

    def getModule(self, fullName):
        return self._modules.get(fullName)
    
#    def getPort(self, fullName):
#        return slef._ports.get(name)
#        
#    def getLink(self, fullName):
#        return self._links.get(fullName)

