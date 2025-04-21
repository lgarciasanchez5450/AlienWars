import os
import typing
from pygame import Surface
from pygame import image
from pygame import transform
from pygame import typing as pgtyping
'''We only support one type of resource: Surface'''
CACHE_MAX_SIZE = 400
resources:dict[str,Surface] = {}
transformations:dict[tuple[Surface,str],Surface] = {}
r_dirs:dict[str,tuple[Surface,...]] = {}
def load(path:str,*post_processing:typing.Callable[[Surface],Surface|None]) -> Surface:
    if (surf := resources.get(path)) is None:
        surf = image.load(path)
        for process in post_processing:
            surf = process(surf) or surf
        resources[path] = surf
        assert len(resources) <= CACHE_MAX_SIZE,'Too Many Resources Loaded'
    return surf

def loadDir(path:str,*post_processing:typing.Callable[[Surface],Surface|None]) -> list[Surface]:
    if (surfs := r_dirs.get(path)) is None:
        surfs = []
        for name in os.listdir(path):
            fqn = os.path.join(path,name)
            surf = image.load(fqn)
            for process in post_processing: 
                surf = process(surf) or surf
            surfs.append(surf)
        r_dirs[path] = tuple(surfs)
    return list(surfs)

def loadAlpha(path:str) ->Surface:
    return load(path,Surface.convert_alpha)

def loadOpaque(path:str):
    return load(path,Surface.convert)

def loadColorKey(path:str,colorkey:pgtyping.ColorLike):
    return load(path,Surface.convert,lambda s: s.set_colorkey(colorkey))

def tScaleBy(surf:Surface,factor:float):
    t_hash = (surf,f'sb({factor})')
    if (n_surf := transformations.get(t_hash)) is None:
        n_surf = transform.scale_by(surf,factor)
        transformations[t_hash] = n_surf
    return n_surf



def sync(path:str,surf:Surface):
    assert path in resources
    resources[path] = surf

    