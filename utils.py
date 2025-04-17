from gametypes import *
import math

from pyglm import glm

def expDecay(a,b,decay:float,dt:float):
    return b+(a-b)*math.exp(-decay*dt)

def cross2d(a:Vec2,b:Vec2):
    return a.x*b.y-a.y*b.x