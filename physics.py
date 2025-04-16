from pyglm import glm
from pygame import Rect
from pygame import Mask
from gametypes import *
from ChunkManager import CHUNK_SIZE
class CollisionInfo:
    mask:Mask
    center_of_collision:glm.vec2
    set_bits:int
    __slots__ = 'mask','center_of_collision','set_bits'

def calc_collision_map(map:MapType):
    collisions:dict[frozenset,CollisionInfo] = {}
    for chunk in map.values():
        for entity in chunk:
            _r = entity.rect
            _cr = entity.rect.colliderect
            _mo = entity.mask.overlap_mask
            for other in chunk:
                if other is entity: continue
                if _cr(other.rect):
                    fs = frozenset([entity,other])
                    if fs in collisions: continue
                    mask =_mo(other.mask,(other.rect.left-_r.left,other.rect.top-_r.top))
                    set_bits = mask.count()
                    if set_bits:
                        info = CollisionInfo()
                        info.mask = mask
                        info.center_of_collision = glm.vec2(mask.centroid()) + entity.rect.topleft
                        info.set_bits = set_bits
                        entity.onCollide(other,info)
                        other.onCollide(entity,info)
                        collisions[fs] = info



def get_colliding(r:Rect,map:MapType):
    s = set()
    _cr = r.colliderect
    for cpos in collide_chunks2d(r.left,r.top,r.right,r.bottom,CHUNK_SIZE):
        if ents:=map.get(cpos):
            for other in ents:
                if other not in s and _cr(other.rect):
                    s.add(other)
                    yield other
                    
def collide_chunks2d(x1:float,y1:float,x2:float,y2:float,chunk_size:int): # type: ignore[same-name]
    cx1 = (x1 // chunk_size).__floor__()
    cy1 = (y1 // chunk_size).__floor__()
    cx2 = (x2 / chunk_size).__ceil__()
    cy2 = (y2 / chunk_size).__ceil__()
    return [(x,y) for x in range(cx1,cx2,1) for y in range(cy1,cy2,1)]
