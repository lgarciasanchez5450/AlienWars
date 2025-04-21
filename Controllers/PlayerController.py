from gametypes import *
import pygame
from pyglm import glm
from Controllers.Controller import Controller
from Entities.Spaceship import Spaceship
from Entities.Bullet import Bullet
class PlayerAction:
    name:str
    img:pygame.Surface

    def __init__(self,name:str,img:pygame.Surface,spa:float):
        self.name = name
        self.img = img
        self.spa = spa #seconds per action
        self._next_time = 0.0
    def percentLeft(self,time:float) -> float:
        time_left = max(self._next_time - time,0)
        return time_left / self.spa

    def isAvailable(self,time:float) -> bool:
        return time >= self._next_time
    
    def reset(self,time:float):
        self._next_time = time + self.spa

class PlayerActionGun(PlayerAction):
    def __init__(self, name: str, img: pygame.Surface,gun:GunType):
        self.name = name
        self.img = img
        self.gun = gun

    def isAvailable(self, time: float) -> bool:
        return self.gun.canFire(time)
    
    def percentLeft(self, time: float) -> float:
        time_left = max(self.gun.next_fire_time - time,0)
        total_time = 60 / self.gun.fire_rate
        percent_left = time_left / total_time
        return percent_left
    
    def reset(self,time:float):
        self.gun.fire(time)
    
class PlayerController(Controller):
    def init(self,entity:Spaceship):
        import ResourceManager
        self.a_charge = PlayerAction('Charge',ResourceManager.loadAlpha('./Images/attack_pics/charge.png'),5)
        self.a_shoot = PlayerAction('Shoot',ResourceManager.loadAlpha('./Images/attack_pics/basic_atk.png'),1/2)

    def update(self,entity:Spaceship,map:MapType,game:GameType):
        keys = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        # updating forwards and backwards + velocity movement
        movement = glm.vec2(
                    keys[pygame.K_w] - keys[pygame.K_s],
                    keys[pygame.K_d] - keys[pygame.K_a]
                )
        
        entity.move(movement)
        # changing rotation based on cursor positioning 
        difference = game.toWorldCoords(mouse_pos) - entity.pos 
        entity.rot = glm.atan(-difference.y, difference.x)
        entity.dirty = True

        if keys[pygame.K_LSHIFT] and self.a_charge.isAvailable(game.time):
            self.a_charge.reset(game.time)
            def m():
                t_start = game.time
                t_end = t_start + 0.5
                dir = glm.normalize(difference)
                while game.time < t_end:
                    entity.vel += dir * ((1-(2*(game.time-t_start))**2) * entity.engine_force * game.dt / entity.mass * 2)
                    yield
            game.asyncCtx.addCoroutine(m())

        if mouse_pressed[0] and self.a_shoot.isAvailable(game.time):
            gun = entity.guns[0]
            self.a_shoot.reset(game.time)
            pos = entity.pos + entity.vel * game.dt + \
                glm.rotate(gun.pos,-entity.rot)
            bullet=Bullet.makeDefault(
                pos,
                glm.vec2(entity.vel),
                entity.rot + gun.rot,
                entity
            )
            game.spawnEntity(bullet)

                    




            
                    
