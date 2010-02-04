import pygame
import MW_global
import MW_controller
import sys
from MW_constants import *
from MW_datatypes import *

import MW_camera
import MW_image
import MW_sound
import MW_speech
import MW_animator

mwc = MW_controller.ControllerController()
#mwc = MW_controller.oldController()
last = pygame.time.get_ticks()

while 1:
    #if time expired
    
    
    if(pygame.time.get_ticks() - last > MSPERFRAME):
        while(pygame.time.get_ticks() - last > MSPERFRAME):
            last += MSPERFRAME
        MW_global.screen.fill((0,0,0))
        t1 = pygame.time.get_ticks()
        mwc.loop()
        MW_global.frame += 1
        if pygame.time.get_ticks()%200 == 1:
            pass
            #print "cycle time", pygame.time.get_ticks() - t1
        if isFull:
            p = (MW_global.screen.get_width()/2-WIDTH/2,MW_global.screen.get_height()/2-HEIGHT/2)
            #MW_global.realscreen.blit(MW_global.screen,p)
            if sys.platform == 'win32' or sys.platform == 'darwin':
                pygame.display.flip()
            else:
                pygame.display.update(pygame.Rect(p[0],p[1],WIDTH,HEIGHT)) 
        else:
            pygame.display.flip()   #flip the screen
    #else wait the difference3
    else: 
        pygame.time.wait( MSPERFRAME - pygame.time.get_ticks() + last)
        
        
    #quit
    pygame.event.pump()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_F12]:
        pass
        #restart for installation
	pygame.quit()

	pygame.mixer.pre_init(44100, -16, 2, 2048)
	pygame.init()
        MW_global.screen = pygame.display.set_mode(pygame.display.list_modes()[0],DISPLAY_FLAGS)
	pygame.mouse.set_visible(0)

        MW_global.camera = MW_camera.Camera(MW_global.screen)
        MW_global.imagewheel = MW_image.ImageWheel()
        MW_global.animwheel = MW_animator.AnimatorWheel()
        MW_global.xmlwheel = MW_animator.XMLWheel()
        MW_global.sound = MW_sound.soundMan()
        MW_global.switchdict = dict()
        MW_global.spawndict = dict()
        MW_global.frame = 0

        MW_global.state = "PASS"
        MW_global.microstate = "PASS"
        MW_global.microstate2 = "PASS"
        MW_global.finalstate = "PASS"
        MW_global.hangstate = False
        MW_global.judgementstate = False
        MW_global.hardcounter = 0

        MW_global.freezetime = 0
        MW_global.freezetime2 = 0

        #scripted constants
        MW_global.font = "visitor2.ttf",10
        MW_global.font = "visitor2.ttf",15
	#font = "FFFATLAN.ttf",8
        #font = "FFFATLAN.ttf",16
        MW_global.soundMap = dict()
        MW_global.soundMap['light'] = "light08.wav"
        MW_global.soundMap['lighton'] = "lightup06.wav"
        MW_global.soundMap['switch'] = "switch01.wav"
        MW_global.soundMap['static'] = "static03.wav"
        MW_global.sound.loadSound(MW_global.soundMap['light'])
        MW_global.stickyswitchlist = set([2123,3,23299,28566,11732])
        MW_global.stickydoorlist = set() #sticky doors do not open
        MW_global.dooropenlist = set() #open automatically
        MW_global.torchStateMap = { 301: "LIGHT", 401: "I1", 402: "I2", 403: "I3", 404: "I4", 405: "I5", 406: "I6", 501:"INSTRUCTION1", 502:"INSTRUCTION2", 503:"SYMBOL1", 504:"SYMBOL2", 510: "BLANK", 520: "BLANK", 530: "GRASS", 540: "HISC", 541: "HERC", 542: "BLANK", 3881: "Z" }
        MW_global.torchonlist = set([3860])
        MW_global.torchofflist = set([503,504,510,3881,530,0,540,541,542,22548])



        mwc = MW_controller.ControllerController()
    if pygame.mouse.get_pressed()[0]:
        print "goodbye"
        del mwc
        pygame.quit()
        break

