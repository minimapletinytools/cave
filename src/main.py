import pygame
import MW_global
import MW_controller
from MW_constants import *
from MW_datatypes import *

        
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
        if pygame.time.get_ticks()%10 == 1:
            print pygame.time.get_ticks() - t1
        pygame.display.flip()   #flip the screen
    #else wait the difference
    else: 
        pygame.time.wait( MSPERFRAME - pygame.time.get_ticks() + last)
        
        
    #quit
    pygame.event.pump()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        print "goodbye"
        del mwc
        pygame.quit()
        quit()

