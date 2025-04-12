import sys
import pygame

window = pygame.Window('GAME')
screen = window.get_surface()

class Spaceship:
    def __init__(self,pos,rotation):
        self.pos = pos
        self.rotation = rotation
    
    def draw(self):
        pass
camera_pos = pygame.Vector2()

bg_image = pygame.image.load('./Images/T8g30s.png')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    screen.blit(bg_image,-camera_pos)
    window.flip()

