'''
This module is purely for type-hinting purposes ONLY
importing this module should not have any side effects 
(i.e. this module should only import typing)
'''

import typing
if typing.TYPE_CHECKING:
    from Entities.Entity import Entity
    from game import Game
    from Attacks import Gun
    from Controllers.Controller import Controller
    from pyglm import glm
    from physics import CollisionInfo
__all__ = [
    'MapType','GameType','GunType','EntityType','ControllerType','Vec2','CollisionInfoType'
]


type MapType = dict[tuple[int,int],list['Entity']]
type GameType = 'Game'
type GunType = 'Gun'
type EntityType = 'Entity'
type ControllerType = 'Controller'
type Vec2 = 'glm.vec2'
type CollisionInfoType = 'CollisionInfo'