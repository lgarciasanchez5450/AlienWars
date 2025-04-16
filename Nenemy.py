from Attacks import *
from pygame import Surface
from pygame import Mask
from pygame import transform
import ResourceManager
import random
import physics
from Entities.Spaceship import Spaceship
# global_entity_physics_cache:list[tuple[Surface,int],tuple[Surface,Mask]] = {}


def deltaAngle(a:float,b:float):
    d_rot = (a - b) %TWO_PI
    if d_rot > pi:
        d_rot -= TWO_PI
    return d_rot

# class Goal:
#     WANDER = 0
#     RETREAT = 1
#     PROTECT = 2
#     ATTACK = 3
#     M_SPAWN = 4
#     M_TURTLE = 5
#     M_PANIC = 6
#     def __init__(self,entity:'SpaceshipAI'):
#         self.entity = entity
#     def update(self,map,game): ...
#     def reload(self,map,game:GameType): ...

# class MotherShipSpawnGoal(Goal):
#     def __init__(self, entity:"Mothership"):
#         super().__init__(entity)
#         self.entity:Mothership

#     def reload(self, map, game):
#         pass

#     def update(self, map, game:GameType):
#         if self.entity.t_next_spawn < game.time:
#             if len(self.entity.spawns) < self.entity.spawn_cap:
#                 self.entity.spawnShip(game)
#             else:
#                 for i in range(len(self.entity.spawns)):
#                     if self.entity.spawns[i].dead:
#                         self.entity.spawns.pop(i)
#                         self.entity.spawnShip(game)
#                         break

#             self.entity.t_next_spawn = game.time + self.entity.spawn_speed

# class MotherShipPanicGoal(Goal):
#     def __init__(self, entity:"Mothership"):
#         super().__init__(entity)
#         self.entity:Mothership

#     def reload(self, map, game):
#         for sub in self.entity.spawns:
#             sub.defendShip(self.entity,200,map,game)

# class ProtectGoal(Goal):
#     class STATE:
#         OUTSIDE = 0
#         NEAR = 1

#     def __init__(self, entity,protectee:'SpaceshipAI',p_radius:float):
#         super().__init__(entity)
#         self.protectee = protectee
#         self.p_rad = p_radius
#         self.state = ProtectGoal.STATE.OUTSIDE
#         self.other_protectors:list['SpaceshipAI'] = []

#     def reload(self, map, game:GameType):
#         self.update(map,game)
#         pass
    
#     def update(self, map, game:GameType):
#         ent = self.entity
#         if self.state == ProtectGoal.STATE.OUTSIDE:
#             dif = self.protectee.pos - ent.pos
#             sqrDst =  glm.length2(dif) #type: ignore
#             if sqrDst < self.p_rad: 
#                 self.state = ProtectGoal.STATE.NEAR
#                 big_rect = pygame.Rect(0,0,300,300)
#                 big_rect.center = ent.pos
#                 for other in physics.get_colliding(big_rect,map):
#                     if other is self.protectee: continue
#                     if isinstance(other,SpaceshipAI):
#                         o_goal = other._goal
#                         if type(o_goal) is ProtectGoal:
#                             if o_goal.protectee is self.protectee:
#                                 self.other_protectors.append(other)
#             target_rot = glm.atan(-dif.y,dif.x)
#             d_rot = deltaAngle(target_rot,ent.rot)
#             if abs(d_rot) > 0.05:
#                 ent.rot += d_rot * game.dt
#                 ent.dirty = True
#             ent.moveRel(glm.vec2(1,0)*500)
#         elif self.state == ProtectGoal.STATE.NEAR:
#             force = glm.vec2()
#             e_pos = ent.pos
#             for other_protector in self.other_protectors:
#                 force += 0.5 * (e_pos - other_protector.pos)

#             pass

# class Wander(Goal):
#     def __init__(self, entity):
#         super().__init__(entity)
#         self.target = None

#     def reload(self,map,game:GameType):
#         if self.target: return 
#         big_rect = pygame.Rect(0,0,300,300)
#         big_rect.center = self.entity.pos
#         self.around = [e for e in physics.get_colliding(big_rect,map) if e is not self.entity]
#         self.target = glm.vec2(
#             random.random()*MAP.w,
#             random.random()*MAP.h
#         )
#         if (dst2:=glm.distance2(self.target,self.entity.pos)) > 100*100:
#             #move target_closer 
#             dst2 -= 100*100
#             self.target -= (self.target- self.entity.pos) *0.1
            
#     def update(self,map,game:GameType):
#         assert self.target
#         dif = self.target - self.entity.pos
#         target_rot = glm.atan(-dif.y,dif.x)
#         d_rot = (target_rot - self.entity.rot) %TWO_PI
#         if d_rot > pi:
#             d_rot -= TWO_PI
#         if abs(d_rot) > 0.1:
#             self.entity.rot += d_rot * game.dt
#             self.entity.dirty = True
        
#         m = glm.dot(glm.normalize(dif),glm.vec2(glm.cos(self.entity.rot),-glm.sin(self.entity.rot)))
#         m = max(0,m)*400
#         dist_to_target = glm.distance2(self.target,self.entity.pos)
#         self.entity.moveRel(glm.vec2(1,0)*m)
        

# class AttackGoal(Goal):
#     def __init__(self, entity,target:'Spaceship'):
#         super().__init__(entity)
#         self.target = target

#     def reload(self,map,game:GameType):
#         big_rect = pygame.Rect(0,0,75,75)
#         big_rect.center = self.entity.pos
#         self.around = [e for e in physics.get_colliding(big_rect,map) if e is not self.entity and isinstance(e,SpaceshipAI)]
        
#     def update(self, map, game:GameType):
#         ent = self.entity
#         dpos = self.target.pos - ent.pos
#         trot = glm.atan(-dpos.y,dpos.x)
#         d_rot = (trot - self.entity.rot) % TWO_PI
#         if d_rot > pi:
#             d_rot -= TWO_PI
#         if abs(d_rot) > 0.05:
#             ent.rot += max(-1,min(d_rot,1)) * game.dt * 2
#             ent.dirty = True
#         if ent.atk_1.next_atk_time < game.time:
#             pos = glm.vec2(ent.pos)+28*glm.vec2(glm.cos(-ent.rot),glm.sin(-ent.rot))
#             game.spawnEntities(ent.atk_1.getBullets(pos,ent.vel*2,ent.rot))
#             ent.atk_1.resetAttackTime(game.time)
#         for s in self.around:
#             dif = ent.pos - s.pos
#             d = glm.length(dif)
#             d /= 50    
#             if d < 1:
#                 m = (d-1)*(d-1) * 1000
#                 ent.vel += dif * m * game.dt

#         ent.moveRel(glm.vec2(1,0)*(glm.length(dpos)-200)*10) 

# class RetreatGoal(Goal):
#     def __init__(self, entity):
#         super().__init__(entity)

#     def reload(self, map, game):
#         big_rect = pygame.Rect(0,0,300,300)
#         big_rect.center = self.entity.pos
#         self.flee_from:list[Spaceship] = []
#         for e in physics.get_colliding(big_rect,map):
#             if isinstance(e,Spaceship) and e.alliance != self.entity.alliance:
#                 self.flee_from.append(e)

#     def update(self, map, game):
#         ent = self.entity
#         sum_pos = glm.vec2()
#         for ent in self.flee_from:
#             sum_pos += ent.pos
#         sum_pos /= len(self.flee_from)

#         dpos = sum_pos - ent.pos
#         trot = glm.atan(-dpos.y,-dpos.x)
#         d_rot = (trot - self.entity.rot) % TWO_PI
#         if d_rot > pi:
#             d_rot -= TWO_PI
#         if abs(d_rot) > 0.05:
#             ent.rot += max(-1,min(d_rot,1)) * game.dt * 2
#             ent.dirty = True

# class SpaceshipAI(Spaceship):
#     type = 'Nenemy'
#     team = 'B'
#     every = 60
#     _uid = 0
#     __slots__ = 'id','_goal','goal','force'
#     def __init__(self, pos, vel, rot, _surf, hp, aliance,controller):
#         super().__init__(pos, vel, rot, _surf, hp, aliance,controller)
#         # ResourceManager.load('./Images/TeamB/0.png',lambda x: transform.scale_by(x,1.75),Surface.convert_alpha)
#         # img = img or ResourceManager.load('./Images/TeamB/0.png',lambda x: transform.scale_by(x,1.75),Surface.convert_alpha)
#         self.id = SpaceshipAI._uid
#         self._goal = None
#         self.goal = Goal.WANDER
#         SpaceshipAI._uid += 1
#         self.force = glm.vec2()

#     def defendShip(self,ship:Spaceship,p_rad:float,map:MapType,game:GameType):
#         assert ship.alliance is self.alliance
#         self._goal = ProtectGoal(self,ship,p_rad)
#         self.goal = Goal.PROTECT
#         self._goal.reload(map,game)


#     def update(self, map, dt, game:GameType):
#         if game.frame % SpaceshipAI.every == self.id % SpaceshipAI.every:
#             self.higher_order_processing(map,dt,game)
#         elif self._goal:
#             self._goal.update(map,game)
#         self.vel += glm.rotate(self.force,-self.rot) * dt
#         self.force = glm.vec2()
#         super().update(map,dt,game)
#         self.vel = expDecay(self.vel,glm.vec2(),4,dt)

#     def moveRel(self,force:glm.vec2):
#         self.force += force

#     def higher_order_processing(self,map:MapType,dt:float,game:GameType):
#         if self._goal is None: 
#             self.goal = Goal.WANDER
#             self._goal = Wander(self)
#         if self.goal is Goal.PROTECT:
#             pass
#         if self.hp/self.hp_max < 0.2 and self.goal != Goal.RETREAT:
#             self.goal = Goal.RETREAT
#             self._goal = RetreatGoal(self)
#         elif self.goal is Goal.WANDER:
#             big_rect = pygame.Rect(0,0,500,500)
#             big_rect.center = self.pos
#             for ent in physics.get_colliding(big_rect,map):
#                 if ent is self: continue
#                 if isinstance(ent,Spaceship):
#                     if ent.alliance is not self.alliance:
#                         self.goal = Goal.ATTACK
#                         self._goal = AttackGoal(self,ent)
#         elif self.goal is Goal.ATTACK:
#             assert isinstance(self._goal,AttackGoal)
#             if glm.distance2(self._goal.target.pos,self.pos) > 1000*1000:
#                 self.goal = Goal.WANDER
#                 self._goal = Wander(self)
#             elif self._goal.target.dead:
#                 self.goal = Goal.WANDER
#                 self._goal = Wander(self)
#         else:
#             if 5 > 6:
#                 self._goal = ProtectGoal() #type: ignore
#         self._goal.reload(map,game)

#     def regenerate_physics(self):
#         rot_hash = (int(self.rot * RAD_TO_DEG) % 360)
#         key = (self._surf,rot_hash)
#         if key not in global_entity_physics_cache:
#             surf = pygame.transform.rotate(self._surf,self.rot*RAD_TO_DEG)
#             mask = pygame.mask.from_surface(surf)
#             if len(global_entity_physics_cache) < 1000:
#                 global_entity_physics_cache[key] = surf,mask
#         else:
#             surf,mask = global_entity_physics_cache[key]
#         self.surf = surf
#         self.mask = mask
#         self.rect = self.surf.get_rect()
#         self.rect.center = self.pos

# class Mothership(SpaceshipAI):
#     type = 'Mothership'
#     def __init__(self, pos, rot):
#         mother = ResourceManager.load('./Images/TeamB/1.png',Surface.convert,lambda x: transform.scale_by(x,0.8))
#         mother.set_colorkey('white')
#         super().__init__(glm.vec2(pos), rot,100,mother)
#         self.spawn_speed = 10
#         self.t_next_spawn = 0
#         self.spawn_cap = 75
#         self.spawns:list[SpaceshipAI] = []
#         self.start_spawn_count = 10

#     def spawnShip(self,game:GameType):
#         new_ship = enemyFactory('basic',glm.circularRand(300)+self.pos,self.rot)
#         self.spawns.append(new_ship)
#         game.spawnEntity(new_ship)

#     def higher_order_processing(self, map, dt, game:GameType):
#         if self.hp/self.hp_max <= 0.5 and self.goal is not Goal.M_PANIC:
#             self.goal = Goal.M_PANIC
#             self._goal = MotherShipPanicGoal(self)
#             print('mothership panicking')
#         if self._goal is None:
#             self.goal = Goal.M_SPAWN
#             self._goal = MotherShipSpawnGoal(self)
#         self._goal.reload(map,game)
    
#     def update(self, map, dt, game:GameType):
#         while self.start_spawn_count:
#             self.spawnShip(game)
#             self.start_spawn_count -=1
#         return super().update(map, dt, game)

#     def onCollide(self, other):
#         pass


type enemytype = typing.Literal['basic','mothership']

def enemyFactory(type:enemytype,pos:glm.vec2,rot:float):
    from Controllers.Controller import Controller
    if type == 'basic':
        emy = Spaceship(pos,glm.vec2(),rot,10,NULL_SURF,0,3,'baddies',Controller())
        emy.atk_1 = BasicEnemyAttack()
        return emy
    elif type== 'mothership':
        # emy = Mothership(pos,rot)
        # return emy 
        raise NotImplementedError