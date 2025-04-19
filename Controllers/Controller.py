from gametypes import *


class Controller:
    __slots__ = ()
    def init(self,entity:EntityType): ...

    def update(self,entity:EntityType,map:MapType,game:GameType): ...

    def onCollide(self,entity:EntityType,other:EntityType,info:CollisionInfoType,collision_normal:Vec2): ...

    def copy(self) -> 'Controller': ...