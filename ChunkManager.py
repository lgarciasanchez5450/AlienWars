import glm
import typing
import pygame
import math
from Input import Input
from math import pi
if typing.TYPE_CHECKING:
    from game import Game
RAD_TO_DEG = 180 / pi
DEG_TO_RAD = pi / 180
TWO_PI = 2*pi

MAP = pygame.Rect(0,0,10_000,10_000)

type MapType = dict[tuple[int,int],list['Entity']]
NULL_SURF = pygame.Surface((0,0))
class Entity:
    pos:glm.vec2 # current position 
    vel:glm.vec2 # current velocity
    rot:float
    surf:pygame.Surface # surface to draw each frame
    dirty:bool
    dead:bool = False
    # The Following are for physics
    rect:pygame.Rect # bounding Rect of the surface
    mask:pygame.Mask # mask from surface
    def __init__(self,pos:glm.vec2,rot:float):
        self.pos = pos
        self.rot = rot
        self.vel = glm.vec2()
        self._surf = NULL_SURF
        self.dirty = True
    
    def update(self,map:MapType,dt:float,input:Input,game:"Game"):
        self.rect.center = self.pos
    
    def regenerate_physics(self):
        self.surf = pygame.transform.rotate(self._surf,self.rot*RAD_TO_DEG)
        self.rect = self.surf.get_rect()
        self.rect.center = self.pos
        self.mask = pygame.mask.from_surface(self.surf)
    
    def onCollide(self,other:"Entity"): ...

class Bullet(Entity):
    dir:glm.vec2
    dmg = 1
    def __init__(self,pos:glm.vec2,rot:float):
        super().__init__(pos,rot)
        self.dir = glm.vec2(math.cos(rot),math.sin(-rot))
        self._surf = pygame.Surface((10,5))
        self._surf.set_colorkey('black')
        self._surf.fill('red')
        self._surf.set_at((0,0),'black')
        self.t = 5
        self.vel = self.dir *  200
        self.rect = pygame.Rect()
    
    def regenerate_physics(self):
        super().regenerate_physics()

    def update(self,map:MapType,dt:float,input:Input,game:"Game"):
        self.pos += self.vel * dt
        self.t -= dt
        if self.t < 0: self.dead = True
        self.rect.center = self.pos

    def onCollide(self, other):
        if isinstance(other,Spaceship):
            self.dead = True


class Attack:
    reload_time:float
    next_atk_time:float
    bullet_power:float
    def resetAttackTime(self,cur_time:float):
        self.next_atk_time = cur_time + self.reload_time
    def makeBullet(self,pos,bvel,rot) -> Bullet: ...

class Spaceship(Entity):
    team:str = 'A'
    rot:float
    hp:float
    hp_max:float
    atk_1:Attack
    atk_2:Attack

    def __init__(self,pos,rot,hp,img:pygame.Surface):
        super().__init__(pos,rot)
        self.hp = hp
        self.hp_max = hp
        self._surf = img
        self.rect = self._surf.get_rect()

    def onCollide(self, other):
        if isinstance(other,Bullet):
            self.hp -= other.dmg
            if self.hp <= 0:
                self.dead = True

CHUNK_SIZE = 100

def build_map(ships:list[Entity]):
    #first hash everything
    map:MapType = {}
    for ship in ships:
        cpos = glm.ivec2(ship.pos // CHUNK_SIZE).to_tuple()
        if cpos not in map:
            map[cpos] = [ship]
        else:
            map[cpos].append(ship)
    return map
        
    
    

