import typing
from gametypes import *
E_CAN_DAMAGE = 0b1
E_IS_PLAYER  = 0b10
E_CAN_BOUNCE = 0b100



### The Classes Below are not used in game, they are only used to type check the entity Tags above ###
if __debug__:
    @typing.runtime_checkable
    class ICanDamage(typing.Protocol):
        def __new__(cls): raise SyntaxError
        dmg:int