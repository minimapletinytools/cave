import pygame
import MW_entity
import MW_global
from MW_datatypes import *
from MW_constants import *

class EffectMenu(MW_entity.Entity):
    def __init__(self,exml=None):
        MW_entity.Entity.__init__(self,Rect2d(0,0,0,0))
        self.effectList = list()
        self.deleteList = []
        self.screen = MW_global.screen
        #self.effectList.append(EffectNova(self,Vector2d(100,100),4000,500,(255,255,255),pointFunctionSquigglyPoly))
        
    def update(self):
        for e in self.effectList:
            e.updateTime()
            e.update()
            
        self.deleteRoutine()
    def addEffect(self,effect):
        self.effectList.append(effect)
            
    def draw(self):
        for e in self.effectList:
            e.draw()
            
    def deleteEffect(self, e):
        self.deleteList.append(e)
    
    def deleteRoutine(self):
        for e in self.deleteList:
            self.effectList.remove(e)
        self.deleteList = []
    
class Effect:
    def __init__(self,parent, position = Vector2d(0,0), expiration = 0):
        self.startTime = pygame.time.get_ticks()
        self.lastUpdate = pygame.time.get_ticks()
        self.p = parent
        self.exp = expiration
        self.pos = position
    def update(self):
        pass
    def updateTime(self):
        self.lastUpdate = pygame.time.get_ticks()
        if self.lastUpdate > self.startTime + self.exp:
            self.deleteSelf()
    def deleteSelf(self):
        self.p.deleteEffect(self)
    def draw(self):
        pass

class EffectText(Effect):
    def __init__(self,parent,position = Vector2d(0,0),expiration = 999999,text = "Game Over"):
        Effect.__init__(self,parent,position,expiration)
        self.text = text
    def draw(self):
#===============================================================================
#        alpha = 40 + (self.lastUpdate - self.startTime)*200/2000
#        if alpha > 200: alpha = 200
#        pygame.draw.rect(
#                         self.p.screen,
#                         (0,0,0, 255),
#                         pygame.Rect(0,0,800,480),
#                         0
#                         )
#===============================================================================
        MW_global.speech.setSize(15)
        MW_global.speech.writeCentered(
                                        self.p.screen,
                                        Vector2d(400,240),
                                        self.text,
                                        COLOR_WHITE
                                        )
