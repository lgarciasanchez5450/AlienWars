from pyglm import glm
from gametypes import *
from pygame import Surface

class Gun:
    __slots__ = 'pos','rot','fire_rate','next_fire_time'
    def __init__(
            self,
            pos:glm.vec2|tuple[float,float],
            rot:float,
            rpm:float #rounds per minute
    ):
        self.pos = glm.vec2(pos)
        self.rot = rot
        self.fire_rate = rpm
        self.next_fire_time = 0

    def tryFire(self,curr_time:float):
        if curr_time > self.next_fire_time:
            self.next_fire_time = curr_time + 60/self.fire_rate
            return True
        return False

    def canFire(self,curr_time:float):
        return curr_time > self.next_fire_time
    
    def fire(self,curr_time:float):
        assert self.canFire(curr_time)
        self.next_fire_time = curr_time + 60/self.fire_rate
    
    def copy(self):
        return Gun(self.pos,self.rot,self.fire_rate)


class NamedGun(Gun):
    name:str
    img:Surface
    __slots__ = 'name','img'
    def __init__(
            self,
            pos:glm.vec2|tuple[float,float],
            rot:float,
            rpm:float, #rounds per minute
            name:str,
            img:Surface
    ):
        super().__init__(pos,rot,rpm)
        self.name = name
        self.img = img