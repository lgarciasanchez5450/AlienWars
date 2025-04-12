import sys
import pygame

window = pygame.Window('GAME')
screen = window.get_surface()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
    window.flip()