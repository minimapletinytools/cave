import pygame
import random
import math


class Vector2d():
    def __init__(self,*args):
        if len(args) == 2:
            self.x = args[0]
            self.y = args[1]
        elif len(args) == 1:
            self.x = args[0].x
            self.y = args[0].y
            
    def __str__(self):
        c = "Vector2d ("
        c += str(self.x)
        c += ","
        c += str(self.y)
        c += ")"
        return c        
    def __sub__(self,c):
        return Vector2d(self.x-c.x, self.y-c.y)
    def __add__(self,c):
        return Vector2d(self.x+c.x, self.y+c.y)
    def __mul__(self,s1):
        try: return Vector2d(self.x*s1[0],self.y*s1[1])
        except: return Vector2d(self.x*s1,self.y*s1)
    def __truediv__(self,scalar):
        try: return self*(1/scalar)
        except:
            print "division by zero!" 
            return self*9999
    def __lt__(self,other):
        return self.magnitude() < other.magnitude()
    def __le__(self,other):
        return self.magnitude() <= other.magnitude()
    def __eq__(self,c):
        return self.x == c.x and self.y == c.y
    def __gt__(self,other):
        return self.magnitude() > other.magnitude()
    def __ge__(self,other):
        return self.magnitude() >= other.magnitude()
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
        return Vector2d(0,0)
    def magnitude(self):
        return math.sqrt(square(self.x)+square(self.y))
    def getTuple(self):
        return (self.x,self.y)
    def getIntTuple(self):
        return (int(self.x),int(self.y))
    def tangentTo(self,vector):
        return getVector2dFromPolar((vector-self).getPolar()[0],(vector-self).getPolar()[1] - math.pi/2).getNormal()
    def getPolar(self):
        return (self.magnitude(),math.atan2(self.y,self.x))
    def getSDLRect(self):
        return pygame.Rect(self.x,self.y,0,0)
    
    
class Line2d():
    def __init__(self,_p1,_p2):
        self.p1 = _p1
        self.p2 = _p2
        #THESE NEED CHECKING
        try: self.m = (self.p1.y-self.p2.y)/(self.p1.x-self.p2.x)
        except: self.m = 999999999999
        self.b = self.p1.y - self.m*self.p1.x
    def getAngleToHorizontal(self):
        #assumes line goes from p1 to p2
        return Vector2d(self.p2.x-self.p1.x, self.p2.y-self.p1.y).getPolar()[1]

class Circle2d():
    def __init(self,_p,_r):
        """
        
        _p: Vector2d
        _r: float"""
        self.p = _p
        self.r = _r
    def containsPt(self,pt):
        return self.p.distance(pt) <= self.r
        
    
    
#factory stuff
def getVector2dFromPolar(r,a):
    return Vector2d(r*math.cos(a),r*math.sin(a))

def getRandVector2d(mag):
    return Vector2d(random.randint(-mag,mag),random.randint(-mag,mag))

def getVector2dFromTuple(tuple):
    return Vector2d(tuple[0],tuple[1])

def getRandVector2dGaussian(mag,dir,sigma = 1):
    """returns a random vector with mean dir and standard deviation sigma in radians
    """
    angle = random.gauss(math.atan2(dir.x, dir.y),sigma)
    return getVector2dFromPolar(mag,angle)

def getRect2dFromVector2d(pos,w,h):
    return Rect2d(pos.x,pos.y,w,h)

def convertToTupleList(vlist, offset = Vector2d(0,0)):
    tupleList = []
    for v in vlist:
        tupleList.append((v+offset).getIntTuple())
    return tupleList

def getAngle3pt(A,B,C):
    """returns angle from line AB to line BC
    
    A,B,C: Vector2d"""
    AB = A.distance(B)
    BC = B.distance(C)
    CA = C.distance(A)
    try: g = math.acos( (square(AB) + square(BC) - square(CA))/(2*AB*BC))
    except: g = 0
    #TODO: determine g is positive or negative
    
    
    #print " A: ", A.x, " ", A.y, " B: ", B.x, " ", B.y, " C: ", C.x, " ", C.y
    #return Line2d(B,A).getAngleToHorizontal() - Line2d(B,C).getAngleToHorizontal()
    if Line2d(B,A).getAngleToHorizontal() >= Line2d(B,C).getAngleToHorizontal():
        g = -g
    
    return g
    
    

class Rect2d(Vector2d):
    def __init__(self,_x = 0, _y = 0, _w = 0, _h = 0):
        Vector2d.__init__(self,_x,_y)
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
    def containsPt(self,point):
        pass
    def getArea(self):
        return self.w*self.h
    def getPerimeter(self):
        return 2*self.w + 2*self.h
    def getCenter(self):
        return Vector2d(self.x+self.w/2, self.y + self.h/2)
    def getRect(self):
        return pygame.Rect(self.x,self.y,self.w,self.h)
    
def square(x): return x*x
def add(a,b): return a + b
def truncateToMultiple(number, multiple):
    """truncates number to greatest multiple of multiple not greater than number
    
    number: number to truncate
    multiple: integer to truncate at multiple of"""
    return int(number/multiple)*multiple
def reflectRect(rect, x):
    return pygame.Rect(2*x-(rect.x+rect.w),rect.y,rect.w,rect.h)
def getRectCollideSideVector2d(r1,r2):
    x = y = 0
    if r1.centerx > r2.centerx: #r1 RIGHT of r2
        x = 1
    elif r1.centerx < r2.centerx:
        x = -1
    if r1.centery > r2.centery: #r1 BELOW r2
        y = 1
    elif r1.centery < r2.centery:
        y = -1
    return Vector2d(x,y)
def getRectDiff(r1,r2):
    side = getRectCollideSideVector2d(r1,r2)
    x = y = 0
    if side.y > 0: #if r1 BELOW r2
        y = r1.y - (r2.y + r2.h)
    elif side.y < 0:
        y = -(r1.y - (r2.y + r2.h))
    if side.x > 0: #r1 RIGHT OF r2
        x = r1.x - (r2.x+r2.h)
    elif side.r < 0:
        x = -(r1.x - (r2.x+r2.h))
    return Vector2d(x,y)
    