""" THIS IS A TESTER FILE FOR ASTEROID CLASS!!!! """
""" okay the only two classes actually used in this file are Asteroid and its child CHICKEN JOCKEY!!! """
import random
import pygame
from Entities.Entity import *
from EntityTags import *
from math import pi
from pyglm import glm


class Asteroid(EntityCachedPhysics):
    type = 'Asteroid'
    __slots__ = 'to_die',
    def __init__(self,pos,vel,rot,mass,img:Surface,tags:int):
        super().__init__(pos, vel,rot,mass,img,tags)
        self.to_die = False
    
    def update(self,map:MapType,dt:float,game:GameType):

        self.rot += 1 * dt
        super().update(map,dt,game)
        # self.vel *= .995
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
                a = Asteroid(self.pos+dir*5,self.vel,theta,self.mass/4,pygame.transform.scale_by(self._surf,0.5),self.tags)
                a.vel += dir * 100
                game.spawnEntity(a)
    
    def onCollide(self, other:Entity):
        if other.tags & E_CAN_DAMAGE:
            # assert isinstance(other,ICanDamage)
            self.to_die = True
        if other.tags & E_CAN_BOUNCE:
            rel_vel = self.vel - other.vel
            d = self.pos - other.pos
            dot = glm.dot(d,rel_vel)
            if dot < 0:
                d *= dot * 2/glm.length2(d) #type: ignore
                self.n_vel = self.vel -  d * (other.mass / (self.mass+other.mass))

class ChickenJockey(Asteroid):
    pass