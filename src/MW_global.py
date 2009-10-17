import pygame
import MW_camera
import MW_image
from MW_constants import *
pygame.init()
#screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
screen = pygame.display.set_mode((SCREEN_SIZE),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.NOFRAME)
print "flags", screen.get_flags()
#pygame.mouse.set_visible(0)
camera = MW_camera.Camera(screen)
imagewheel = MW_image.ImageWheel()
controller = None
matrixcontainer = None
eventList = None
switchdict = dict()
frame = 0

def getMatrixContainer():
    return matrixcontainer
