import pygame
import xml.dom.minidom
import MW_animator
import MW_xml
import MW_global
import MW_containers
import MW_entity
import MW_effects
from MW_constants import *
from MW_datatypes import *

class ControllerController():
    def __init__(self):
        self.cList = [TestController(),StartController(),PlayController(),WinController()]
        self.effect = MW_effects.EffectMenu()
        self.activeIndex = 2 
        MW_global.controller = self
    def loop(self):
        if MW_global.freezetime < 1:
            MW_global.eventList = pygame.event.get()
        else: 
            MW_global.freezetime -= 1
            MW_global.eventList = list()
        pygame.event.clear()
        self.effect.update()
        self.cList[self.activeIndex].loop()
        self.effect.draw()
    def switchController(self,index):
        if 0 <= index < len(self.cList):
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
        #self.cont = MW_containers.MatrixContainer( (100,100), self )
        self.woman = MW_entity.WomanEn(self)
    def loop(self):
        self.woman.update()
        self.woman.draw()
        #self.cont.update()
        #self.cont.draw()
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
        self.cont = MW_containers.MatrixContainer( (1000,1000), self )
        self.woman = MW_containers.WomanContainer(self)
        self.man = MW_entity.ManEn(self)
        self.activePlayer = "man"
        self.burningTorches = list()
    def getPlayerList(self):
        return [self.man,self.woman.getActiveWoman()]
    def getActivePlayer(self):
        if self.activePlayer == "man":
            return self.man
        elif self.activePlayer == "woman":
            return self.woman.getActiveWoman()
        else: 
            #todo??? nothing really
            return None 
    def handleInput(self):
        for e in MW_global.eventList:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_TAB:
                    if self.activePlayer == "man" and MW_global.microstate2 != "WOMAN AT END" and MW_global.state != "LOSE":
                        if(MW_global.state != "WINNING" or self.man.anim.activeNode.state == "REALLYREALLYDEAD"):
                            self.activePlayer = "woman"
                            MW_global.camera.moveTo(self.woman.getActiveWoman().pos)
                    elif MW_global.state != "WINNING" and MW_global.freezetime2 == 0: 
                        self.activePlayer = "man"
                        MW_global.camera.moveTo(self.man.pos)
    def loop(self):
        if CAMERA_MODE == "force":
            MW_global.camera.moveTo(self.getActivePlayer().pos)
        self.handleInput()
                        
        self.woman.update()
        self.man.update()
        self.cont.update() #though tehre really is nothing to update
        #t = pygame.time.get_ticks()
        self.cont.draw()
        #if pygame.time.get_ticks()%10 == 1:
            #print pygame.time.get_ticks() - t
        self.woman.draw()
        self.man.draw()
        #pygame.draw.rect(MW_global.screen,COLOR_WHITE,MW_global.camera.convertCrds(MW_global.camera.rect.inflate(-10,-10)),1)
    
class WinController(Controller):
    def __init__(self):
        Controller.__init__(self)
        pass
    def loop(self):
        pass
