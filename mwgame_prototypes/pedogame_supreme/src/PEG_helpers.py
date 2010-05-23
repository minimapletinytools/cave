import pygame
from PEG_datatypes import *

def collided(r1, r2):
    """checks collision between two Rect2d and returns bool
    
    r1, r2: Rect2d
    returns: bool"""
    AL = r1.x
    AR = r1.x + r1.w
    AT = r1.y
    AB = r1.y + r1.h
    BL = r2.x
    BR = r2.x + r2.w
    BT = r2.y
    BB = r2.y + r2.h
    #check left and right
    if AR < BL or BR < AL:
        return False
    if AB < BT or BB < AT:
        return False
    return True

def collideSide(r1, r2):
    #make sure there was a collision
    if collided(r1,r2) == False:
        return (0,0)
    AL = r1.x
    AR = r1.x + r1.w
    AT = r1.y
    AB = r1.y + r1.h
    BL = r2.x
    BR = r2.x + r2.w
    BT = r2.y
    BB = r2.y + r2.h
    #if A RIGHT is in B LEFT
    if AR-BL < BR-AL:
        #if A BOTTOM is in B TOP
        if AB-BT < BB-AT:
            if AR-BL < AB-BT:
                return Vector2d(AR-BL,0)
            else:
                return Vector2d(0,AB-BT)
        else:
            if AR-BL < BB-AT:
                return Vector2d(AR-BL,0)
            else:
                return Vector2d(0,-(BB-AT))   
    else:
        #if A BOTTOM is in B TOP
        if AB-BT < BB-AT:
            if BR-AL < AB-BT:
                return Vector2d(-(BR-AL),0)
            else:
                return Vector2d(0,AB-BT)
        else:
            if BR-AL < BB-AT:
                return Vector2d(-(BR-AL),0)
            else:
                return Vector2d(0,-(BB-AT))
        
def easeIn(number, rate = .2):
    """eases in based on 90 degree circle
    
    number: number to ease in to
    rate: rate in percent to """
    
def truncateToMultiple(number, multiple):
    """truncates number to greatest multiple of multiple not greater than number
    
    number: number to truncate
    multiple: integer to truncate at multiple of"""
    return int(number/multiple)*multiple
    
def duck():
    print "quack"