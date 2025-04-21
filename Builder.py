from math import pi
from pyglm import glm
from _random import Random

from Entities.Asteroid import Asteroid
from Entities.Bullet import Bullet
from Entities.Entity import Entity
from Entities.Spaceship import Spaceship
from Attacks import Gun

from Controllers.Controller import Controller
from Controllers.StateController import StateController
from Controllers.States import WarshipState
from Controllers.States import FighterState
import ResourceManager
from EntityTags import *


_random = Random()
class Builder:
    def __init__(self) -> None:
        self.fighter = {
            'hp':10,
            'mass':5,
            'tags':E_CAN_BOUNCE,
            'img':ResourceManager.loadAlpha('./Images/TeamB/0.png'),
            'controller':StateController(FighterState.Wander(),None),
            'guns':[Gun((35,0),0,120)],
            'engine_force':3000
        }
        self.scout = {
            'hp':3,
            'mass':2,
            'tags':E_CAN_BOUNCE,
            'img':ResourceManager.loadAlpha('./Images/TeamB/scout.png'),
            'controller':Controller(),
            'engine_force':3000,
            'guns':[Gun((40,0),0,20)],


        }
        self.warship = {
            'hp':40,
            'mass':150,
            'tags':E_CAN_BOUNCE,
            'img':ResourceManager.loadAlpha('./Images/TeamB/warship.png'),
            'controller':StateController(WarshipState.Idle(),WarshipState.SharedState()),
            'guns':[Gun((80,30),0,30)],
            'engine_force':2000,
            'cache_every':0
        }
        self.mothership = {
            'hp':100,
            'mass':9999999,
            'tags':E_CAN_BOUNCE,
            'img':ResourceManager.loadColorKey('./Images/TeamB/warship.png',(255,255,255)),
            'controller':Controller()
        }

    def buildEnemy(self,pos:glm.vec2,vel:glm.vec2,rot:float|None,alliance:str,/,mass:float,img,tags:int,hp:int,guns:list[Gun],engine_force:float,controller:Controller,**kwargs):
        ship = Spaceship(
            pos,
            vel,
            rot if rot is not None else glm.linearRand(0,2*pi),
            mass,
            img,
            tags,
            hp,
            alliance,
            [g.copy() for g in guns],
            engine_force,
            controller.copy()
        )
        ship.cache_every = kwargs.get('cache_every',2)
        return ship