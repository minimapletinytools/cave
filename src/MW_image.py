import pygame
import MW_global
from MW_constants import *

class ImageWheel:
    def __init__(self):
        self.iMap = dict()
    def loadImage(self,filename):
        if filename not in self.iMap:
            self.iMap[filename] = pygame.image.load(filename).convert()
            self.iMap[filename].set_colorkey(COLOR_KEY)
            self.flipImage(filename)
    def flipImage(self,identifier):
        """only to be used by self.loadImage"""
        self.iMap[identifier+"_flip"] = pygame.transform.flip(self.iMap[identifier],True,False)
        
    def getImage(self,identifier):
        if identifier in self.iMap:
            return self.iMap[identifier]
        else: return None
    def getFlipImage(self,identifier):
        if identifier+"_flip" in self.iMap:
            return self.iMap[identifier+"_flip"]
        else: return None
        