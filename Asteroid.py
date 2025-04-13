""" THIS IS A TESTER FILE FOR ASTEROID CLASS!!!! """
""" okay the only two classes actually used in this file are Asteroid and its child CHICKEN JOCKEY!!! """
import random
import pygame
from ChunkManager import * 
from Nenemy import enemyFactory
from Input import Input

from ChunkManager import *

class Asteroid(Entity):
    def __init__(self,pos,rot,img:pygame.Surface):
        super().__init__(pos, rot)
        self.pos = pos
        self.rot = rot

        angle = random.uniform(0, 2 * pi)
        speed = random.uniform(50, 150)
        self.vel.x = glm.cos(angle) * speed
        self.vel.y = glm.sin(angle) * speed

        self._surf = img.convert_alpha()
        self.rect = self._surf.get_rect()
        self.to_die = False
    
    def update(self,map:MapType,dt:float,input:Input,game:"Game"):
        self.rot += 1 * dt
        self.pos += self.vel * dt
        self.vel *= .995
        self.dirty = True
        if self.to_die:
            self.dead = True
            children = 4
            t_offset = random.random()*2*pi
            if min(self._surf.get_size()) <= 48:
                return
            for i in range(children):
                theta = i*2*pi/children + t_offset
                dir = glm.vec2(glm.cos(theta),glm.sin(theta))
                a = Asteroid(self.pos+dir*40,theta,pygame.transform.scale_by(self._surf,0.5))
                a.vel += dir * 100
                game.spawnEntity(a)
    
    def onCollide(self, other):
        if isinstance(other,Bullet):
            self.to_die = True
        elif isinstance(other,Asteroid):
            self.vel = self.pos - other.pos
        
class ChickenJockey(Asteroid):
    def __init__(self,pos,rot,img:pygame.Surface):
        super().__init__(pos, rot, img)