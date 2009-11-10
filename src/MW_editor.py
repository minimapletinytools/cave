import pygame
import MW_entity
import MW_global
from MW_datatypes import *
from MW_constants import *
import xml.dom.minidom


class WallEditor:
    def __init__(self,matrix):
        self.p = matrix
        self.screenCrds = Vector2d(0,0)
        self.cursor = Vector2d(0,0)
        self.ocursor = Vector2d(0,0)
        self.index = 0
        self.entityRefList = (MW_entity.WallEn,MW_entity.SpikeEn,MW_entity.TorchEn,MW_entity.DoorEn, MW_entity.SwitchEn, MW_entity.RespawnEn, None)
        self.setActive()
        self.mode = "place"
        self.placed = False
        self.mIndex = 0
        self.mX = self.mY = 0
        
    def setMouse(self):
        self.ocursor = self.cursor     
        self.screenCrds = Vector2d(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        self.cursor = MW_global.camera.convertScreenCrds(self.screenCrds)
        self.cursor.x = truncateToMultiple(self.cursor.x, TILING_SIZE.x)
        self.cursor.y = truncateToMultiple(self.cursor.y, TILING_SIZE.y)
        self.mIndex = self.p.getMatrixIndex(self.cursor)
        self.mX, self.mY = self.p.getMatrixPosition(self.cursor)
    def toggleMode(self):
        if self.activeObject == None:
            if self.entityRefList[self.index]:
                self.activeObject = self.entityRefList[self.index]()
            else:
                self.setActive(1)
        else: self.activeObject = None
        
    def setActive(self,offset = 0):
        self.index += offset
        self.index = self.index%len(self.entityRefList)
        if self.entityRefList[self.index] != None:
            self.activeObject = self.entityRefList[self.index]()
            if self.activeObject.getName() == "TorchEn":
                self.activeObject.id = 530
        else: self.activeObject = None
        
    def toggleModeOld(self):
        if self.mode == "place":
            self.mode = "edit"
            self.activeObject = None
        else:
            self.mode = "place"
            self.activeObject = MW_entity.WallEn()
            self.activeObject.teleport(self.cursor)
    
    def addMode(self):
        self.setMouse()
        if not self.ocursor.__eq__( self.cursor ):
            self.placed = False
        if self.activeObject:
            self.activeObject.teleport(self.cursor)
        for e in MW_global.eventList:
            if e.type == pygame.MOUSEBUTTONDOWN or (e.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]) and not self.placed:
                self.placed = True
                self.appendObject()
            if e.type == pygame.MOUSEBUTTONUP:
                self.placed = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_PAGEUP:
                    self.setActive(1)
                if e.key == pygame.K_PAGEDOWN:
                    self.setActive(-1)
                if e.key == pygame.K_SPACE:
                    self.toggleMode()
        
    def appendObject(self):
        #rint "wall appended at", self.activeObject.pos
        self.p.addEn(self.activeObject,self.cursor)
        if self.mode == "place":
            self.setActive(0)
            if self.activeObject:
                self.activeObject.teleport(self.cursor)
        
    def update(self):
        for e in MW_global.eventList:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    self.p.printXML()
                if e.key == pygame.K_KP4:
                    MW_global.camera.moveToRel(Vector2d(-100,0))
                if e.key == pygame.K_KP6:
                    MW_global.camera.moveToRel(Vector2d(100,0))
                if e.key == pygame.K_KP8:
                    MW_global.camera.moveToRel(Vector2d(0,-100))
                if e.key == pygame.K_KP2:
                    MW_global.camera.moveToRel(Vector2d(0,100))
        self.addMode()
        
    def draw(self):
        if self.activeObject and self.mode == "place":
            self.activeObject.draw()
        pygame.draw.rect(MW_global.screen, (255,255,255),MW_global.camera.convertCrds(pygame.Rect(self.cursor.x,self.cursor.y,TILING_SIZE.x,TILING_SIZE.y)),1)
        MW_global.speech.setSize(8)
        #MW_global.speech.writeText(MW_global.screen, Vector2d(10,10), "x: " + str(self.mX) + "  y: " + str(self.mY) + "  index: " + str(self.mIndex), COLOR_WHITE)
        MW_global.speech.writeText(MW_global.screen, Vector2d(10,10), "x: " + str(self.cursor.x) + "  y: " + str(self.cursor.y) + "  index: " + str(self.mIndex), COLOR_WHITE)
        
#import MW_lookup
class DooEditor:
    def __init__(self, doodadcontainer):
        self.p = doodadcontainer
        self.cursor = Vector2d(0,0)
        self.ocursor = Vector2d(0,0)
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
            self.activeObject = MW_lookup.enTables(self.entityList[self.currentItem])
        else:
            self.currentItem = (self.currentItem + move)%len(self.entityList)
            self.activeObject = MW_lookup.enTables(self.entityList[self.currentItem])
    
    def setMouse(self):
        self.ocursor = self.cursor     
        self.screenCrds = Vector2d(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        self.cursor = MW_global.camera.convertScreenCrds(self.screenCrds)
        self.cursor.x = truncateToMultiple(self.cursor.x, TILING_SIZE.x)
        self.cursor.y = truncateToMultiple(self.cursor.y, TILING_SIZE.y)
        self.activeObject.teleport(self.cursor)
    
    def addMode(self):
        self.setMouse()
        
        for e in MW_global.eventList:
            if e.type == pygame.MOUSEBUTTONDOWN:
                clickEvent = True
                ret = self.activeObject.sendClick(e)
                if ret != None:
                    print "object ", self.activeObject, " appended"
                    self.p.enList.append(ret)
                    self.activeObject = MW_lookup.enTables(self.entityList[self.currentItem].cloneNode(True))
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_PAGEUP:
                    self.setActive(1)
                if e.key == pygame.K_PAGEDOWN:
                    self.setActive(-1)
                if e.key == pygame.K_SPACE:
                    self.toggleMode()
#CAN DELETE
#===============================================================================
#            if e.type == pygame.MOUSEBUTTONUP:
#                PEG_mainLoop.mainLoop().entityList.append(self.activeObject)
#                self.activeObject = pedo_lookup.enTables(self.entityList[self.currentItem].cloneNode(True))
#==============================================================================
        if pygame.mouse.get_pressed()[0]:
            if not self.ocursor.__eq__(self.cursor):
                for e in PEG_mainLoop.mainLoop().entityList:
                    if e.getRect().collidepoint(self.cursor.getIntTuple()):
                            self.p.deleteEntity(e)
                self.appendObject()
            
    def appendObject(self):
        self.p.enList.append(self.activeObject)
        self.activeObject = MW_lookup.enTables(self.entityList[self.currentItem].cloneNode(True))
        
    def editMode(self):
        self.setMouse()
        for e in MW_global.eventList:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self.toggleMode()
            if e.type == pygame.MOUSEBUTTONUP:
                for e in MW_global.entityList:
                    if e.getRect().collidepoint(self.cursor.getIntTuple()):
                        self.activeObject = e
                        self.p.deleteEntity(e)
                        self.toggleMode()
        
        
    def update(self):
        for e in MW_global.eventList:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_KP4:
                    MW_global.camera.moveToRel(Vector2d(-50,0))
                if e.key == pygame.K_KP6:
                    MW_global.camera.moveToRel(Vector2d(50,0))
                if e.key == pygame.K_KP8:
                    MW_global.camera.moveToRel(Vector2d(0,-50))
                if e.key == pygame.K_KP2:
                    MW_global.camera.moveToRel(Vector2d(0,50))
        if self.mode == "place":
            self.addMode()
        else:
            self.editMode()
            
        for e in MW_global.eventList:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                pass
                #todo WRITE XML
        
    def draw(self):
        if self.activeObject:
            self.activeObject.draw()
        pygame.draw.rect(MW_global.screen, (255,255,255),MW_global.camera.convertCrds(pygame.Rect(self.cursor.x,self.cursor.y,TILING_SIZE.x,TILING_SIZE.y)),1)
        
        
        
