from pyglm import glm
import ChunkManager
from ChunkManager import Bullet
import pygame
from Input import Input
from Attacks import *
import math
img=  pygame.image.load('./Images/TeamA/Ship/0.png')

def expDecay(a,b,decay:float,dt:float):
  return b+(a-b)*math.exp(-decay*dt)


class Playership(ChunkManager.Spaceship):
    def __init__(self, pos, rot, hp):
        _surf = img.convert_alpha()
        super().__init__(pos, rot, hp,_surf)
        self.atk_1 = EightShotPassive()

    def update(self,map:ChunkManager.MapType, dt,game:"ChunkManager.Game"):
        keys = pygame.key.get_pressed()

        # updating forwards and backwards + velocity movement
        force = glm.vec2(
             (keys[pygame.K_w]) * 1000,
             0
        )
        self.vel += glm.rotate(force,-self.rot) * dt * 2
        self.pos += self.vel * dt
        self.vel = expDecay(self.vel,glm.vec2(),4,dt)

        if keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0] == True:
            if self.atk_1.next_atk_time < game.time:
                game.spawnEntities(self.atk_1.getBullets(glm.vec2(self.pos)+40*glm.vec2(glm.cos(-self.rot),glm.sin(-self.rot)),self.vel,self.rot))
                self.atk_1.resetAttackTime(game.time)
        # changing rotation based on cursor positioning 
        mouse_pos = pygame.mouse.get_pos()
        difference = game.toWorldCoords(mouse_pos) - self.pos 
        # print(input.toWorldCoords(mouse_pos))
        self.rot = glm.atan(-difference.y, difference.x)
        self.dirty = True
        super().update(map, dt, game)