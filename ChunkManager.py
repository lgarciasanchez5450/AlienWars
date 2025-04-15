import pygame
import typing
from math import pi
from pyglm import glm
from pygame import Surface
from gametypes import *

RAD_TO_DEG = 180 / 3.1415926535897932384626
DEG_TO_RAD =  3.1415926535897932384626 / 180
TWO_PI = 2*3.1415926535897932384626
MAP = pygame.Rect(0,0,10_000,10_000)

NULL_SURF = pygame.Surface((0,0))


CHUNK_SIZE = 300
BG_CHUNK_SIZE = CHUNK_SIZE*2

def build_map(entities:list[EntityType]):
    #first hash everything
    map:MapType = {}
    for ent in entities:
        assert type(ent.pos) is glm.vec2, f'Ship:{ent}'
        cpos = glm.ivec2(ent.pos // CHUNK_SIZE).to_tuple()
        if cpos not in map:
            map[cpos] = [ent]
        else:
            map[cpos].append(ent)
    return map



    

