from ChunkManager import *
from Attacks import *
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
        self.around = [e for e in physics.get_colliding(big_rect,map) if e is not self.entity]
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
        if d_rot > pi:
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
        ent = self.entity
        dpos = self.target.pos - ent.pos
        trot = glm.atan(-dpos.y,dpos.x)
        d_rot = (trot - self.entity.rot) % TWO_PI
        if d_rot > pi:
            d_rot -= TWO_PI
        if abs(d_rot) > 0.05:
            ent.rot += max(-1,min(d_rot,1)) * game.dt * 2
            ent.dirty = True
        if ent.atk_1.next_atk_time < game.time:
            pos = glm.vec2(ent.pos)+30*glm.vec2(glm.cos(-ent.rot),glm.sin(-ent.rot))
            game.entities.append(ent.atk_1.makeBullet(pos,ent.vel,ent.rot))
            ent.atk_1.resetAttackTime(game.time)


class RetreatGoal(Goal):
    def __init__(self, entity):
        super().__init__(entity)

    def reload(self, map, game):
        big_rect = pygame.Rect(0,0,300,300)
        big_rect.center = self.entity.pos
        self.flee_from:list[Spaceship] = []
        for e in physics.get_colliding(big_rect,map):
            if isinstance(e,Spaceship) and e.team != self.entity.team:
                self.flee_from.append(e)

    def update(self, map, game):
        ent = self.entity
        sum_pos = glm.vec2()
        for ent in self.flee_from:
            sum_pos += ent.pos
        sum_pos /= len(self.flee_from)

        dpos = sum_pos - ent.pos
        trot = glm.atan(-dpos.y,-dpos.x)
        d_rot = (trot - self.entity.rot) % TWO_PI
        if d_rot > pi:
            d_rot -= TWO_PI
        if abs(d_rot) > 0.05:
            ent.rot += max(-1,min(d_rot,1)) * game.dt * 2
            ent.dirty = True

class Nenemy(Spaceship):
    team = 'B'
    every = 60
    _uid = 0
    def __init__(self, pos, rot):
        super().__init__(pos, rot, 3,img.convert_alpha())
        self.every = 1
        self.id = Nenemy._uid
        self
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
        dprint('hop')
        if self._goal is None: 
            self.goal = Goal.WANDER
            self._goal = Wander(self)
            dprint('Goal Changed to Wander')
        if self.hp/self.hp_max < 0.2 and self.goal != Goal.RETREAT:
            self.goal = Goal.RETREAT
            self._goal = RetreatGoal(self)
            dprint('changin to retreat goal')
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


type enemytype = typing.Literal['basic','mothership']

def enemyFactory(type:enemytype,pos,rot):
    if type == 'basic':
        emy = Nenemy(pos,rot)
        emy.atk_1 = BasicEnemyAttack()
        return emy
    elif type== 'mothership':
        emy = Nenemy(pos,rot)
        raise NotImplementedError('lol not made yet :)')
    