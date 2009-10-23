import pygame
import MW_camera
import MW_image
import MW_sound
import os
from MW_constants import *
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
#screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
screen = pygame.display.set_mode((SCREEN_SIZE),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.NOFRAME)
#print "flags", screen.get_flags()
pygame.mouse.set_visible(0)
camera = MW_camera.Camera(screen)
imagewheel = MW_image.ImageWheel()
sound = MW_sound.soundMan()
soundMap = dict()
soundMap['light'] = os.path.join("data","light07.wav")
sound.loadSound(soundMap['light'])
controller = None
matrixcontainer = None
eventList = None
switchdict = dict()
frame = 0

def getMatrixContainer():
    return matrixcontainer
