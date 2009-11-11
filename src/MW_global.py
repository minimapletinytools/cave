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
screen = None
if isFull:
    screen = pygame.display.set_mode(pygame.display.list_modes()[0],DISPLAY_FLAGS)
    #screen = pygame.Surface((SCREEN_SIZE))
else:
    screen = pygame.display.set_mode(SCREEN_SIZE, DISPLAY_FLAGS)
pygame.display.set_caption("game")
pygame.display.set_icon(pygame.image.load(os.path.join("data","icon3.bmp")).convert())
pygame.mouse.set_visible(0)
camera = MW_camera.Camera(screen)
imagewheel = MW_image.ImageWheel()
animwheel = MW_animator.AnimatorWheel()
xmlwheel = MW_animator.XMLWheel()
sound = MW_sound.soundMan()
speech = MW_speech.Speech()
controller = None
matrixcontainer = None
effect = None
eventList = None
switchdict = dict()
spawndict = dict()
frame = 0

state = "PASS"
microstate = "PASS"
microstate2 = "PASS"
finalstate = "PASS"
hangstate = False
judgementstate = False

freezetime = 0
freezetime2 = 0

#scripted constants
font = "visitor2.ttf",10
font = "visitor2.ttf",15
#font = "FFFATLAN.ttf",8
#font = "FFFATLAN.ttf",16
soundMap = dict()
soundMap['light'] = "light08.wav"
soundMap['switch'] = "switch01.wav"
soundMap['static'] = "static03.wav"
sound.loadSound(soundMap['light'])
stickyswitchlist = set([2123,3,23299,28566,11732])
stickydoorlist = set() #sticky doors do not open
dooropenlist = set() #open automatically
torchStateMap = { 301: "LIGHT", 401: "I1", 402: "I2", 403: "I3", 404: "I4", 405: "I5", 406: "I6", 501:"INSTRUCTION1", 502:"INSTRUCTION2", 503:"SYMBOL1", 504:"SYMBOL2", 510: "BLANK", 520: "BLANK", 530: "GRASS", 540: "HISC", 541: "HERC", 542: "BLANK", 3881: "Z" }
torchonlist = set([3860])
torchofflist = set([503,504,510,3881,530,0,540,541,542,22548])

def getMatrixContainer():
    return matrixcontainer
