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
        if pygame.time.get_ticks()%200 == 1:
            pass
            #print "cycle time", pygame.time.get_ticks() - t1
        if isFull:
            p = (MW_global.realscreen.get_width()/2-MW_global.screen.get_width()/2,MW_global.realscreen.get_height()/2-MW_global.screen.get_height()/2)
            MW_global.realscreen.blit(MW_global.screen,p)
            #pygame.display.update(pygame.Rect(p[0],p[1],WIDTH,HEIGHT))
            pygame.display.flip()
        else:
            pygame.display.flip()   #flip the screen
    #else wait the difference3
    else: 
        pygame.time.wait( MSPERFRAME - pygame.time.get_ticks() + last)
        
        
    #quit
    pygame.event.pump()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        print "goodbye"
        del mwc
        pygame.quit()
        exit()

