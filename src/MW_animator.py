import pygame
import xml.dom.minidom
import MW_xml
import MW_image
import MW_global
import random
import os
from MW_datatypes import *
from MW_constants import *

class FrameNode:
    def __init__(self, wxml, id, createdNodeList = list()):
        
        exml = MW_xml.getChildNodeWithAttribute(wxml, "frame", "id", id)
        
        createdNodeList.append(self)
        #set up important data
        self.id = exml.getAttribute("id")
        
        if exml.hasAttribute("state"):
            self.state = exml.getAttribute("state")
        else:
            print exml, " has no \"state\" attribute, setting to default DEFAULT"
            self.state = "DEFAULT"
            
        if exml.hasAttribute("time"):
            self.time = int(exml.getAttribute("time"))
        else:
            print exml, " has no \"time\" attribute, setting to default 0"
            self.time = 0
            
        if MW_xml.hasAttributes(exml, ("x","y")):
            self.iRect = pygame.Rect(
                                       int(exml.getAttribute("x")),
                                       int(exml.getAttribute("y")),
                                       int(exml.getAttribute("w")),
                                       int(exml.getAttribute("h"))
                                       )
        else:
            self.iRect = pygame.Rect(0,0,0,0)
            print exml, " has no x y w h attributes, setting iRect2d default", self.iRect
            
        
        #self.dVect2d
        if MW_xml.hasAttributes(exml, ("dx","dy")):
            self.dVect2d = Vector2d(exml.getAttribute("dx"),exml.getAttribute("dy"))
        else:
            self.dVect2d = Vector2d(0,0)
            #print exml, " has no dx dy attributes, setting dVect2d default", self.dVect2d
        
        #self.hRect2d
        if MW_xml.hasAttributes(exml, ("hx","hy","hw","hh")):
            self.hRect = pygame.Rect(
                                       int(exml.getAttribute("hx")),
                                       int(exml.getAttribute("hy")),
                                       int(exml.getAttribute("hw")),
                                       int(exml.getAttribute("hh"))
                                       )
        else:
            self.hRect = pygame.Rect(0,0,self.iRect.w,self.iRect.h)
            #print exml, " has no hx hy hw hh attributes, setting hRect2d to default", self.hRect
        
        #set up data dict, grab data from exml
        dataNode = MW_xml.getChildNode(exml, "data")
        if dataNode:
            self.data = MW_xml.getAttributeMap(dataNode)
        else: self.data = dict()
        
        #set up next node dict, get data from xml, recursively create new ones, etc..
        self.next = dict()
        self.nextTime = dict()
        for e in exml.getElementsByTagName("next"):
            if e.hasAttribute("time"):
                self.nextTime[e.getAttribute("state")] = int(e.getAttribute("time"))
            else:
                self.nextTime[e.getAttribute("state")] = self.time
            flag = True
            for f in createdNodeList:
                if f.id == e.getAttribute("id"):
                    self.next[e.getAttribute("state")] = f
                    flag = False
                    break
            if flag:
                self.next[e.getAttribute("state")] = FrameNode(wxml,e.getAttribute("id"), createdNodeList)
    def __str__(self):
        return "Framenode " + str(self.id) + " state " + str(self.state)
    
class Animator:
    """create one instance of me for each animation graph"""
    def __init__(self,exml):
        """pass exml node at top of graph"""
        if MW_xml.hasAttributes(exml, ("name","file")):
            imageList = exml.getAttribute("file").split(" ")
            self.file = imageList[random.randint(0,len(imageList))-1]
            self.name = exml.getAttribute("name")
        else:
            raise Exception("can not file file")        
        
        MW_global.imagewheel.loadImage(self.file)
        self.image = MW_global.imagewheel.getImage(self.file)
        self.flipImage = MW_global.imagewheel.getFlipImage(self.file)
        self.activeNode = FrameNode(exml,1,list())
        self.last = 0
        self.time = 0
        self.dir = "RIGHT"
        self.state = "DEFAULT"
        
    def getNextState(self):
        if self.state in self.activeNode.next:
            return self.state
        elif "DEFAULT" in self.activeNode.next:
            return "DEFAULT"
        else:
            print "no", self.state, "or DEFAULT path found"
            return self.activeNode.next.keys()[0]
    def forceUpdate(self):
        self.activeNode = self.activeNode.next[self.getNextState()]   

    def update(self):
        """advance one frame"""
        while self.time - self.last >= self.activeNode.nextTime[self.getNextState()]:
            self.last += self.activeNode.nextTime[self.getNextState()]
            self.activeNode = self.activeNode.next[self.getNextState()]   
        self.time += 1
    def getVelData(self):
        x = y = 0
        if 'velx' in self.activeNode.data:
            x = float(self.activeNode.data['velx'])
        if 'vely' in self.activeNode.data:
            y = float(self.activeNode.data['vely'])
        if self.dir == "RIGHT":
            return Vector2d(x,y)
        else: return Vector2d(-x,y)
    def getDrawRect(self):
        if self.dir == "RIGHT":
            return self.activeNode.iRect
        else:
            return reflectRect(self.activeNode.iRect,self.image.get_width()/2)
    def getDrawOffset(self):
        return self.activeNode.dVect2d
    def getHitRect(self,pos):
        if self.dir == "RIGHT":
            return self.activeNode.hRect
        else:
            return reflectRect(self.activenode.hRect,self.activeNode.iRect.w/2)
    def getImage(self):
        if self.dir == "RIGHT":
            return self.image
        else:
            return self.flipImage       
    def drawAt(self,pos):
        MW_global.screen.blit(
                              MW_global.imagewheel.getImage(self.file),
                              (pos-self.activeNode.dVect2d).getIntTuple(),
                              self.activeNode.iRect
                              )
    def printGraph(self):
        """debugging, prints tree"""
        printGraph(self.activeNode)

def printGraph(node,visited=list()):
    if visited.count(node) == 0:
        visited.append(node)
        print node
        for e in node.next.values():
            printGraph(e,visited)
            
