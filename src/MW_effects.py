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
        self.p = parent
        self.exp = expiration
        self.current = self.expiration
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
    def __init__(self,parent,position = Vector2d(0,0),expiration = 100,text = "Game Over", size = 15):
        Effect.__init__(self,parent,position,expiration)
        self.text = text
        self.size = size
    def draw(self):
        MW_global.speech.setSize(self.size)
        MW_global.speech.writeCentered(
                                        self.p.screen,
                                        Vector2d(400,240),
                                        self.text,
                                        COLOR_WHITE
                                        )
