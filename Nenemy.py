from ChunkManager import *
import random
img= pygame.image.load('./Images/nship.png')
import physics
class Goal:
    WANDER = 0
    RETREAT = 1
    PROTECT = 2
    ATTACK = 3
    def update(self,map,game): ...

class Wander(Goal):
    def __init__(self,entity:Spaceship):
        self.entity = entity

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
        

        
class Nenemy(Spaceship):
    every = 60
    _uid = 0
    def __init__(self, pos, rot,player:Spaceship):
        super().__init__(pos, rot, 3,img)
        self.player = player
        self.every = 1
        self.id = Nenemy._uid
        self.goal = Wander(self)
        Nenemy._uid += 1

    def update(self, map, dt, input:Input,game:"Game"):
        if game.frame % Nenemy.every == self.id:
            self.higher_order_processing(map,dt,input,game)
        else:
            self.goal.update
        dpos = self.player.pos - self.pos
        trot = glm.atan(-dpos.y,dpos.x)
        drot = trot - self.rot
        if drot:
            self.rot += max(-1,min(drot,1)) * dt * 2
            self.dirty = True
        super().update(map,dt,input,game)

    def higher_order_processing(self,map:MapType,dt:float,input:Input,game:"Game"):
        pass

    