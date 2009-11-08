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
screen = pygame.display.set_mode((SCREEN_SIZE),DISPLAY_FLAGS)
#print "flags", screen.get_flags()
pygame.mouse.set_visible(0)
camera = MW_camera.Camera(screen)
imagewheel = MW_image.ImageWheel()
animwheel = MW_animator.AnimatorWheel()
xmlwheel = MW_animator.XMLWheel()
sound = MW_sound.soundMan()
speech = MW_speech.Speech()
controller = None
matrixcontainer = None
effectentity = None
eventList = None
switchdict = dict()
spawndict = dict()
frame = 0

state = "PASS"

#scripted constants

soundMap = dict()
soundMap['light'] = "light08.wav"
soundMap['switch'] = "switch01.wav"
sound.loadSound(soundMap['light'])
stickyswitchlist = set([2123,3,23299,28566])
stickydoorlist = set() #sticky doors do not open
dooropenlist = set() #open automatically
torchStateMap = { 501:"INSTRUCTION1", 502:"INSTRUCTION2", 503:"SYMBOL1", 504:"SYMBOL2", 510: "BLANK", 520: "BLANK" }
torchonlist = set([23125]) #23909 pit torch, turn on with scrpiting
torchofflist = set()

def getMatrixContainer():
    return matrixcontainer
