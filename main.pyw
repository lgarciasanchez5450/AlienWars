import sys
import pygame

window = pygame.Window('GAME')
screen = window.get_surface()

from ChunkManager import * 
from Playership import Playership

FPS = 0

bg_image = pygame.image.load('./Images/T8g30s.png')
bg_image = pygame.transform.scale_by(bg_image,5)



entities:list[Entity] = []
camera_pos = glm.vec2()

player = Playership(glm.vec2(0,0),0,1)

entities.append(player)
half_screen_size = glm.vec2(window.size)/2
from Nenemy import Nenemy
import physics
import random
dt = 0
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

        if event.type == pygame.KEYDOWN: #TODO move some of this logic to player class and 
            if event.key == pygame.K_SPACE:
                entities.append(Bullet(glm.vec2(player.pos)+30*glm.vec2(glm.cos(-player.rot),glm.sin(-player.rot)),player.vel,player.rot))    
            if event.key == pygame.K_q:
                entities.append(
                    Nenemy(player.pos+glm.circularRand(50),glm.linearRand(0,2*pi),player)
                )


     
    map = build_map(entities)
    # update all entities
    for e in entities:
        e.update(map, dt)

    for e in entities:
        if e.dirty:
            e.regenerate_physics()

    #do physics
    physics.do_physics(entities,map)
    entities = list(filter(lambda x:not x.dead, entities))

    camera_pos = player.pos
    screen.blit(bg_image,-camera_pos+half_screen_size-glm.vec2(bg_image.get_size())//2)

    for e in entities:
        surf = e.surf
        # if type(e) is Bullet:
        #     print(e.pos-camera_pos+half_screen_size-glm.vec2(surf.get_size())//2,surf.get_size())
        screen.blit(surf,e.pos-camera_pos+half_screen_size-glm.vec2(surf.get_size())//2)
        
    window.flip()
    dt = clock.tick(FPS) / 1000
    window.title = str(dt*1000)+'ms'

