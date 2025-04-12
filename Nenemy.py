from ChunkManager import *
import random
img= pygame.image.load('./Images/nship.png')
import physics

def dprint(*args):
    import sys
    sys.stdout.write(' '.join([str(a) for a in args])+'\n')
    sys.stdout.flush()
class Goal:
    WANDER = 0
    RETREAT = 1
    PROTECT = 2
    ATTACK = 3
    def __init__(self,entity:Spaceship):
        self.entity = entity
    def update(self,map,game): ...
    def reload(self,map,game:"Game"): ...


class Wander(Goal):

    def reload(self,map,game:"Game"): 
        big_rect = pygame.Rect(0,0,300,300)
        big_rect.center = self.entity.pos
        self.around = [e for e in physics.get_colliding(big_rect) if e is not self.entity]
        self.target = glm.vec2(
            random.random()*MAP.w,
            random.random()*MAP.h
        )
        if (dst2:=glm.distance2(self.target,self.entity.pos)) > 100*100:
            #move target_closer 
            dst2 -= 100*100
            self.target += (self.entity.pos - self.target) * math.sqrt(dst2)*0.7
            
    def update(self,map,game:"Game"):
        dif = self.target - self.entity.pos
        target_rot = glm.atan(-dif.y,dif.x)
        d_rot = (target_rot - self.entity.rot) %TWO_PI
        if d_rot > TWO_PI:
            d_rot -= TWO_PI
        if abs(d_rot) > 0.1:
            self.entity.rot += d_rot * game.dt
            self.entity.dirty = True

class AttackGoal(Goal):
    def __init__(self, entity,target:Spaceship):
        super().__init__(entity)
        self.target = target

    def reload(self,map,game:"Game"): 
        big_rect = pygame.Rect(0,0,300,300)
        big_rect.center = self.entity.pos
        self.around = [e for e in physics.get_colliding(big_rect,map) if e is not self.entity]
        
    def update(self, map, game:"Game"):
        dpos = self.target.pos - self.entity.pos
        trot = glm.atan(-dpos.y,dpos.x)
        d_rot = (trot - self.entity.rot) % TWO_PI
        if d_rot > pi:
            d_rot -= TWO_PI
        if abs(d_rot) > 0.05:
            self.entity.rot += max(-1,min(d_rot,1)) * game.dt * 2
            self.entity.dirty = True
    
class Nenemy(Spaceship):
    team = 'B'
    every = 60
    _uid = 0
    def __init__(self, pos, rot,player:Spaceship):
        super().__init__(pos, rot, 3,img.convert_alpha())
        self.player = player
        self.every = 1
        self.id = Nenemy._uid
        self._goal = None
        self.goal = Goal.WANDER
        Nenemy._uid += 1

    def update(self, map, dt, input:Input,game:"Game"):
        if game.frame % Nenemy.every == self.id:
            self.higher_order_processing(map,dt,input,game)
        elif self._goal:
            self._goal.update(map,game)
      
        super().update(map,dt,input,game)

    def higher_order_processing(self,map:MapType,dt:float,input:Input,game:"Game"):
        if self.goal is None: 
            self.goal = Goal.WANDER
            self._goal = Wander(self)
            dprint('Goal Changed to Attack')

        elif self.goal is Goal.WANDER:
            big_rect = pygame.Rect(0,0,300,300)
            big_rect.center = self.pos
            for ent in physics.get_colliding(big_rect,map):
                if ent is self: continue
                if isinstance(ent,Spaceship):
                    if ent.team is not self.team:
                        dprint('Goal Changed to Attack')
                        self.goal = Goal.ATTACK
                        self._goal = AttackGoal(self,ent)
        self._goal.reload(map,game)
