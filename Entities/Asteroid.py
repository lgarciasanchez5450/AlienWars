""" THIS IS A TESTER FILE FOR ASTEROID CLASS!!!! """
""" okay the only two classes actually used in this file are Asteroid and its child CHICKEN JOCKEY!!! """
import random
import pygame
from Entities.Entity import *
from EntityTags import *
from math import pi
from pyglm import glm
import ResourceManager


class Asteroid(Entity):
    type = 'Asteroid'
    __slots__ = 'to_die',
    def __init__(self,pos,vel,rot,mass,img:Surface,tags:int):
        super().__init__(pos, vel,rot,mass,img,tags)
        self.cache_every = 3
        self.to_die = False
    
    def update(self,map:MapType,dt:float,game:GameType):
        self.rot += 1 * dt
        super().update(map,dt,game)
        self.dirty = True
        if self.to_die:
            self.dead = True
            children = 4
            t_offset = random.random()*2*pi
            if self.mass < 1:
                return
            smaller_surf = ResourceManager.tScaleBy(self.surf,0.5)
            
            for i in range(children):
                theta = i*2*pi/children + t_offset + random.random()*0.5
                dir = glm.vec2(glm.cos(theta),glm.sin(theta))
                a = Asteroid(self.pos+dir*5,
                             self.vel + dir * 100,
                             theta,
                             self.mass/4,
                             smaller_surf,
                             self.tags
                            )
                game.spawnEntity(a)
    
    def onCollide(self, other:Entity,info:CollisionInfo,normal:glm.vec2):
        if other.tags & E_CAN_DAMAGE:
            # assert isinstance(other,ICanDamage)
            self.to_die = True
        super().onCollide(other,info,normal)
class ChickenJockey(Asteroid):
    pass