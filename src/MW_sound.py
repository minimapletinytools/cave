import pygame
import os

class soundMan:
    def __init__(self):
        self.soundList = dict()
        pass
    def loadSound(self,filename):
        """loads sound filename and puts it on the flywheel
        
        filename: string"""
        self.soundList[filename] = pygame.mixer.Sound(os.path.join("data",filename))
        
    def play(self, filename):
        if not self.soundList[filename]:
            self.loadSound(filename)
        self.soundList[filename].play()