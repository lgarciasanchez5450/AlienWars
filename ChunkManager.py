import typing
import pygame
from math import pi
RAD_TO_DEG = 180 / pi
DEG_TO_RAD = pi / 180

type MapType = dict[tuple[int,int],list['Entity']]

class Entity:
    pos:pygame.Vector2
    
    def update(self,map:MapType): ...
    def get_surf(self): ...

class Bullet(Entity):
    rot:float
    dir:pygame.Vector2
    def __init__(self,pos:pygame.Vector2,rot:float):
        self.pos = pos
        self.rot = rot
        self.dir = pygame.Vector2.from_polar(self.rot)
        self.surf = pygame.Surface((10,5))
        self.surf = pygame.transform.rotate(self.surf,rot*RAD_TO_DEG)        

    def update(self,map:MapType):
        pass

    def get_surf(self):
        return self.surf


class Attack:
    reload_time:float
    next_atk_time:float
    bullet_power:float
    def makeBullet(self) -> Bullet: ...

class Spaceship(Entity):
    rot:float
    hp:float
    hp_max:float
    atk_1:Attack
    atk_2:Attack

    def __init__(self,pos,rot,hp):
        self.pos = pos
        self.rot = rot
        self.hp =hp


CHUNK_SIZE = 10

def build_map(ships:list[Entity]):
    #first hash everything
    map:MapType = {}
    for ship in ships:
        cpos = ship.pos / CHUNK_SIZE
        cpos = cpos.x,cpos.y
        if cpos not in map:
            map[cpos] = [ship]
        else:
            map[cpos].append(ship)
    return map
        
    
    

