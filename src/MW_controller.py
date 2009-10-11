import pygame
import xml.dom.minidom
import MW_animator
import MW_xml
import MW_global
import MW_containers
import MW_entity
from MW_constants import *
from MW_datatypes import *

class ControllerController():
    def duck():
        print "quack!"
    def __init__(self):
        self.cList = [TestController(),StartController(),PlayController(),WinController()]
        self.activeIndex = 2 
        MW_global.controller = self
    def loop(self):
        #post events
        MW_global.eventList = pygame.event.get()
        pygame.event.clear()
        self.cList[self.activeIndex].loop()
    def switchController(self,index):
        if 0 <= index < len(self.activeIndex):
            self.activeIndex = index 
    
class Controller:
    def __init__(self):
        pass
    def loop(self):
        pass
    
class oldController:
    def __init__(self):
        self.anim = MW_animator.Animator(MW_xml.getChildNodeWithAttribute(xml.dom.minidom.parse("anim.xml"), "sprite","name","player"))
    def loop(self):
        self.anim.update()
        self.anim.drawAt(Vector2d(100,100))
        
class TestController(Controller):
    def __init__(self):
        Controller.__init__(self)
        self.cont = MW_containers.MatrixContainer( (100,100) )
        self.woman = MW_entity.WomanEn(self)
    def loop(self):
        self.woman.update()
        self.woman.draw()
        self.cont.update()
        self.cont.draw()
        pass
    
class StartController(Controller):
    def __init__(self):
        Controller.__init__(self)
        pass
    def loop(self):
        pass

class PlayController(Controller):
    def __init__(self):
        Controller.__init__(self)
        self.cont = MW_containers.MatrixContainer( (1000,1000) )
        self.doodads = MW_containers.DoodadContainer()
        self.woman = MW_entity.WomanEn(self)
        self.man = MW_entity.ManEn(self)
        self.activePlayer = self.man
    def loop(self):
        for e in MW_global.eventList:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_TAB:
                    if self.activePlayer == self.man:
                        self.activePlayer = self.woman
                        MW_global.camera.moveTo(self.woman.pos)
                    else: 
                        self.activePlayer = self.man
                        MW_global.camera.moveTo(self.man.pos)
        self.woman.update()
        self.man.update()
        self.doodads.update() #scripting goes in here
        self.cont.update() #though tehre really is nothing to update
        self.cont.draw()
        self.doodads.draw()
        self.woman.draw()
        self.man.draw()
       #pygame.draw.rect(MW_global.screen,COLOR_WHITE,MW_global.camera.convertCrds(MW_global.camera.rect),1)
    
class WinController(Controller):
    def __init__(self):
        Controller.__init__(self)
        pass
    def loop(self):
        pass