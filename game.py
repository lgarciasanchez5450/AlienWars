import sys
import pygame

window = pygame.Window('GAME')
screen = window.get_surface()

from ChunkManager import * 
from Playership import Playership

FPS = 70

bg_image = pygame.image.load('./Images/T8g30s.png')
bg_image = pygame.transform.scale_by(bg_image,5)



camera_pos = glm.vec2()

player = Playership(glm.vec2(0,0),0,1)

half_screen_size = glm.vec2(window.size)/2
from Nenemy import Nenemy
import physics
from Input import Input
import random
dt = 0
clock = pygame.time.Clock()
inp = Input()
inp.screen_size = glm.vec2(window.size)
inp.camera_pos = glm.vec2()

class Game:
    def __init__(self):
        self.entities:list[Entity] = []
        self.clock = clock
        self.input = Input()

        self.player = Playership(
            glm.vec2(0,0),
            pi/2,
            10
        )
        self.entities.append(self.player)
        self.dt = 0

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN: #TODO move some of this logic to player class and 
                    if event.key == pygame.K_SPACE:
                        self.entities.append(Bullet(glm.vec2(player.pos)+30*glm.vec2(glm.cos(-player.rot),glm.sin(-player.rot)),player.vel,player.rot))    
                    if event.key == pygame.K_q:
                        self.entities.append(
                            Nenemy(player.pos+glm.circularRand(50),glm.linearRand(0,2*pi),player)
                        )

            map = build_map(self.entities)
            # update all entities
            for e in self.entities:
                e.update(map, self.dt, inp,self)

            for e in self.entities:
                if e.dirty:
                    e.regenerate_physics()

            #do physics
            physics.do_physics(self.entities,map)
            self.entities = list(filter(lambda x:not x.dead, self.entities))

            inp.camera_pos = player.pos
            screen.blit(bg_image,-inp.camera_pos+half_screen_size-glm.vec2(bg_image.get_size())//2)

            for e in self.entities:
                surf = e.surf
                # if type(e) is Bullet:
                #     print(e.pos-camera_pos+half_screen_size-glm.vec2(surf.get_size())//2,surf.get_size())
                screen.blit(surf,e.pos-inp.camera_pos+half_screen_size-glm.vec2(surf.get_size())//2)
                
            window.flip()
            dt = clock.tick(FPS) 
            window.title = str(dt)+'ms'
            self.dt  = dt/ 1000

if __name__=='__main__':
    g = Game()
    g.run()