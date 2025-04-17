from gametypes import *
import pygame
from pyglm import glm
from Controllers.Controller import Controller
from Entities.Spaceship import Spaceship
from Entities.Bullet import Bullet

class PlayerController(Controller):
    def init(self,entity:Spaceship):
        if entity.guns:
            self.selected_gun = entity.guns[0]
        else:
            self.selected_gun = None

    def update(self,entity:Spaceship,map:MapType,game:GameType):
        keys = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # updating forwards and backwards + velocity movement
        entity.move(
            glm.vec2(
                keys[pygame.K_w] - keys[pygame.K_s],
                keys[pygame.K_d] - keys[pygame.K_a]
            )
        )
        # changing rotation based on cursor positioning 
        difference = game.toWorldCoords(mouse_pos) - entity.pos 
        entity.rot = glm.atan(-difference.y, difference.x)
        entity.dirty = True

        if keys[pygame.K_SPACE] or mouse_pressed[0]:
            if self.selected_gun and self.selected_gun.tryFire(game.time):
                    pos = entity.pos + entity.vel * game.dt + \
                        glm.rotate(self.selected_gun.pos,-entity.rot)
                    bullet=Bullet.makeDefault(
                        pos,
                        glm.vec2(entity.vel),
                        entity.rot + self.selected_gun.rot,
                        entity
                    )
                    game.spawnEntity(bullet)
