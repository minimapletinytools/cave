from MW_datatypes import *

DISPLAY_FLAGS = pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.NOFRAME
#DISPLAY_FLAGS = pygame.FULLSCREEN
gamemode = 2
if gamemode == 1:
    SCREEN_SIZE = WIDTH, HEIGHT = 641,480
    LIGHTING = 1
    CAMERA_MODE = "force"
elif gamemode == 2:
    SCREEN_SIZE = WIDTH, HEIGHT = 1200,800
    LIGHTING = 0
    CAMERA_MODE = "nothing"
elif gamemode == 3:
    SCREEN_SIZE = WIDTH, HEIGHT = 800,600
    LIGHTING = 0
    CAMERA_MODE = "nothing"
elif gamemode == 4:
    SCREEN_SIZE = WIDTH, HEIGHT = 1200,800
    LIGHTING = 0
    CAMERA_MODE = "force"

FRAMERATE = 25
MSPERFRAME = 1000/FRAMERATE
TILING_SIZE = Vector2d(20,20)


#colors
COLOR_RED = 255,0,0
COLOR_WHITE = 255,255,255
COLOR_LIGHT_BLUE = 127,127,255
COLOR_BLACK = 0,0,0
COLOR_GREEN = 0,255,0
COLOR_DARK = 100,100,100
COLOR_KEY = COLOR_BLACK

#game constants
TORCH_RADIUS = 100,150
PLAYER_LIGHT_RADIUS = 50,75
MAN_START = Vector2d(-500,-100)
WOMAN_START = Vector2d(-530,-120)

#engine constants
dirMap = dict()
dirMap["RIGHT"] = 1
dirMap["LEFT"] = -1
