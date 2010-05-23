import pygame
from PEG_datatypes import *
from PEG_entity import *
import PEG_helpers
import PEG_mainLoop

class Player(MovingEntity):
    """player controlled character
    
    __dict__
    position: Rect2d, represents HIT BOX on screen
    drawRect: Rect2d, represents DRAW BOX relative to HIT BOX"""
    def __init__(self, exml):
        self.drawOffset = Vector2d(60,35)
        tr = Rect2d(0,0,110,190)
        if exml.hasAttribute("x"):
            tr.x = float(exml.getAttribute("x"))
        if exml.hasAttribute("y"):
            tr.x = float(exml.getAttribute("y"))
        self.myxml = exml
        MovingEntity.__init__(self,tr)
        self.setUpImages()
        self.grounded = False
        self.dir = "left"
        self.state = "stand"
    
    def getxml(self):
        self.myxml.setAttribute("x", str(self.pos.x))
        self.myxml.setAttribute("y", str(self.pos.y))
        return self.myxml
    
    def setUpImages(self):
        self.mainSurface = pygame.image.load("pedoman.png").convert_alpha()
        self.flipSurface = pygame.transform.flip(self.mainSurface,True,False)
        self.activeSurface = self.mainSurface
        self.frames = dict()
        #frame[<animation string>] = (<frame position list>,<ms per frame>)
        self.frames["run"] = ((Vector2d(0,0),Vector2d(250,0),Vector2d(500,0),Vector2d(750,0)),100)
        self.frames["stand"] = ((Vector2d(750,0),),100)
        
    def update(self):
        #handle the input
        for e in PEG_mainLoop.mainLoop().eventList:
            if e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:
                self.handleInput(e)
        
        if self.grounded:
            self.vel.y = 0
        #gravity
        self.vel -= GRAVITY
        
        #move the character
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        
    
    def draw(self):
        if self.dir == "left":
            self.activeSurface = self.flipSurface
        else:
            self.activeSurface = self.mainSurface
                    
        frameNum = (PEG_helpers.truncateToMultiple(pygame.time.get_ticks(),self.frames[self.state][1])/self.frames[self.state][1])%len(self.frames[self.state][0])
        print self.state
        PEG_mainLoop.mainLoop().cam.drawOnScreen(self.activeSurface, self.pos-self.drawOffset, pygame.Rect(self.frames[self.state][0][frameNum].x, self.frames[self.state][0][frameNum].y,250,250))
        
    def collide(self, e):
        """see super"""
        if isinstance(e, SolidEntity):
            col = PEG_helpers.collideSide(self.pos,e.pos)
            self.pos -= col
            #if collide with ground
            if col.y > 0:
                self.grounded = True
            if col.x != 0:
                self.vel.x = 0
            
        
    def handleInput(self, e):
        """handles KEYDOWN type events
        
        e: pygame.event w/ pygame.event.type = pygame.KEYDOWN"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.dir = "left"
            self.vel.x = -7
        if keys[pygame.K_RIGHT]:
            self.dir = "right"
            self.vel.x = 7
        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.state = "stand"
            self.vel.x = 0
        else:
            self.state = "run"
            
        if e.type == pygame.KEYDOWN:
#===============================================================================
#            if e.key == pygame.K_UP:
#                if self.grounded == True:
#                    self.grounded = False
#                    self.vel.y = -15
#                    
#===============================================================================
            if e.key == pygame.K_DOWN:
                #self.vel.y = 5
                pass
        
               
