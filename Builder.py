from math import pi
from pyglm import glm
from _random import Random

from Entities.Asteroid import Asteroid
from Entities.Bullet import Bullet
from Entities.Entity import Entity
from Entities.Spaceship import Spaceship

from Controllers.Controller import Controller
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
            'controllerType':Controller
        }
        self.scout = {
            'hp':3,
            'mass':2,
            'tags':E_CAN_BOUNCE,
            'img':ResourceManager.loadAlpha('./Images/TeamB/scout.png'),
            'controllerType':Controller
        }
        self.warship = {
            'hp':40,
            'mass':15,
            'tags':E_CAN_BOUNCE,
            'img':ResourceManager.loadAlpha('./Images/TeamB/warship.png'),
            'controllerType':Controller
        }
        self.mothership = {
            'hp':100,
            'mass':9999999,
            'tags':E_CAN_BOUNCE,
            'img':ResourceManager.loadColorKey('./Images/TeamB/warship.png',(255,255,255)),
            'controllerType':Controller
        }
    def buildEnemy(self,pos:glm.vec2,vel:glm.vec2,rot:float|None,alliance:str,/,mass:float,img,tags:int,hp:int,controllerType:type[Controller]):
        e = Spaceship(pos,vel,rot or _random.random()*2*pi,mass,img,tags,hp,alliance,controllerType())