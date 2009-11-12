import pygame
import MW_entity
import MW_global
from MW_datatypes import *
from MW_constants import *

class EffectMenu(MW_entity.Entity):
    def __init__(self):
        MW_entity.Entity.__init__(self)
        self.effectList = list()
        self.deleteList = []
        self.screen = MW_global.screen
        MW_global.effect = self
        
    def update(self):
        for e in self.effectList:
            e.updateTime()
            e.update()
        self.deleteRoutine()
        
    def text(self,pos,text):
        self.addEffect(EffectText(self,text,pos))
        
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
        self.p = parent
        self.exp = expiration
        self.current = self.exp
        self.pos = position
    def update(self):
        pass
    def updateTime(self):
        self.current -= 1
        if self.current < 1:
            self.deleteSelf()
    def deleteSelf(self):
        self.p.deleteEffect(self)
    def draw(self):
        pass

def getTextEffect(pos,text):
    return EffectText()

class EffectText(Effect):
    def __init__(self,parent,text = "Game Over",position = Vector2d(0,0),expiration = 100, size = MW_global.font[1]):
        Effect.__init__(self,parent,position,expiration)
        self.text = text
        self.size = size
    def draw(self):
        if MW_global.camera.isOnScreen(pygame.Rect(self.pos.x,self.pos.y,1,1)):
            if self.text == "harder":
                MW_global.hardcounter = 1
            MW_global.speech.setSize(self.size,MW_global.font[0])
            MW_global.speech.writeCentered(
                                            self.p.screen,
                                            MW_global.camera.convertCrds(self.pos),
                                            self.text,
                                            COLOR_WHITE
                                            )
