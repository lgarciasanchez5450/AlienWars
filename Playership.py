from pyglm import glm
import ChunkManager
import pygame
import math
img=  pygame.image.load('./Images/ship.png')

def expDecay(a,b,decay:float,dt:float):
  return b+(a-b)*math.exp(-decay*dt)


class Playership(ChunkManager.Spaceship):
    def __init__(self, pos, rot, hp):
        _surf = img.convert_alpha()
        super().__init__(pos, rot, hp,_surf)

    def update(self,map:ChunkManager, dt):
        keys = pygame.key.get_pressed()
        force = glm.vec2(
            (keys[pygame.K_w] - keys[pygame.K_s]) * 1000,
            0
        )

        self.vel += glm.rotate(force,-self.rot) * dt * 2
        drot = keys[pygame.K_a] - keys[pygame.K_d]
        if drot:
            self.dirty = True
            self.rot += drot * dt
        self.pos += self.vel * dt
        self.vel = expDecay(self.vel,glm.vec2(),4,dt)

