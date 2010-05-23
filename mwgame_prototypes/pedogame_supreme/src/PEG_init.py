import pygame
from PEG_mainLoop import *
from PEG_constants import *






pygame.init()
#screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
screen = pygame.display.set_mode(SCREEN_SIZE)   
#pygame.display.toggle_fullscreen()
#pygame.mouse.set_visible(0)

#load game
myGame = mainLoop(screen)
#assume the last update was now
last = pygame.time.get_ticks()
while 1:
    #if time expired
    if(pygame.time.get_ticks() - last > MSPERFRAME):
        while(pygame.time.get_ticks() - last > MSPERFRAME):
            last += MSPERFRAME
        screen.fill(COLOR_DARK)
        myGame.loop()
        pygame.display.flip()   #flip the screen
    #else wait the difference
    else: 
        pygame.time.wait( MSPERFRAME - pygame.time.get_ticks() + last)
        
        
    #quit
    pygame.event.pump()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        print "goodbye"
        pygame.quit()
        quit()

