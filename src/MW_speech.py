import pygame
from MW_constants import *
from MW_datatypes import *

class Speech:
    def __init__(self):
        print "loading speech singleton..."
        self.font = dict()
        self.defaultFont = self.getFont(pygame.font.get_default_font(),50) 
    
    def getFont(self,name,size):
        if name not in self.font:
            self.font[name] = dict()
        if size not in self.font[name]:
            try: 
                self.font[name][size] = pygame.font.Font(name,size)
                print "created font: ", name, " at size: ", size
            except: 
                self.font[name][size] = pygame.font.SysFont(pygame.font.get_default_font(), size)
                print "created default font: ", pygame.font.get_default_font(), " at size: ", size, " in place of font ", name
            
        return self.font[name][size]
    
    def delFont(self,name,size):
        try: del self.font[name][size]
        except: pass
                    
    def setSize(self,size,name = pygame.font.get_default_font()):
        """use this to preload default size at a certain size"""
        self.defaultFont = self.getFont(name,size)
            
    def writeText(self, sfc, pos, text, color = COLOR_WHITE):
        """writes Text to sfc at pos
        
        sfc: pygame.Surface
        pos: vectorMath.Position
        text: string"""
        tsfc = self.defaultFont.render(str(text), False, color)
        sfc.blit(tsfc, (pos.x,pos.y))
        
    def writeBubble01(self, sfc, pos, text, width):
        """writes Text to sfc at pos in textbox type 01 of width width
        
        sfc: pygame.Surface
        pos: vectorMath.Position
        text: string
        width: integer"""
        #draw circles and rectangles to fill inside of text box
        #while there is stuff to write
            #while font.size(text) less than width
                #add another character
            #draw and move y position down font.height()
        #draw boundaries
    
    def writeCentered(self,sfc,pos,text, color = COLOR_WHITE):
        """same as writeText except writes centered at pos"""
        newPos = Vector2d(pos.x - self.defaultFont.size(str(text))[0]/2,pos.y - self.defaultFont.size(str(text))[1]/2)
        self.writeText(sfc,newPos,text,color)
    
    def writeBubble02(self, sfc, pos, text):
        pass