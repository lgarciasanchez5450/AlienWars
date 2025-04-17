from Controllers.Controller import Controller
from Entities.Spaceship import Spaceship
from pyglm import glm
import physics
from gametypes import *
from Attacks import Gun
from Entities.Bullet import Bullet
from Controllers.FighterController import StateMachineController
from pygame import Rect
import utils
from Controllers.States import *

class StateController(Controller):
    def __init__(self,states:list[State]):
        self.states:dict[int,State] = {state.id:state.copy() for state in states}

    def init(self,entity:Spaceship):
        self.t_think = 1
        
        self.setState(StateIdle.id)

    def update(self,entity:Spaceship,map:MapType,game:GameType):
        self.t_think -= game.dt
        if self.t_think <= 0:
            self.t_think = 10
            self.states[self.state].think(self,entity,map,game)
        else:
            self.states[self.state].update(self,entity,map,game)

    def setState(self,state:int,*args,**kwargs):
        self.state = state
        self.states[state].start(*args,**kwargs)

    def copy(self) -> 'StateController':
        return type(self)(list(self.states.values()))