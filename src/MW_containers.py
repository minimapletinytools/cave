import pygame
import xml.dom.minidom
import MW_global
import MW_editor
import MW_xml
import MW_entity
from MW_datatypes import *
from MW_constants import *

class SuperContainer:
    def __init__(self):
        self.duck = "quack"
        pass

class MatrixContainer(SuperContainer):
    def __init__(self,dim):
        SuperContainer.__init__(self)
        self.width = dim[0]
        self.height = dim[1]
        self.startPos = Vector2d(-500,-500)
        self.wList = list()
        for e in range(self.width*self.height):
            self.wList.append(None)
        self.length = len(self.wList)
        self.edit = True
        self.editor = MW_editor.WallEditor(self)
        
        self.readXML(xml.dom.minidom.parse("testlevel.xml"))
    def update(self):
        if self.edit:
            self.editor.update()
    def draw(self):
        if self.edit: 
            self.editor.draw()
            
        rect = self.getMatrixRect(MW_global.camera.rect)
        for r in range(rect.h):
            for c in range(rect.w):
                e = self.wList[self.getIndex((rect.x + c),(rect.y + r))]
                if e:
                    e.draw()
    def addEn(self,en,pos):
        print en, "added"
        index = self.getIndex(*self.getMatrixPosition(pos))
        #print pos, TILING_SIZE, self.getMatrixPosition(pos)
        self.wList[index] = en
    def getWallRects(self,rect):
        ret = list()
        for r in range(rect.h):
            for c in range(rect.w):
                e = self.wList[self.getIndex((rect.x + c),(rect.y + r))]
                if e:
                    ret.append(e.getRect())
        return ret
            
        
    def setRectWalls(self,rect):
        rect = rect.inflate(TILING_SIZE.x,TILING_SIZE.y)
        for r in range(rect.h):
            for c in range(rect.w):
                self.setWall(self.getIndex((rect.x + c),(rect.y + r)))
                
    def setAllWalls(self):
        for i in range(self.length):
            if self.wList[i]:
                self.setWall(self,getCart(i))
            
    def setWall(self, *args):
        if len(args == 1): x,y = args[0].x, args[0].y
        else: x,y = args[0],args[1]
        l = r = t = b = False
        if self.isInBound(x+1, y) and self.wList[self.getIndex(x+1,y)]: r = True
        if self.isInBound(x-1, y) and self.wList[self.getIndex(x-1,y)]: l = True
        if self.isInBound(x, y+1) and self.wList[self.getIndex(x,y+1)]: b = True
        if self.isInBound(x, y-1) and self.wList[self.getIndex(x,y-1)]: t = True
        #TODO decide how we want to generate tiles
    def isInBound(self,x,y):
        if x + y*self.width < self.length: return True
        return False
    def getIndex(self,x,y):
        i = x + y*self.width
        if i < self.length: return i
        else: raise Exception("out of index")
    def getCart(self,index):
        return index%self.width, int(index/self.width)
    def getMatrixRect(self,rect): #used for converting camera rect to matrix rect
        x,y = self.getMatrixPosition(rect)
        w = int(rect.w/TILING_SIZE.x)*2
        h = int(rect.h/TILING_SIZE.y)*2
        return pygame.Rect(x,y,w,h).inflate(1,1)
    def getScreenPosition(self,x,y):    #converts matrix coordinates to screen coordinates
        return Vector2d(self.startPos.x + x*TILING_SIZE.x, self.startPos.y + y*TILING_SIZE.y)
    def getMatrixPosition(self,pos):
        x = int((pos.x-self.startPos.x)/TILING_SIZE.x)
        y = int((pos.y-self.startPos.y)/TILING_SIZE.y)
        return x,y
    def getMatrixIndex(self,pos):
        return self.getIndex(*self.getMatrixPosition(pos))    
    def callList(self,rect,fcn,args=None):
        for r in range(rect.h):
            for c in range(rect.w):
                if args==None:
                    fcn(self.wList[(rect.x+c) + (rect.y + r)*self.width])
                else:
                    fcn(self.wList[(rect.x+c) + (rect.y + r)*self.width],*args)
    
    def printXML(self):
        exml = xml.dom.minidom.parseString("<p><walls></walls></p>").getElementsByTagName("walls")[0]
        c = xml.dom.minidom.parseString(
                                        "<p><size w=\""
                                        +str(self.width)+"\" h=\""
                                        +str(self.height)+"\" x=\""
                                        +str(self.startPos.x)+"\" y=\"" 
                                        +str(self.startPos.y)+"\"/></p>"
                                        ).getElementsByTagName("size")[0]

        exml.appendChild(c)
        for i in range(len(self.wList)):
            if self.wList[i] != None:
                exml.appendChild(xml.dom.minidom.parseString("<p><wall i=\""
                                                     +str(i)+"\" /></p>").getElementsByTagName("wall")[0])
        print exml.toxml()
    def readXML(self,exml):
        size = exml.getElementsByTagName("size")[0]
        self.startPos = Vector2d(int(size.getAttribute("x")),int(size.getAttribute("y")))
        self.width = int(size.getAttribute("w"))
        self.height = int(size.getAttribute("h"))
        self.wList = list()
        for e in range(self.width*self.height):
            self.wList.append(None)
        self.length = len(self.wList)
        for e in exml.getElementsByTagName("wall"):
            index = int(e.getAttribute("i"))
            self.wList[index] = MW_entity.WallEn()
            self.wList[index].teleport(self.getScreenPosition(index%self.width,int(index/self.width)))
        
        pass
    
class DoodadContainer(SuperContainer):
    def __init__(self):
        SuperContainer.__init__(self)
        self.enList = list()
    def update(self):
        for e in self.enList:
            e.update()
    def draw(self):
        for e in self.enList:
            e.draw()
    def destroy(self):
        delList = list()
        for e in self.enList:
            if e.destroy:
                delList.append(e)
        for e in delList:
            self.enList.remove(e)
        del delList