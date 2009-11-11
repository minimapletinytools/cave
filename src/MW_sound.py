import pygame
import os

class soundMan:
    def __init__(self):
        self.soundList = dict()
        pass
    def loadSound(self,filename):
        """loads sound filename and puts it on the flywheel
        
        filename: string"""
        if filename not in self.soundList:
            self.soundList[filename] = pygame.mixer.Sound(os.path.join("data",filename))
            print "loaded sound", filename
        
    def play(self, filename):
        if filename not in self.soundList:
            self.loadSound(filename)
        #print "playing sound",filename
        self.soundList[filename].play()
    
    def stopAll(self):
        pygame.mixer.stop()