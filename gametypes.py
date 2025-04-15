'''
This module is purely for type-hinting purposes ONLY
importing this module should not have any side effects 
(i.e. this module should only import typing)
'''

import typing
if typing.TYPE_CHECKING:
    from Entities.Entity import Entity
    from game import Game
    from Attacks import Attack
    from Controllers.Controller import Controller

__all__ = [
    'MapType','GameType','AttackType','EntityType','ControllerType'
]


type MapType = dict[tuple[int,int],list['Entity']]
type GameType = 'Game'
type AttackType = 'Attack'
type EntityType = 'Entity'
type ControllerType = 'Controller'