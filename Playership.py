from pyglm import glm
import ChunkManager
from ChunkManager import Bullet
import pygame
from Input import Input
import math
img=  pygame.image.load('./Images/ship.png')

def expDecay(a,b,decay:float,dt:float):
  return b+(a-b)*math.exp(-decay*dt)


class Playership(ChunkManager.Spaceship):
    def __init__(self, pos, rot, hp):
        _surf = img.convert_alpha()
        super().__init__(pos, rot, hp,_surf)

    def update(self,map:ChunkManager.MapType, dt, input:Input,game:"ChunkManager.Game"):
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
            game.entities.append(Bullet(glm.vec2(self.pos)+30*glm.vec2(glm.cos(-self.rot),glm.sin(-self.rot)),self.vel,self.rot))  

        # changing rotation based on cursor positioning 
        mouse_pos = pygame.mouse.get_pos()
        difference = input.toWorldCoords(mouse_pos) - self.pos 
        print(input.toWorldCoords(mouse_pos))
        self.rot = glm.atan(-difference.y, difference.x)
        self.dirty = True





        

