import random
from ChunkManager import BG_CHUNK_SIZE
from pygame import Surface
from pygame import image
from pygame import draw
import os
r_inst = random.Random()
stars = []
def loadStars():
    for name in os.listdir('./Images/Stars'):
        fqn = os.path.join('./Images/Stars',name)
        try:
            stars.append(image.load(fqn).convert_alpha())
        except:pass
    assert stars
import time
def generate(x:int,y:int) -> Surface:
    t_start = time.perf_counter()
    surf = Surface((BG_CHUNK_SIZE,BG_CHUNK_SIZE))
    s = [(x-1,y-1),
        (x+0,y-1),
        (x+1,y-1),
        (x-1,y+0),
        (x+0,y+0),
        (x+1,y+0),
        (x-1,y+1),
        (x+0,y+1),
        (x+1,y+1)
    ]
    if not stars:loadStars()
    for cpos in s:
        for star_x,star_y,star_index in get_stars(*cpos,1):
            star_surf= stars[star_index%len(stars)]
            surf.blit(star_surf,(star_x+(cpos[0]-x)*BG_CHUNK_SIZE,star_y+(cpos[1]-y)*BG_CHUNK_SIZE))
    t_end = time.perf_counter()
    # print(f'gen in: {(t_end-t_start)*1000:.2f} ms')
    draw.rect(surf,'red',surf.get_rect(),2)

    return surf
def get_stars(x:int,y:int,stars:int) -> list[tuple[int,int,int]]:
    r_inst.seed(hash((x,y)))
    return [(r_inst.randint(0,BG_CHUNK_SIZE-1),r_inst.randint(0,BG_CHUNK_SIZE-1),r_inst.randint(0,10)) for i in range(stars)]

