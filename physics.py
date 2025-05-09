from pyglm import glm
from pygame import Rect
from pygame import Mask
from gametypes import *
import ChunkManager
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
            _cr = _r.colliderect
            _mo = entity.mask.overlap_mask
            _ma = entity.mask.overlap_area
            for other in chunk:
                if other is entity: continue
                if _cr(other.rect):
                    fs = frozenset([entity,other])
                    if fs in collisions: continue
                    x = other.rect.left - _r.left
                    y = other.rect.top - _r.top
                    mask =_mo(other.mask,(x,y))
                    set_bits = mask.count()
                    if set_bits:
                        dx = _ma(other.mask, (x + 1, y)) - _ma(other.mask, (x - 1, y))
                        dy = _ma(other.mask, (x, y + 1)) - _ma(other.mask, (x, y - 1))
                        collision_normal = glm.vec2(dx,dy)
                        info = CollisionInfo()
                        info.mask = mask
                        info.center_of_collision = glm.vec2(mask.centroid()) + entity.rect.topleft
                        info.set_bits = set_bits
                        entity.onCollide(other,info,collision_normal)
                        other.onCollide(entity,info,-collision_normal)
                        collisions[fs] = info



def get_colliding(r:Rect,map:MapType):
    s = set()
    _cr = r.colliderect
    for cpos in collide_chunks2d(r.left,r.top,r.right,r.bottom,ChunkManager.CHUNK_SIZE):
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


def linecast(origin:Vec2,dest:Vec2,map:MapType):
    '''This implementation is incorrect: TODO Use Proper voxel traversal raycast algo'''
    chunks_crossed = set()
    
    for i in range(200):
        i /= 200
        p = origin * (1-i) + dest * i
        cpos = glm.ivec2(p // ChunkManager.CHUNK_SIZE).to_tuple()
        if cpos in chunks_crossed: continue
        chunks_crossed.add(cpos)
        for entity in map.get(cpos,[]):
            raise NotImplementedError
    

def collide_line_rect(origin:Vec2,dir:Vec2,rect:Rect):
    if not dir.x: return rect.left < origin.x < rect.right
    if not dir.y: return rect.top < origin.y < rect.bottom
    
    t_top = rect.top / dir.y
    t_bottom = rect.bottom / dir.y
    t_left = rect.left / dir.x
    t_right = rect.right / dir.x

    pass