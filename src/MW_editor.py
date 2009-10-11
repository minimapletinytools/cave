import pygame
import MW_entity
import MW_global
from MW_datatypes import *
from MW_constants import *
import xml.dom.minidom


class WallEditor():
    def __init__(self,matrix):
        self.p = matrix
        self.cursor = Vector2d(0,0)
        self.ocursor = Vector2d(0,0)
        self.activeObject = MW_entity.WallEn()
        self.mode = "place"
        self.placed = False
        
    def setMouse(self):
        self.ocursor = self.cursor     
        self.screenCrds = Vector2d(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        self.cursor = MW_global.camera.convertScreenCrds(self.screenCrds)
        self.cursor.x = truncateToMultiple(self.cursor.x, TILING_SIZE.x)
        self.cursor.y = truncateToMultiple(self.cursor.y, TILING_SIZE.y)
    
    def toggleMode(self):
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
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                self.toggleMode()
        
    def appendObject(self):
        #rint "wall appended at", self.activeObject.pos
        self.p.addEn(self.activeObject,self.cursor)
        if self.mode == "place":
            self.activeObject = MW_entity.WallEn()
            self.activeObject.teleport(self.cursor)
        
    def update(self):
        for e in MW_global.eventList:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    self.p.printXML()
                if e.key == pygame.K_KP4:
                    MW_global.camera.moveToRel(Vector2d(-40,0))
                if e.key == pygame.K_KP6:
                    MW_global.camera.moveToRel(Vector2d(40,0))
                if e.key == pygame.K_KP8:
                    MW_global.camera.moveToRel(Vector2d(0,-40))
                if e.key == pygame.K_KP2:
                    MW_global.camera.moveToRel(Vector2d(0,40))

        self.addMode()
        
    def draw(self):
        if self.activeObject and self.mode == "place":
            self.activeObject.draw()
        pygame.draw.rect(MW_global.screen, (255,255,255),MW_global.camera.convertCrds(pygame.Rect(self.cursor.x,self.cursor.y,TILING_SIZE.x,TILING_SIZE.y)),1)
        

class DooEditor():
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
            self.activeObject = pedo_lookup.enTables(self.entityList[self.currentItem])
        else:
            self.currentItem = (self.currentItem + move)%len(self.entityList)
            self.activeObject = pedo_lookup.enTables(self.entityList[self.currentItem])
    
    def setMouse(self):
        self.ocursor = self.cursor        
        self.screenCrds = Vector2d(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        self.cursor = PEG_mainLoop.mainLoop().cam.convertScreenCrds(self.screenCrds)
        self.cursor.x = PEG_helpers.truncateToMultiple(self.cursor.x, TILING_SIZE.x)
        self.cursor.y = PEG_helpers.truncateToMultiple(self.cursor.y, TILING_SIZE.y)
    
    def addMode(self):
        self.setMouse()
        if self.activeObject:
            self.activeObject.updateCursor(self.cursor)
        
        for e in PEG_mainLoop.mainLoop().eventList:
            if e.type == pygame.MOUSEBUTTONDOWN:
                clickEvent = True
                ret = self.activeObject.sendClick(e)
                if ret != None:
                    print "object ", self.activeObject, " appended"
                    PEG_mainLoop.mainLoop().entityList.append(ret)
                    self.activeObject = pedo_lookup.enTables(self.entityList[self.currentItem].cloneNode(True))
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
            try:
                if self.activeObject.repeatable:
                    if self.ocursor != self.cursor:
                        for e in PEG_mainLoop.mainLoop().entityList:
                                if e.pos.getSDLRect().collidepoint(self.cursor.getIntTuple()):
                                    #TODO should check additional conditions for deleting things
                                    try: 
                                        if not e.drawOver or e.repeatable: #TEMPORARY CODE
                                            PEG_mainLoop.mainLoop().deleteEntity(e)
                                    except: pass
                        self.appendObject()
            except: pass
            
    def appendObject(self):
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
                    if e.pos.getSDLRect().collidepoint(self.cursor.getIntTuple()):
                        self.activeObject = e
                        PEG_mainLoop.mainLoop().deleteEntity(e)
                        self.toggleMode()
        
        
    def update(self):
        for e in PEG_mainLoop.mainLoop().eventList:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_KP4:
                    PEG_mainLoop.mainLoop().cam.moveToRel(Vector2d(-50,0))
                if e.key == pygame.K_KP6:
                    PEG_mainLoop.mainLoop().cam.moveToRel(Vector2d(50,0))
                if e.key == pygame.K_KP8:
                    PEG_mainLoop.mainLoop().cam.moveToRel(Vector2d(0,-50))
                if e.key == pygame.K_KP2:
                    PEG_mainLoop.mainLoop().cam.moveToRel(Vector2d(0,50))
        if self.mode == "place":
            self.addMode()
        else:
            self.editMode()
            
        #return 0 means propogate input down
        #return 1 means taken
        #return 2 means I'm done, put me down!
        for e in PEG_mainLoop.mainLoop().eventList:
            if self.activeObject:
                n = self.activeObject.sendKey(e)
                if n == 0:
                    #propogate
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                        PEG_mainLoop.mainLoop().saveState(99)
                elif n == 2:
                    self.appendObject() 
        
    def draw(self):
        if self.activeObject:
            self.activeObject.draw()
        pygame.draw.rect(PEG_mainLoop.mainLoop().screen, (255,255,255),pygame.Rect(self.screenCrds.x, self.screenCrds.y, 2, 2))
        
        