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

    def update(self,map:ChunkManager, dt, camera_pos):
        keys = pygame.key.get_pressed()
        force = glm.vec2(
             (keys[pygame.K_w] - keys[pygame.K_s]) * 1000,
             0
        )

        self.vel += glm.rotate(force,-self.rot) * dt * 2
        # drot = keys[pygame.K_a] - keys[pygame.K_d]
        # if drot:
        #     self.dirty = True
        #     self.rot += drot * dt
        self.pos += self.vel * dt
        self.vel = expDecay(self.vel,glm.vec2(),4,dt)

        # if keys[pygame.K_w]:
        #     self.pos.y -= 300 * dt
        # if keys[pygame.K_s]:
        #     self.pos.y += 300 * dt
        # if keys[pygame.K_a]:
        #     self.pos.x -= 300 * dt
        # if keys[pygame.K_d]:
        #     self.pos.x += 300 * dt
        mouse_pos = pygame.mouse.get_pos()

        # get 
        difference = mouse_pos - camera_pos

        self.rot = glm.atan(difference.y, difference.x)

        self.dirty = True





        

