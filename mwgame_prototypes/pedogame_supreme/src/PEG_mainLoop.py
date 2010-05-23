from PEG_camera import *
from PEG_helpers import *
from pedo_player import *

import pedo_lookup

import xml.dom.minidom


class mainLoop:
    class __impl:
        
        #public data
        screen = None
        cam = None
        eventList = []
        entityList = []
        deleteList = []
        cLevel = 0
        wLevel = 1
        
        def __init__(self, sfc):
            self.screen = sfc
            self.cam = Camera(sfc)
            
        def loop(self):
            #load level
            if self.cLevel != self.wLevel:
                #level loading function
                self.loadLevel(self.wLevel)
                self.cLevel = self.wLevel
                pass
            
            #get (ALL) events and clear it
            self.eventList = pygame.event.get()
            pygame.event.clear()
                    
            for e in self.entityList:
                e.update()
                          
            self.handleCollision()
            
            self.deleteRoutine()
            
            for e in self.entityList:
                e.draw()
        
        def handleCollision(self):
            for e in self.entityList:
                if isinstance(e, MovingEntity):
                    for f in self.entityList:
                        if isinstance(f, StaticEntity):
                            if collided(e.pos, f.pos):
                                e.collide(f)
                                pass
        
        def deleteEntity(self, e):
            self.deleteList.append(e)
        
        def deleteRoutine(self):
            for e in self.deleteList:
                self.entityList.remove(e)
            self.deleteList = []
        
        def loadLevel(self,lvl):
            topxml = xml.dom.minidom.parse("level.xml")
            lvlxml = None
            for n in topxml.getElementsByTagName('level'):
                if n.hasAttribute("id") and n.getAttribute("id") == str(lvl):
                    lvlxml = n
                    break
            if lvlxml == None:
                print "no such level exists!"
                return
            for n in lvlxml.getElementsByTagName('entity'):
                if n.hasAttribute("type"):
                    self.entityList.append(pedo_lookup.enTables(n))
        
        def saveState(self,lvl):
            topxml = xml.dom.minidom.parse("level.xml")
            #cerate a new node
            lvlxml = topxml.createElement("level")
            #topxml.appendChild(lvlxml)
            lvlxml.setAttribute("id",str(lvl))
            for e in self.entityList:
                if e.getxml():
                    lvlxml.appendChild(e.getxml())
            print lvlxml.toprettyxml()
            f = open('level.xml','w')
            f.write(topxml.toprettyxml())
                   
    #storage for the instance reference
    #WHY DO I NOT NEED TO DECLARE THIS STATIC????
    __instance = None
    
    def __init__(self,sfc = None):
        """ create instance """
        #check if instance exists and create it
        if mainLoop.__instance is None:
            if sfc == None:
                print "mainLoop instantiation requires surface"
            mainLoop.__instance = mainLoop.__impl(sfc)
            
        
        #store instance reference as the only member in the handle???
        self.__dict__['_mainLoop_instance'] = mainLoop.__instance
    
    def __getattr__(self, attr):
        """delegate access to implementation"""
        return getattr(self.__instance, attr)
    
    def __setattr__(self, attr, value):
        """delegate access to implementation"""
        return setattr(self.__instance, attr, value) 
        