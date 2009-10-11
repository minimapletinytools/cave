from distutils.core import setup
import py2exe
setup(console=['main.py'])


#===============================================================================
# import pygame
# from MW_datatypes import *
# 
# 
# 
# 
# pygame.init()
# screen = pygame.display.set_mode((1440 ,900))
# 
# #image = pygame.image.load("testimage.png")
# while 1:
#    r1 = pygame.Rect(100,100,50,50)
#    r2 = reflectRect(r1,200)
#    pygame.draw.line(screen,(127,127,127),(200,0),(200,500))
#    pygame.draw.rect(screen,(127,127,127),r1,1)
#    pygame.draw.rect(screen,(127,127,127),r2,1)
#    #screen.blit(image,(50,50))
#    pygame.display.flip()
#    #quit
#    pygame.event.pump()
#    keys = pygame.key.get_pressed()
#    if keys[pygame.K_q]:
#        print "goodbye"
#        del mwc
#        pygame.quit()
#        quit()
#===============================================================================
