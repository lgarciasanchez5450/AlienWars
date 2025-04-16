import math
from pyglm import glm

def expDecay(a,b,decay:float,dt:float):
  return b+(a-b)*math.exp(-decay*dt)
