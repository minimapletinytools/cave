import pygame
import MW_global
import MW_animator
import MW_xml
import math
import xml.dom.minidom
import os
from MW_datatypes import *
from MW_constants import *

class Entity:
    def __init__(self):
        self.destroy = False
    def update(self):
        pass
    def draw(self):
        pass
    def getName(self):
        return "Entity"

class WallEn(Entity):
    def __init__(self,pos=Vector2d(0,0)):
        Entity.__init__(self)
        self.pos = pos
        #self.image = pygame.image.load(os.path.join("data","basic_wall.png"))
        self.anim = MW_animator.Animator(MW_xml.getChildNodeWithAttribute(MW_global.xmlwheel.loadXML("tiles.xml"), "sprite","name","wall"))
        self.state = "LIGHT"
        self.highlight = False
    def getName(self):
        return "WallEn"
    def teleport(self,pos):
        self.pos = pos
    def getRect(self):
        return pygame.Rect(self.pos.x,self.pos.y,TILING_SIZE.x,TILING_SIZE.y)
    def setType(self,l,r,t,b):
        sum = 0
        if l: sum += 1
        if r: sum += 1
        if t: sum += 1
        if b: sum += 1
        rotate = 0
        if sum == 4:
            self.image = pygame.image.load("wall_lrtb.png")
        elif sum == 3:
            self.image = pygame.image.load("wall_lrt.png")
            self.image = pygame.transform.rotate(self.image,rotate)
                
        pass
    def update(self):
        pass
    def draw(self):
        #MW_global.camera.drawOnScreen(self.image, self.pos)
        self.anim.state = self.state
        self.anim.update()
        MW_global.camera.drawOnScreen(self.anim.getImage(), self.pos+self.anim.getDrawOffset(), self.anim.getDrawRect())
        #check if covered by light
            #draw
        if self.highlight:
            dPos = MW_global.camera.convertCrds(self.pos)
            #pygame.draw.rect(MW_global.screen,COLOR_WHITE,pygame.Rect(dPos.x,dPos.y,TILING_SIZE.x,TILING_SIZE.y),1)
        self.highlight = False
        
class TorchEn(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.pos = Vector2d(0,0)
        self.id = 0
        self.state = "DEFAULT"
        self.anim = MW_animator.Animator(MW_xml.getChildNodeWithAttribute(MW_global.xmlwheel.loadXML("tiles.xml"), "sprite","name","torch"))
        
    def getRect(self):
        return pygame.Rect(self.pos.x,self.pos.y,TILING_SIZE.x,TILING_SIZE.y)
    def getName(self):
        return "TorchEn"
    def teleport(self,pos):
        self.pos = pos
    def update(self):
        if self.id in MW_global.torchonlist:
            self.state = "BURNING"
        elif self.id in MW_global.torchofflist:
            self.state = "DEFAULT"
        self.anim.state = self.state
        self.anim.update()
    def draw(self):
        MW_global.camera.drawOnScreen(self.anim.getImage(), self.pos+self.anim.getDrawOffset(), self.anim.getDrawRect())
        #dPos = MW_global.camera.convertCrds(self.pos)
        #pygame.draw.rect(MW_global.screen,COLOR_WHITE,pygame.Rect(dPos.x,dPos.y,TILING_SIZE.x,TILING_SIZE.y),1)
class SpikeEn(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.pos = Vector2d(0,0)
        #TODO load spikes, load random image out of a set
        self.anim = MW_animator.Animator(MW_xml.getChildNodeWithAttribute(MW_global.xmlwheel.loadXML("tiles.xml"), "sprite","name","spike"))
        self.state = "DEFAULT"
        self.highlight = False
    def getName(self):
        return "SpikeEn"
    
    def update(self):
        self.anim.state = self.state
        self.anim.update()
        
    def draw(self):
        MW_global.camera.drawOnScreen(self.anim.getImage(), self.pos+self.anim.getDrawOffset(), self.anim.getDrawRect())
        
        
        if self.highlight:
            dPos = MW_global.camera.convertCrds(self.pos)
            #pygame.draw.rect(MW_global.screen,COLOR_WHITE,pygame.Rect(dPos.x,dPos.y,TILING_SIZE.x,TILING_SIZE.y),1)
        self.highlight = False
        
    def getRect(self):
        return pygame.Rect(self.pos.x,self.pos.y,TILING_SIZE.x,TILING_SIZE.y)
    def teleport(self,pos):
        self.pos = pos

class DoorEn(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.id = 0
        self.pos = Vector2d(0,0)
        self.anim = MW_animator.Animator(MW_xml.getChildNodeWithAttribute(MW_global.xmlwheel.loadXML("tiles.xml"), "sprite","name","door"))
        self.state = "UP"   #note, UP is down and DOWN is up
    def getName(self):
        return "DoorEn"
    def getRect(self):
        r = pygame.Rect(self.anim.activeNode.hRect)
        r.x += self.pos.x
        r.y += self.pos.y
        return r
    def teleport(self,pos):
        self.pos = pos
    def update(self):
        if self.id in MW_global.switchdict:
            #if door is not stick 
            if self.id not in MW_global.stickydoorlist and MW_global.switchdict[self.id]:
                self.state = "DOWN"
            else:
                self.state = "UP"                
        if self.id in MW_global.dooropenlist:
            self.state = "DOWN"
        self.anim.state = self.state
        self.anim.update()
    def draw(self):
        MW_global.camera.drawOnScreen(self.anim.getImage(), self.pos+self.anim.getDrawOffset(), self.anim.getDrawRect())
        #pygame.draw.rect(MW_global.screen,COLOR_WHITE,MW_global.camera.convertCrds(self.getRect()),1)
        

class SwitchEn(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.id = 0
        self.pos = Vector2d(0,0)
        self.anim = MW_animator.Animator(MW_xml.getChildNodeWithAttribute(MW_global.xmlwheel.loadXML("tiles.xml"), "sprite","name","switch"))
        self.setState("UP")
    def setState(self,state):
        self.state = state
        if self.state == "UP":
            MW_global.switchdict[self.id] = False
        elif self.state == "DOWN":
            MW_global.switchdict[self.id] = True
    def teleport(self,pos):
        self.pos = pos
    def update(self):
        self.anim.state = self.state
        self.anim.update()
        #should put this SCRIPTING code with checkhits for switches but it does not really matter
        if self.id == 9338:
            if 7 not in MW_global.stickydoorlist:
                MW_global.stickydoorlist.append(7)
    def draw(self):
        MW_global.camera.drawOnScreen(self.anim.getImage(), self.pos+self.anim.getDrawOffset(), self.anim.getDrawRect())
        #if needed, put this in "post update"
        if self.id not in MW_global.stickyswitchlist:
            self.setState("UP")

        
    def getRect(self):
        r = pygame.Rect(self.anim.activeNode.hRect)
        r.x += self.pos.x
        r.y += self.pos.y
        return r
        
    def getName(self):
        return "SwitchEn"
    
class RespawnEn(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.pos = Vector2d(0,0)
        self.id = 0
        self.trigger(False)
    def trigger(self,flag):
        MW_global.spawndict[self.id] = flag
    def getRect(self):
        return pygame.Rect(self.pos.x, self.pos.y, TILING_SIZE.x, TILING_SIZE.y)
    def teleport(self,pos):
        self.pos = pos
    def update(self):
        pass
    def draw(self):
        pygame.draw.rect(MW_global.screen,COLOR_WHITE,MW_global.camera.convertCrds(self.getRect()),0)        
    def getName(self):
        return "RespawnEn"
        
class PlayerEn(Entity):
    def __init__(self,controller):
        Entity.__init__(self)
        self.setupKeyMap()
        self.pos = Vector2d(0,0)
        self.hitOld = self.getRect()
        self.p = controller
        self.state = "STAND"
    def getName(self):
        return "PlayerEn"
    
    def teleport(self,pos):
        self.pos = pos
        
    def setupKeyMap(self):
        self.keyMap = dict()
        keyList = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_x, pygame.K_z]
        for e in keyList:
            self.keyMap[e] = False
        
    def input(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                self.keyMap[e.key] = True
            elif e.type == pygame.KEYUP:
                self.keyMap[e.key] = False
    
    def getRect(self):
        return pygame.Rect(0,0,0,0)
    
    def checkProjected(self,projection):
        r = self.getRect().inflate(60,60)
        r.x += projection.x
        r.y += projection.y
        rect = self.p.cont.getMatrixRect(r)#arbitrary, can be more precise
        wallRects = self.p.cont.getWallRects(rect)
        selfRect = self.getRect()
        selfRect.x += projection.x
        selfRect.y += projection.y
        hits = selfRect.collidelistall(wallRects)
        if len(hits) > 0:
            return True
        else: return False

    def checkProjectedRect(self,projection,rect):
        selfRect = self.getRect()
        selfRect.x += projection.x
        selfRect.y += projection.y
        if selfRect.colliderect(rect):
            return True
        else: return False
    
    def checkRespawn(self):
        rect = self.p.cont.getMatrixRect(self.getRect().inflate(60,60))  #arbitrary, can be more precise
        respawnRects = self.p.cont.getRespawnRects(rect)
        #append man/woman onto the wallRect
        selfRect = self.getRect()
        hits = selfRect.collidelistall(respawnRects)
        for i in hits:
            #TODO check if type is event tirgger and tirgger event
            self.respawn = self.p.cont.wList[self.p.cont.getMatrixIndex(respawnRects[i])].pos
        
    def checkHits(self):
        rect = self.p.cont.getMatrixRect(self.getRect().inflate(60,60))  #arbitrary, can be more precise
        wallRects = self.p.cont.getWallRects(rect)
        #append man/woman onto the wallRect
        selfRect = self.getRect()
        hits = selfRect.collidelistall(wallRects)
        #for i in hits:
            #self.p.cont.wList[self.p.cont.getMatrixIndex(wallRects[i])].highlight = True
        flag = False
        counter = 0
        while len(hits) > 0:
            if counter > 30:
                self.state = "DEAD"
                #self.anim.state = self.state
                #.anim.forceUpdate()
		        #self.pos = Vector2d(self.hitOld.x,self.hitOld.y)
                #print "hit infinite loop detected, breaking now"
                break
            counter += 1
            flag = True
            if (Vector2d(selfRect)-Vector2d(self.hitOld)).magnitude() > 0:
                if math.fabs((selfRect.y-self.hitOld.y)) >= math.fabs((selfRect.x-self.hitOld.x)):
                    self.pos.y -= (selfRect.y-self.hitOld.y)/math.fabs((selfRect.y-self.hitOld.y))
                else:
                    self.pos.x -= (selfRect.x-self.hitOld.x)/math.fabs((selfRect.x-self.hitOld.x))
            #TODO make sure to check only on ground hits
            selfRect = self.getRect()
            hits = selfRect.collidelistall(wallRects)
        #BAD should move to woman class
        if flag == True:
            if self.state == "JUMP" or self.state == "FALLING":
                if self.checkProjected(Vector2d(0,1)):
                    self.state = "STAND"
                else:
                    self.state = "FALLING"
                self.anim.state = self.state
                self.anim.forceUpdate()
    def checkSideHitRect(self,rect):
        selfRect = self.getRect()
        if selfRect.colliderect(rect):
            side = getRectCollideSideVector2d(selfRect,rect)
            intersect = selfRect.clip(rect)
            rdiff = getRectDiff(self.hitOld,rect)
            if math.fabs(rdiff.x) >  math.fabs(rdiff.y):    #we prioritize y direction
                if side.x > 0:
                    self.pos.x += selfRect.clip(rect).w
                else:
                    self.pos.x -= selfRect.clip(rect).w
            else:
                if side.y > 0:
                    self.pos.y += selfRect.clip(rect).h
                else:
                    self.pos.y -= selfRect.clip(rect).h
                    if self.state == "JUMP" or self.state == "FALLING":
                        self.state = "STAND"
    def checkTorch(self):
        rect = self.p.cont.getMatrixRect(self.getRect().inflate(40,40))  #arbitrary, can be more precise
        spikes = self.p.cont.getTorchRects(rect)
        hits = self.getRect().collidelistall(spikes)
        for i in hits:
            self.p.cont.wList[self.p.cont.getMatrixIndex(spikes[i])].state = "BURNING"    
    def checkSpikes(self):
        rect = self.p.cont.getMatrixRect(self.getRect().inflate(40,40))  #arbitrary, can be more precise
        spikes = self.p.cont.getSpikeRects(rect)
        hits = self.getRect().collidelistall(spikes)
        for i in hits:
            self.p.cont.wList[self.p.cont.getMatrixIndex(spikes[i])].highlight = True
            if self.anim.getVelData().y > 0 and self.state != "WALK" and self.state != "LEDGE" and self.state != "STAND":
                self.state = "DEAD"
                self.p.cont.wList[self.p.cont.getMatrixIndex(spikes[i])].state = "BLOOD"      
    def checkSwitches(self):
        rect = self.p.cont.getMatrixRect(self.getRect().inflate(20,20))  #arbitrary, can be more precise
        switches = self.p.cont.getSwitchRects(rect)
        hits = self.getRect().collidelistall(switches)   
        for i in hits:
            if self.getRect().clip(switches[i]).h > 15:
                self.p.cont.wList[self.p.cont.getMatrixIndex(switches[i])].setState("DOWN")
                #self.pos.y = switches[i].y+switches[i].h - 8 - self.getRect().h
    def checkHitsOld(self):
        rect = pygame.Rect(0,0,50,50) #arbitrary, can be more precise
        wallRects = self.p.cont.getWallRects(rect)
        hits = self.getRect().collidelistall(wallRects)
        for i in hits:
            self.p.cont.wList[self.p.cont.getMatrixIndex(wallRects[i])].highlight = True
        if len(hits) > 0:
            #TODO make sure to check only on ground hits
            if self.state == "JUMP" or self.state == "FALLING":
                self.state = "STAND"
            #for now
            intersect = wallRects[hits[0]].clip(self.getRect())
            change = self.pos - self.hitOld
            if math.fabs(change.x/(intersect.w+0.000000001)) > math.fabs(change.y/(intersect.h+0.000000001)):
                if change.x > 0: self.pos.x -= intersect.w
                else: self.pos.x += intersect.w
            else:
                if change.y > 0: self.pos.y += intersect.h
                else: self.pos.y -= intersect.h
            if len(hits) == 1:
                pass
            else: pass
            

                
class WomanEn(PlayerEn):
    def __init__(self,controller):
        self.anim = MW_animator.Animator(MW_xml.getChildNodeWithAttribute(MW_global.xmlwheel.loadXML("characters.xml"), "sprite","name","woman"))
        PlayerEn.__init__(self,controller)
        self.pos = WOMAN_START
        self.respawn = WOMAN_START
        
    def input(self, events):
        PlayerEn.input(self,events)
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    MW_global.sound.play(MW_global.soundMap['light'])
                    MW_global.screen.fill((35,20,20))
                    self.checkTorch()
                if e.key == pygame.K_UP:
                    if self.state == "STAND" or self.state == "WALK":
                        self.state = "JUMP"
                if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT:
                    if self.state == "STAND" or self.state == "WALK":
                        self.state = "WALK"
                        if e.key == pygame.K_LEFT:
                            self.anim.dir = "LEFT"
                        else: self.anim.dir = "RIGHT"
                    if self.state == "CRAWL" or self.state == "CRAWLING":
                        self.state = "CRAWLING"
                        if e.key == pygame.K_LEFT:
                            self.anim.dir = "LEFT"
                        else: self.anim.dir = "RIGHT"
                if e.key == pygame.K_DOWN:
                    if self.state == "WALK":
                        self.state = "CRAWLING"
                    elif self.state == "STAND":
                        self.state = "CRAWL"
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT:
                    if self.state == "WALK":
                        self.state = "STAND"
                    if self.state == "CRAWLING":
                        self.state = "CRAWL"
                    
        if not self.keyMap[pygame.K_DOWN]:
            if not self.checkProjected(Vector2d(0,-20)):
                if self.state == "CRAWLING":
                    self.state = "WALK"
                elif self.state == "CRAWL":
                    self.state = "STAND"
    def checkHits(self):
        rect = self.p.cont.getMatrixRect(self.getRect().inflate(60,60))  #arbitrary, can be more precise
        wallRects = self.p.cont.getWallRects(rect)
        selfRect = self.getRect()
        hits = selfRect.collidelistall(wallRects)
        #TODO something to convert tiled rects into big rects or something like that 
        for i in hits:
            self.p.cont.wList[self.p.cont.getMatrixIndex(wallRects[i])].highlight = True
        flag = False
        if len(hits) == 1:
            #check if at least halfway above
            #check if left or right intersect is minimal
            if getRectCollideSideVector2d(self.getRect(),wallRects[hits[0]]).x == -dirMap[self.anim.dir]:
                if self.hitOld.y < wallRects[hits[0]].y and self.anim.state != "WALK":
                    if self.getRect().clip(wallRects[hits[0]]).w < 10:
                        if self.anim.dir == "RIGHT":
                            self.pos.x = wallRects[hits[0]].x - 10
                        else:
                            self.pos.x = wallRects[hits[0]].x + 10
                        self.pos.y = wallRects[hits[0]].y - 40
                        self.state = "LEDGE"
                        return
        counter = 0
        while len(hits) > 0:
            if counter > 30:
                self.state = "DEAD"
                #self.pos = Vector2d(self.hitOld.x,self.hitOld.y)
                #print "hit infinite loop detected, breaking now"
                break
            counter += 1
            flag = True
            if (Vector2d(selfRect)-Vector2d(self.hitOld)).magnitude() > 0:
                if math.fabs((selfRect.y-self.hitOld.y)) >= math.fabs((selfRect.x-self.hitOld.x)):
                    self.pos.y -= (selfRect.y-self.hitOld.y)/math.fabs((selfRect.y-self.hitOld.y))
                else:
                    self.pos.x -= (selfRect.x-self.hitOld.x)/math.fabs((selfRect.x-self.hitOld.x))
            #TODO make sure to check only on ground hits
            selfRect = self.getRect()
            hits = selfRect.collidelistall(wallRects)
        if flag == True:
            if self.state == "JUMP" or self.state == "FALLING":
                if self.checkProjected(Vector2d(0,1)):
                    self.state = "STAND"
                else:
                    self.state = "FALLING"
                self.anim.state = self.state
                self.anim.forceUpdate()
    def update(self):
        #print self.state, self.anim.activeNode.id
        self.hitOld = self.getRect()
        #get input, update and move character based on input, check hits, check if over ground, if so, will update next loop
        if self.p.activePlayer == "woman":
            self.input(MW_global.eventList)
        elif self.state == "WALK": self.state = "STAND"
        self.anim.state = self.state
        self.anim.update()
        self.pos += self.anim.getVelData()
        if self.state == "LEDGE":
            self.state = "STAND"
        self.checkRespawn()
        self.checkHits()
        #self.checkSideHitRect(self.p.man.getRect())
        self.checkSwitches()
        self.checkSpikes()
        #check if over ground
        if not self.checkProjected(Vector2d(0,1)) and not self.checkProjectedRect(Vector2d(0,1),self.p.man.getRect()):
            if self.state != "JUMP" and self.state != "DEAD" and self.state != "LEDGE":
                self.state = "FALLING" 
           
    def draw(self):
        MW_global.camera.drawOnScreen(self.anim.getImage(), self.pos+self.anim.getDrawOffset(), self.anim.getDrawRect())
        #pygame.draw.rect(MW_global.screen,COLOR_WHITE,MW_global.camera.convertCrds(self.getRect()),1)
        #pygame.draw.rect(MW_global.screen,COLOR_WHITE,self.getRect().inflate(40,40),1)
    
    def getRect(self):
        r = pygame.Rect(self.anim.activeNode.hRect)
        r.x += self.pos.x
        r.y += self.pos.y
        return r
    
class ManEn(PlayerEn):
    def __init__(self,controller):
        self.anim = MW_animator.Animator(MW_xml.getChildNodeWithAttribute(MW_global.xmlwheel.loadXML("characters.xml"), "sprite","name","man"))
        PlayerEn.__init__(self,controller)
        self.pos = MAN_START
        self.respawn = MAN_START
        
    def input(self, events):
        PlayerEn.input(self,events)
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    if self.state == "STAND" or self.state == "WALK":
                        self.state = "JUMP"
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT:
                    if self.state == "WALK":
                        self.state = "STAND"
        if self.keyMap[pygame.K_LEFT] or self.keyMap[pygame.K_RIGHT]:
            if self.state == "STAND" or self.state == "WALK":
                self.state = "WALK"
                if self.keyMap[pygame.K_LEFT]:
                    self.anim.dir = "LEFT"
                else: self.anim.dir = "RIGHT"
    def update(self):
        if self.anim.activeNode.state == "REALLYDEAD":
            self.state ="STAND"
            self.teleport(self.respawn)
        #print self.state, self.anim.activeNode.id
        self.hitOld = self.getRect()
        #get input, update and move character based on input, check hits, check if over ground, if so, will update next loop
        if self.p.activePlayer == "man":
            self.input(MW_global.eventList)
        elif self.state == "WALK": self.state = "STAND"
        self.anim.state = self.state
        self.anim.update()
        self.pos += self.anim.getVelData()
        self.checkRespawn()
        self.checkHits()
        #self.checkSideHitRect(self.p.woman.getActiveWoman().getRect())
        self.checkSpikes()
        self.checkSwitches()

        #check if over ground
        if not self.checkProjected(Vector2d(0,1)) and not self.checkProjectedRect(Vector2d(0,1),self.p.woman.getActiveWoman().getRect()): 
            if self.state != "JUMP" and self.state != "DEAD":
                self.state = "FALLING" 
    
    def draw(self):
        MW_global.camera.drawOnScreen(self.anim.getImage(), self.pos+self.anim.getDrawOffset(), self.anim.getDrawRect())
        #pygame.draw.rect(MW_global.screen,COLOR_WHITE,MW_global.camera.convertCrds(self.getRect()),1)
        #pygame.draw.rect(MW_global.screen,COLOR_WHITE,self.getRect().inflate(20,20),1)
    
    def getRect(self):
        r = pygame.Rect(self.anim.activeNode.hRect)
        r.x += self.pos.x
        r.y += self.pos.y
        return r
    


        
    
