import sys
import pygame

window = pygame.Window('GAME')
screen = window.get_surface()

from ChunkManager import * 



bg_image = pygame.image.load('./Images/T8g30s.png')
bg_image = pygame.transform.scale_by(bg_image,5)

entities:list[Entity] = []
camera_pos = pygame.Vector2()
from Playership import Playership
player = Playership(pygame.Vector2(0,0),0,100000000000000000)
entities.append(player)
half_screen_size = pygame.Vector2(window.size)/2
dt = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
    
    map = build_map(entities)
    for e in entities:
        e.update(map, dt)
    camera_pos = player.pos
    screen.blit(bg_image,-camera_pos+ half_screen_size)
    for e in entities:
        surf = e.get_surf()
        screen.blit(surf,e.pos-camera_pos+half_screen_size)
    window.flip()
    dt = pygame.time.Clock().tick(60)

