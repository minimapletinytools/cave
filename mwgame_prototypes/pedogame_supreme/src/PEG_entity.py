import pygame
from PEG_datatypes import *
import PEG_mainLoop
import PEG_camera
import pedo_lookup
import xml.dom.minidom
import PEG_helpers
from PEG_constants import *

class Entity:
    def __init__(self, position = Rect2d(0,0,0,0)):
        """initialize Entity at position position
        
        position: Vector2d"""
        self.pos = position
        self.vel = Vector2d(0,0)
        
    def teleport(self, position):
        """moves entity to position
        
        position: PEG_datatypes.Vector2d"""
        self.pos.x = position.x
        self.pos.y = position.y
        
    def draw(self):
        pass
    
    def update(self):
        pass
    
    def getxml(self):
        return None
    
class MovingEntity(Entity):
    def __init__(self, position = Rect2d(0,0,0,0)):
        Entity.__init__(self,position)
    def collide(self,e):
        """is called when there is a colision with Entity e
        
        e: Entity that is collided with"""
        pass
        
class StaticEntity(Entity):
    def __init__(self, position = Rect2d(0,0,0,0)):
        Entity.__init__(self,position)

class SolidEntity(StaticEntity):
    def __init__(self, exml):
        """loads a static terrain square
        
        img: string filename of image"""
        tr = Rect2d(0,0,0,0)
        if exml.hasAttribute("x"):
            tr.x = float(exml.getAttribute("x"))
        if exml.hasAttribute("y"):
            tr.y = float(exml.getAttribute("y"))
        if exml.hasAttribute("w"):
            tr.w = float(exml.getAttribute("w"))
        if exml.hasAttribute("h"):
            tr.h = float(exml.getAttribute("h"))
        if exml.hasAttribute("img"):
            self.mainSurface = pygame.image.load(exml.getAttribute("img")).convert()
            self.mainSurface.set_colorkey(COLOR_GREEN,pygame.RLEACCEL)
        
        self.myxml = exml
        StaticEntity.__init__(self,tr)
        
    def draw(self):
        PEG_mainLoop.mainLoop().cam.drawOnScreen(self.mainSurface, self.pos)
    
    def getxml(self):
        self.myxml.setAttribute("x", str(self.pos.x))
        self.myxml.setAttribute("y", str(self.pos.y)) 
        return self.myxml
        
class Editor(Entity):
    def __init__(self, exml = None):
        Entity.__init__(self, Rect2d(0,0,0,0))
        self.cursor = Vector2d(0,0)
        self.topxml = xml.dom.minidom.parse("entities.xml").getElementsByTagName('list')[0]
        self.entityList = self.topxml.getElementsByTagName('entity')
        self.currentItem = 0
        self.activeObject = None
        self.setActive()
        self.mode = "place"
    
    def toggleMode(self):
        if self.mode == "place":
            self.activeObject = None
            self.mode = "edit"
        else:
            if not self.activeObject:
                self.setActive()
            self.mode = "place"
        
    def setActive(self, move = 0):
        if not self.activeObject:
            self.activeObject = pedo_lookup.enTables(self.entityList[self.currentItem])
        else:
            self.currentItem = (self.currentItem + move)%len(self.entityList)
            self.activeObject = pedo_lookup.enTables(self.entityList[self.currentItem])
    
    def setMouse(self):
        self.screenCrds = Vector2d(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        self.cursor = PEG_mainLoop.mainLoop().cam.convertCrds(self.screenCrds)
        self.cursor.x = PEG_helpers.truncateToMultiple(self.cursor.x, TILING_SIZE.x)
        self.cursor.y = PEG_helpers.truncateToMultiple(self.cursor.y, TILING_SIZE.y)
        if self.activeObject:
            self.activeObject.teleport(self.cursor)
    
    def addMode(self):
        self.setMouse()
        for e in PEG_mainLoop.mainLoop().eventList:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_PAGEUP:
                    self.setActive(1)
                if e.key == pygame.K_PAGEDOWN:
                    self.setActive(-1)
                if e.key == pygame.K_SPACE:
                    self.toggleMode()
            if e.type == pygame.MOUSEBUTTONUP:
                PEG_mainLoop.mainLoop().entityList.append(self.activeObject)
                self.activeObject = pedo_lookup.enTables(self.entityList[self.currentItem].cloneNode(True))
        
    def editMode(self):
        self.setMouse()
        for e in PEG_mainLoop.mainLoop().eventList:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self.toggleMode()
            if e.type == pygame.MOUSEBUTTONUP:
                for e in PEG_mainLoop.mainLoop().entityList:
                    if self.cursor == e.pos.getPosition():
                        self.activeObject = e
                        PEG_mainLoop.mainLoop().deleteEntity(e)
                        self.toggleMode()
        
        
    def update(self):
#===============================================================================
#        for e in PEG_mainLoop.mainLoop().eventList:
#            if e.type == pygame.KEYDOWN:
#                if e.key == pygame.K_LEFT:
#                    PEG_mainLoop.mainLoop().cam.moveToRel(Vector2d(-50,0))
#                if e.key == pygame.K_RIGHT:
#                    PEG_mainLoop.mainLoop().cam.moveToRel(Vector2d(50,0))
#                if e.key == pygame.K_UP:
#                    PEG_mainLoop.mainLoop().cam.moveToRel(Vector2d(0,-50))
#                if e.key == pygame.K_DOWN:
#                    PEG_mainLoop.mainLoop().cam.moveToRel(Vector2d(0,50))
#===============================================================================
        if self.mode == "place":
            self.addMode()
        else:
            self.editMode()
            
        #not very efficienty to be looping through this again but who cares
        for e in PEG_mainLoop.mainLoop().eventList:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                PEG_mainLoop.mainLoop().saveState(99)
        
    def draw(self):
        if self.activeObject:
            self.activeObject.draw()
        pass