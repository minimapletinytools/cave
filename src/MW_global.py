import pygame
import MW_camera
import MW_image
import MW_sound
import MW_speech
import MW_animator
import os,sys
from MW_constants import *

print "version,",sys.version

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
#screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
screen = pygame.display.set_mode((SCREEN_SIZE),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.NOFRAME)
#print "flags", screen.get_flags()
pygame.mouse.set_visible(0)
camera = MW_camera.Camera(screen)
imagewheel = MW_image.ImageWheel()
animwheel = MW_animator.AnimatorWheel()
xmlwheel = MW_animator.XMLWheel()
sound = MW_sound.soundMan()
speech = MW_speech.Speech()
soundMap = dict()
soundMap['light'] = "light08.wav"
sound.loadSound(soundMap['light'])
stickyswitchlist = [2123,3]
stickydoorlist = [] #sticky doors do not open
controller = None
matrixcontainer = None
eventList = None
switchdict = dict()
spawndict = dict()
frame = 0

def getMatrixContainer():
    return matrixcontainer
