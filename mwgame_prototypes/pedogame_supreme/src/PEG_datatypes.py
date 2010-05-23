import pygame

class Vector2d:
    def __init__(self,_x,_y):
        self.x = _x
        self.y = _y
    def __sub__(self,c):
        return Vector2d(self.x-c.x, self.y-c.y)
    def __add__(self,c):
        return Vector2d(self.x+c.x, self.y+c.y)
    def __mul__(self,scalar):
        return Vector2d(self.x*scalar,self.y*scalar)
    def __eq__(self,c):
        return self.x == c.x and self.y == c.y
    def distance(self,target):
        return math.sqrt(square(self.x-target.x) + square(self.y-target.y))
    def moveTowards(self,target,distance):
        uvector = Vector2d(target.x-self.x,target.y-self.y).getNormal()
        tv2d = self + uvector*distance
        self.x = tv2d.x
        self.y = tv2d.y
    def normalize(self):
        tv2d = getNormal(self)
        self.x = tv2d.x
        self.y = tv2d.y
    def getNormal(self):
        mag = math.sqrt(self.x*self.x + self.y*self.y)
        if mag != 0:
            return Vector2d(self.x/mag, self.y/mag)
        return Position(0,0)
    def getTuple(self):
        return (self.x,self.y)
    def getIntTuple(self):
        return (int(self.x),int(self.y))

class Rect2d:
    def __init__(self,_x = 0, _y = 0, _w = 0, _h = 0):
        self.x = _x
        self.y = _y
        self.w = _w
        self.h = _h
        
    def __add__(self,c):
        if isinstance(c,Vector2d):
            return Rect2d(self.x+c.x, self.y+c.y, self.w, self.h)
        else:
            return NotImplemented
    
    def __sub__(self,c):
        if isinstance(c,Vector2d):
            return Rect2d(self.x-c.x, self.y-c.y, self.w, self.h)
        else:
            return NotImplemented

    def getPosition(self):
        return Vector2d(self.x, self.y)
    
    def getSDLRect(self):
        return pygame.Rect(self.x,self.y,self.w,self.h)
    
def square(x):
    return x*x