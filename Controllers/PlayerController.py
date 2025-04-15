from gametypes import *
import pygame
from pyglm import glm
from Controllers.Controller import Controller
from Entities.Spaceship import Spaceship
from utils import expDecay

class PlayerController(Controller):
    def init(self,entity:Spaceship):
        pass

    def update(self,entity:Spaceship,map:MapType,game:GameType):
        keys = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # updating forwards and backwards + velocity movement
        force = glm.vec2(
             (keys[pygame.K_w]) * 1000,
             0
        )
        # changing rotation based on cursor positioning 
        difference = game.toWorldCoords(mouse_pos) - entity.pos 
        entity.rot = glm.atan(-difference.y, difference.x)
        entity.dirty = True

        if keys[pygame.K_SPACE] or mouse_pressed[0]:
            if entity.atk_1:
                if entity.atk_1.next_atk_time < game.time:
                    game.spawnEntities(entity.atk_1.getBullets(glm.vec2(entity.pos)+40*glm.vec2(glm.cos(-entity.rot),glm.sin(-entity.rot)),entity.vel,entity.rot))
                    entity.atk_1.resetAttackTime(game.time)

        entity.vel += glm.rotate(force,-entity.rot) * game.dt * 2
        entity.n_vel = expDecay(entity.vel,glm.vec2(),1,game.dt)