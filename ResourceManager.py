import typing
from pygame import Surface
from pygame import image
'''We only support one type of resource: Surface'''
CACHE_MAX_SIZE = 400
resources:dict[str,Surface] = {}

def load(path:str,*post_processing:typing.Callable[[Surface],Surface]) -> Surface:
    if (surf := resources.get(path)) is None:
        surf = image.load(path)
        for process in post_processing:
            surf = process(surf)
        resources[path] = surf
        assert len(resources) <= CACHE_MAX_SIZE,'Too Many Resources Loaded'
    return surf



def loadAlpha(path:str) ->Surface:
    return load(path,Surface.convert_alpha)

def loadOpaque(path:str):
    return load(path,Surface.convert)

def sync(path:str,surf:Surface):
    assert path in resources
    resources[path] = surf

    