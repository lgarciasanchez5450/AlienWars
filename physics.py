from ChunkManager import Entity,MapType,CHUNK_SIZE
def do_physics(entities:list[Entity],map:MapType):
    for entity in entities:
        cpos = (entity.pos//CHUNK_SIZE).to_tuple()
        surrounding = [(cpos[0]-1,cpos[1]-1),
                       (cpos[0]+0,cpos[1]-1),
                       (cpos[0]+1,cpos[1]-1),
                       (cpos[0]-1,cpos[1]+0),
                       (cpos[0]+0,cpos[1]+0),
                       (cpos[0]+1,cpos[1]+0),
                       (cpos[0]-1,cpos[1]+1),
                       (cpos[0]+0,cpos[1]+1),
                       (cpos[0]+1,cpos[1]+1)
                    ]
        _r = entity.rect
        _cr = entity.rect.colliderect
        _m = entity.mask
        for s_cpos in surrounding:
            if ents:=map.get(s_cpos):
                for other in ents:
                    if other is entity: continue
                    if _cr(other.rect):
                        if _m.overlap(other.mask,(other.rect.left-_r.left,other.rect.top-_r.top)):
                            entity.onCollide(other)

from pygame import Rect

def get_colliding(r:Rect,map:MapType):
    _cr = r.colliderect
    for cpos in collide_chunks2d(r.left,r.top,r.right,r.bottom,CHUNK_SIZE):
        if ents:=map.get(cpos):
            for other in ents:
                if _cr(other.rect):
                    yield other
                    
def collide_chunks2d(x1:float,y1:float,x2:float,y2:float,chunk_size:int): # type: ignore[same-name]
    cx1 = (x1 // chunk_size).__floor__()
    cy1 = (y1 // chunk_size).__floor__()
    cx2 = (x2 / chunk_size).__ceil__()
    cy2 = (y2 / chunk_size).__ceil__()
    return [(x,y) for x in range(cx1,cx2,1) for y in range(cy1,cy2,1)]
