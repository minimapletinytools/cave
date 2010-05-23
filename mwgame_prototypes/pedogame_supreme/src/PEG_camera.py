from PEG_constants import *
from PEG_datatypes import *
import PEG_mainLoop

class Camera:
    def __init__(self, sfc):
        self.pos = Vector2d(0,0)
        self.screen = sfc
    
    def drawOnScreen(self, sfc, pos, area = None):
        """draws onto self.screen at camera coordinates pos
        
        sfc: pygame.Surface
        pos: PEG_datatypes.Vector2d"""
        PEG_mainLoop.mainLoop().screen.blit(sfc, (pos+self.pos).getSDLRect(), area)
    
    def convertCrds(self, pos):
        return Vector2d(pos.x-self.pos.x, pos.y-self.pos.y)
    
    def moveTo(self, target):
        self.pos = target
    
    def moveToRel(self, displacement):
        self.pos += displacement
    
    def smoothTo(self, target, rate = 10):
        self.pos.moveTowards(position, (target-self.pos).distance()/rate )
