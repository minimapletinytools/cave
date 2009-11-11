import pygame
from MW_datatypes import *
from MW_constants import *
class Camera:
    def __init__(self, sfc):
        self.width = WIDTH
        self.height = HEIGHT
        self.rect = pygame.Rect(0,0,WIDTH,HEIGHT)
        
        self.p = Vector2d(sfc.get_width()/2-self.width/2,sfc.get_height()/2-self.height/2)
        
#        self.width = sfc.get_width()
#        self.height = sfc.get_height()
#        self.rect = pygame.Rect(0,0,sfc.get_width(),sfc.get_height())
        self.rect.center = self.p.getIntTuple()
        self.screen = sfc
        
    def update(self):
        pass
    
    def drawOnScreen(self, sfc, pos, area = None):
        place = Vector2d(self.rect.x,self.rect.y)
        self.screen.blit(sfc, (pos - place + self.p).getIntTuple(), area)
    
    def isOnScreen(self,rect):
        if self.rect.colliderect(rect):
            return True
        return False
    
    def convertScreenCrds(self, pos):
        return Vector2d(pos.x+self.rect.x, pos.y+self.rect.y) + self.p
    
    def convertCrds(self,pos):
        if isinstance(pos,pygame.Rect):
            ret = pygame.Rect(pos.x,pos.y,pos.w,pos.h)
            ret.x -= self.rect.x
            ret.y -= self.rect.y
            return ret
        elif isinstance(pos,Vector2d):
            return Vector2d(pos.x - self.rect.x, pos.y - self.rect.y) + self.p
        else: #tuple case
            return (pos[0] - self.rect.x + self.p.x, pos[1] - self.rect.y + self.p.y)
    def moveTo(self, target):
        self.rect.center = (target.x,target.y)
    
    def moveToRel(self, displacement):
        self.rect.centerx += displacement.x
        self.rect.centery += displacement.y
