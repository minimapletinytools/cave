import pygame
from MW_datatypes import *
class Camera:
    def __init__(self, sfc):
        self.width = sfc.get_width()
        self.height = sfc.get_height()
        self.rect = pygame.Rect(0,0,sfc.get_width(),sfc.get_height())
        self.rect.center = (0,0)
        self.screen = sfc
        
    def drawOnScreen(self, sfc, pos, area = None):
        place = Vector2d(self.rect.x,self.rect.y)
        self.screen.blit(sfc, (pos - place).getIntTuple(), area)
    
    def isOnScreen(self,rect):
        if self.rect.colliderect(rect.getSDLRect()):
            return True
        return False     
    
    def convertScreenCrds(self, pos):
        return Vector2d(pos.x+self.rect.x, pos.y+self.rect.y)
    
    def convertCrds(self,pos):
        if isinstance(pos,pygame.Rect):
            ret = pygame.Rect(pos.x,pos.y,pos.w,pos.h)
            ret.x -= self.rect.x
            ret.y -= self.rect.y
            return ret
        elif isinstance(pos,Vector2d):
            return Vector2d(pos.x - self.rect.x, pos.y - self.rect.y)
        else: #tuple case
            return (pos[0] - self.rect.x, pos[1] - self.rect.y)    
    def moveTo(self, target):
        self.rect.center = (target.x,target.y)
    
    def moveToRel(self, displacement):
        self.rect.centerx += displacement.x
        self.rect.centery += displacement.y
