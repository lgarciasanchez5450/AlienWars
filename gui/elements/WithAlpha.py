from ..core import *

class WithAlpha:
    __slots__ = 'obj','order_in_layer','update','surf','onResize'
    def __init__(self,obj:types.HasRect,/,alpha:int=255) -> None:
        self.obj= obj
        self.order_in_layer = obj.order_in_layer
        self.surf = Surface(self.obj.rect.size,const.SRCALPHA)
        self.surf.set_alpha(alpha)
        if hasattr(obj,'update'):
            self.update = obj.update #type: ignore
        if hasattr(obj,'onResize'):
            self.onResize = obj.onResize #type: ignore

    def setAlpha(self,alpha:int):
        self.surf.set_alpha(alpha)

    @property
    def rect(self):
        return self.obj.rect

    def draw(self,surf:Surface):
        r = self.rect
        x,y = r.topleft
        r.top = 0
        r.left = 0
        self.surf.fill((0,0,0,0))
        self.obj.draw(self.surf)
        r.left = x
        r.top = y
        surf.blit(self.surf,r)
