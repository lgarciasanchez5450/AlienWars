'''
Framework for building Graphical User Interfaces for existing applications\n
This has been used to make:\n
Pixel Art Program\n
Gravity Sim\n
Music Player (similar to Spotify)\n
Notes Application (trashy)
'''
#lmty
import time
import pygame
pygame.init()

from pygame import draw
from pygame import font
from pygame import Rect
from pygame import scrap
from pygame import image
from pygame import Surface
from pygame import display
from pygame import gfxdraw
from pygame import transform
from pygame import constants as const
from pygame.time import Clock
from src.Utils import advanced_color #type: ignore
from src.Utils import unicode_constants as u_const #type: ignore
from src.Utils.events import Event
from Utils.gui.core.types import * #type: ignore
import src.Input as Input_
from src.Input import Input
from src.Input import getInput
from utils2 import binaryApproximate
from utils2 import expDecay
pygame.key.set_repeat(400,20) #this feels closest to how windows does its key repeats
from Utils.debug import Tracer

WHEEL_SENSITIVITY = 7
SCROLL_SMOOTHING = .1
MONITOR_WIDTH = display.Info().current_w
MONITOR_HEIGHT = display.Info().current_h
DOUBLE_CLICK_THRESHOLD = 0.5 #move this to settings

def neg(c:Callable[P,bool]):
  def wrapper(*args:P.args,**kwargs:P.kwargs):
    return not c(*args,**kwargs)
  return wrapper

def set_WHEEL_SENSITIVITY(i:int) -> None:
  global WHEEL_SENSITIVITY
  WHEEL_SENSITIVITY = i

def set_SCROLL_SMOOTHING(value:float):
  assert value > 0,'Scroll Smoothing Must be a positive value'
  global SCROLL_SMOOTHING
  SCROLL_SMOOTHING = value

class ToPixelsError(Exception): ...

class KeyBoundFunction:
  __slots__ = 'func','keybinds','consume'
  def __init__(self,func:EventHook,keybinds:list[tuple[int,int]],consume=True):
    self.func = func
    self.keybinds = keybinds
    self.consume = consume

  def update(self,input:Input) -> None:
    if self.consume:
      if input.consumeKeys(*self.keybinds):
        self.func()
    else:
      if input.checkKeys(*self.keybinds):
        self.func()

class KeyBoundFunctionConditional(KeyBoundFunction):
  __slots__ = 'condition',
  def __init__(self,condition:Callable[[],Any], func:Callable[[],Any],keybinds:list[tuple[int,int]],consume = True):
    super().__init__(func,keybinds,consume)
    self.condition = condition
  
  def update(self, input):
    if self.condition():
      super().update(input)

class SelectionBase(Button):
  __slots__ = 'pos','yoffset'
  def __init__(self,pos:tuple[int,int],size:tuple[int,int],color_scheme:ColorScheme,onDown:EventHook|None = None,onUp:EventHook|None = None) -> None:
    self.pos = pos
    super().__init__(pos,size,color_scheme,onDown,onUp)
    self.setYOffset(0)  

  def onYOffsetChangeHook(self,offsetY:int): ...
  def getYOffSet(self) -> int: return self.yoffset

  def setYOffset(self,y:int): 
    self.yoffset = y
    self.rect.top = self.pos[1] - y
    self.onYOffsetChangeHook(y)


class Region(DrawBase):
  def __init__(self,rect:Rect):
    self.rect = rect
    self.active = True
    self.to_update:list[SupportsUpdate] = []
    self.to_draw:list[SupportsDraw] = []
    self.to_resize:list[SupportsResize] = []

  def setActive(self,active:bool=True):
    self.active = active
  def setInactive(self):
    self.setActive(False)

  def addObject(self,element:SupportsDraw|SupportsUpdate):
    if hasattr(element,'update'):
      self.to_update.append(element) #type: ignore
    if hasattr(element,'draw'):
      self.to_draw.append(element) #type: ignore
      self.to_draw.sort(key=lambda x:x.order_in_layer)
    if hasattr(element,'onResize'):
      self.to_resize.append(element) #type: ignore
  
  def addObjects(self,*elements:SupportsDraw|SupportsUpdate) -> "Region":
    for element in elements:
      self.addObject(element)
    return self
  
  def update(self,input:Input):
    if not self.active: return
    x = self.rect.left
    y = self.rect.top
    input.mousex -= x
    input.mousey -= y    
    for u in self.to_update:
      u.update(input)
    input.mousex += x
    input.mousey += y
    
  @Tracer().traceas('Region')
  def onResize(self,size:tuple[int,int]):
    for ui in self.to_resize:
        ui.onResize(self.rect.size)

  def draw(self,surf:Surface):
    if not self.active: return
    srect = surf.get_rect()
    if srect.colliderect(self.rect):
      sub = surf.subsurface(self.rect.clip(srect))
      for ui in self.to_draw:
        ui.draw(sub)


def findAllFiles(ending:str,addedPath:str = ''):
  '''Find all files with a specific extension like .png or .txt'''
  from os import walk
  for _root, _dirsfiles in walk('./'+addedPath): 
    for file in files:
      if file.endswith(ending):
        yield str(file)

class FontRule:
  def __init__(self,min:int=5,max:int=30):
    self.min = min
    self.max = max

  def __call__(self,f:font.Font,text:str,r:Rect):
    f.set_point_size(min(self.max,max(self.min,r.height-4)))
    s = f.size(text)
    if s[0] > r.width:
      def search(i:int):
        f.set_point_size(i)
        return f.size(text)[0]
      binaryApproximate(search,r.width,self.min,f.get_point_size())

# def aaarc(source:Surface,color:tuple[int,int,int]|str,center:tuple[float,float],radius:float,start_angle:float,end_angle:float,resolution:int = 0):
#   #if end_angle < start_angle: end_angle += 2*3.141592653589
#   from math import cos,sin
#   #if start_angle > end_angle: return
#   if start_angle==end_angle: return
#   points = [center]
#   dif = end_angle-start_angle
#   resolution = max(int(dif*10),1) if resolution <= 0 else resolution
#   for i in range(resolution+1):
#     a = start_angle + i*dif/resolution
#     points.append((center[0] + cos(a)*radius,center[1]-sin(a)*radius))
#   gfxdraw.aapolygon(source,points,color)
#   gfxdraw.filled_polygon(source,points,color)
