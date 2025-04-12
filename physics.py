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
        _r.center = entity.pos
        for s_cpos in surrounding:
            if ents:=map.get(s_cpos):
                for other in ents:
                    if other is entity: continue
                    other.rect.center = other.pos
                    if _cr(other.rect):
                        if _m.overlap(other.mask,(other.rect.left-_r.left,other.rect.top-_r.top)):
                            entity.onCollide(other)