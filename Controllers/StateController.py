from Controllers.Controller import Controller
from Entities.Spaceship import Spaceship
from pyglm import glm
import physics
from gametypes import *
from Attacks import Gun
from Entities.Bullet import Bullet
from pygame import Rect
import utils
from Controllers.States.WarshipState import *

class StateController[T](Controller):
    def __init__(self,initial_state:State,shared_state:T):
        self.state = initial_state
        self.shared_state = shared_state
        self.think_dt = 10

    def init(self,entity:Spaceship):
        self.t_think = 1

    def update(self,entity:Spaceship,map:MapType,game:GameType):
        self.t_think -= game.dt
        if self.t_think <= 0:
            self.t_think = self.think_dt
            self.state.think(self,entity,map,game)
        else:
            self.state.update(self,entity,map,game)

    def setState(self,state:State,*args,**kwargs):
        self.state = state
        state.start(*args,**kwargs)

    def onCollide(self,entity:Spaceship,other:EntityType,info:CollisionInfoType,collision_normal:Vec2):
        self.state.onCollide(self,entity,other,info,collision_normal)

    def copy(self) -> 'StateController':
        return type(self)(self.state.copy(),self.shared_state.copy() if self.shared_state is not None else None) #type: ignore