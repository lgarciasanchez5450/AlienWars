from ChunkManager import *
from Attacks import *
import random
enemy_img = pygame.transform.scale_by(pygame.image.load('./Images/TeamB/0.png'), 1.75)
import physics

def expDecay(a,b,decay:float,dt:float):
  return b+(a-b)*math.exp(-decay*dt)

def deltaAngle(a:float,b:float):
    d_rot = (a - b) %TWO_PI
    if d_rot > pi:
        d_rot -= TWO_PI
    return d_rot
def dprint(*args):
    import sys
    sys.stdout.write(' '.join([str(a) for a in args])+'\n')
    sys.stdout.flush()
class Goal:
    WANDER = 0
    RETREAT = 1
    PROTECT = 2
    ATTACK = 3
    M_SPAWN = 4
    M_TURTLE = 5
    M_PANIC = 6
    def __init__(self,entity:'Nenemy'):
        self.entity = entity
    def update(self,map,game): ...
    def reload(self,map,game:"Game"): ...

class MotherShipSpawnGoal(Goal):
    def __init__(self, entity:"Mothership"):
        super().__init__(entity)
        self.entity:Mothership

    def reload(self, map, game):
        pass

    def update(self, map, game:"Game"):
        if self.entity.t_next_spawn < game.time:
            if len(self.entity.spawns) < self.entity.spawn_cap:
                self.entity.spawnShip(game)
            else:
                for i in range(len(self.entity.spawns)):
                    if self.entity.spawns[i].dead:
                        self.entity.spawns.pop(i)
                        self.entity.spawnShip(game)
                        break

            self.entity.t_next_spawn = game.time + self.entity.spawn_speed

class MotherShipPanicGoal(Goal):
    def __init__(self, entity:"Mothership"):
        super().__init__(entity)
        self.entity:Mothership

    def reload(self, map, game):
        for sub in self.entity.spawns:
            sub.defendShip(self.entity,200,map,game)

class ProtectGoal(Goal):
    class STATE:
        OUTSIDE = 0
        NEAR = 1
        
    def __init__(self, entity,protectee:Spaceship,p_radius:float):
        super().__init__(entity)
        self.protectee = protectee
        self.p_rad = p_radius
        self.state = ProtectGoal.STATE.OUTSIDE
        self.other_protectors:list[Nenemy] = []

    def reload(self, map, game:"Game"):
        self.update(map,game)
        pass
    
    def update(self, map, game:"Game"):
        ent = self.entity
        if self.state == ProtectGoal.STATE.OUTSIDE:
            dif = self.protectee.pos - ent.pos
            sqrDst =  glm.length2(dif)
            if sqrDst < self.p_rad: 
                self.state = ProtectGoal.STATE.NEAR
                big_rect = pygame.Rect(0,0,300,300)
                big_rect.center = ent.pos
                for other in physics.get_colliding(big_rect,map):
                    if other is self.protectee: continue
                    if isinstance(other,Nenemy):
                        o_goal = other._goal
                        if type(o_goal) is ProtectGoal:
                            if o_goal.protectee is self.protectee:
                                self.other_protectors.append(other)
            target_rot = glm.atan(-dif.y,dif.x)
            d_rot = deltaAngle(target_rot,ent.rot)
            if abs(d_rot) > 0.05:
                ent.rot += d_rot * game.dt
                ent.dirty = True
            ent.moveRel(glm.vec2(1,0)*500)
        elif self.state == ProtectGoal.STATE.NEAR:
            force = glm.vec2()
            e_pos = ent.pos
            for other_protector in self.other_protectors:
                force += 0.5 * (e_pos - other_protector.pos)

            pass
class Wander(Goal):
    def __init__(self, entity):
        super().__init__(entity)
        self.target = None
    def reload(self,map,game:"Game"):
        if self.target: return 
        big_rect = pygame.Rect(0,0,300,300)
        big_rect.center = self.entity.pos
        self.around = [e for e in physics.get_colliding(big_rect,map) if e is not self.entity]
        self.target = glm.vec2(
            random.random()*MAP.w,
            random.random()*MAP.h
        )
        if (dst2:=glm.distance2(self.target,self.entity.pos)) > 100*100:
            # print(glm.distance(self.target,self.entity.pos),end=' ')
            # print(dst2, math.sqrt(dst2-100*100))
            #move target_closer 
            dst2 -= 100*100
            self.target -= (self.target- self.entity.pos) *0.1
            # print(glm.distance(self.target,self.entity.pos))
            
    def update(self,map,game:"Game"):
        assert self.target
        dif = self.target - self.entity.pos
        target_rot = glm.atan(-dif.y,dif.x)
        d_rot = (target_rot - self.entity.rot) %TWO_PI
        if d_rot > pi:
            d_rot -= TWO_PI
        if abs(d_rot) > 0.1:
            self.entity.rot += d_rot * game.dt
            self.entity.dirty = True
        
        m = glm.dot(glm.normalize(dif),glm.vec2(glm.cos(self.entity.rot),-glm.sin(self.entity.rot)))
        m = max(0,m)*400
        dist_to_target = glm.distance2(self.target,self.entity.pos)
        self.entity.moveRel(glm.vec2(1,0)*m)
        

class AttackGoal(Goal):
    def __init__(self, entity,target:Spaceship):
        super().__init__(entity)
        self.target = target

    def reload(self,map,game:"Game"):
        big_rect = pygame.Rect(0,0,75,75)
        big_rect.center = self.entity.pos
        self.around = [e for e in physics.get_colliding(big_rect,map) if e is not self.entity and isinstance(e,Nenemy)]
        
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
            pos = glm.vec2(ent.pos)+28*glm.vec2(glm.cos(-ent.rot),glm.sin(-ent.rot))
            game.spawnEntities(ent.atk_1.getBullets(pos,ent.vel*2,ent.rot))
            ent.atk_1.resetAttackTime(game.time)
        for s in self.around:
            dif = ent.pos - s.pos
            d = glm.length(dif)
            d /= 50    
            if d < 1:
                m = (d-1)*(d-1) * 1000
                ent.vel += dif * m * game.dt

        ent.moveRel(glm.vec2(1,0)*(glm.length(dpos)-200)*10) 

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
    def __init__(self, pos, rot,hp = 3,img=None):
        img = img or enemy_img.convert_alpha()
        super().__init__(pos, rot,hp,img)
        self.every = 1
        self.id = Nenemy._uid
        self._goal = None
        self.goal = Goal.WANDER
        Nenemy._uid += 1
        self.force = glm.vec2()

    def defendShip(self,ship:Spaceship,p_rad:float,map:MapType,game:"Game"):
        assert ship.team is self.team
        self._goal = ProtectGoal(self,ship,p_rad)
        self.goal = Goal.PROTECT
        self._goal.reload(map,game)


    def update(self, map, dt, game:"Game"):
        if game.frame % Nenemy.every == self.id % Nenemy.every:
            self.higher_order_processing(map,dt,game)
        elif self._goal:
            self._goal.update(map,game)
        self.vel += glm.rotate(self.force,-self.rot) * dt
        self.force = glm.vec2()
        self.pos += self.vel * dt
        super().update(map,dt,game)
        self.vel = expDecay(self.vel,glm.vec2(),4,dt)

    def moveRel(self,force:glm.vec2):
        self.force += force

    def higher_order_processing(self,map:MapType,dt:float,game:"Game"):
        if self._goal is None: 
            self.goal = Goal.WANDER
            self._goal = Wander(self)
            # dprint('Goal Changed to Wander')
        if self.goal is Goal.PROTECT:
            pass
        if self.hp/self.hp_max < 0.2 and self.goal != Goal.RETREAT:
            self.goal = Goal.RETREAT
            self._goal = RetreatGoal(self)
            # dprint('changin to retreat goal')
        elif self.goal is Goal.WANDER:
            big_rect = pygame.Rect(0,0,500,500)
            big_rect.center = self.pos
            for ent in physics.get_colliding(big_rect,map):
                if ent is self: continue
                if isinstance(ent,Spaceship):
                    if ent.team is not self.team:
                        # dprint('Goal Changed to Attack')
                        self.goal = Goal.ATTACK
                        self._goal = AttackGoal(self,ent)
        elif self.goal is Goal.ATTACK:
            assert isinstance(self._goal,AttackGoal)
            if glm.distance2(self._goal.target.pos,self.pos) > 1000*1000:
                self.goal = Goal.WANDER
                self._goal = Wander(self)
            elif self._goal.target.dead:
                self.goal = Goal.WANDER
                self._goal = Wander(self)
        else:
            if 5 > 6:
                self._goal = ProtectGoal() #type: ignore
        self._goal.reload(map,game)

class Mothership(Nenemy):
    def __init__(self, pos, rot):
        super().__init__(glm.vec2(pos), rot,100,pygame.image.load('Images/TeamB/1.png'))
        self.spawn_speed = 10
        self.t_next_spawn = 0
        self.spawn_cap = 75
        self.spawns:list[Nenemy] = []

    def spawnShip(self,game:"Game"):
        new_ship = enemyFactory('basic',glm.circularRand(300)+self.pos,self.rot)
        self.spawns.append(new_ship)
        game.entities.append(new_ship)
        if type(self._goal) is not MotherShipSpawnGoal:
            print(self._goal)

    def higher_order_processing(self, map, dt, game:"Game"):
        if self.hp/self.hp_max <= 0.5 and self.goal is not Goal.M_PANIC:
            self.goal = Goal.M_PANIC
            self._goal = MotherShipPanicGoal(self)
            print('mothership panicking')
        if self._goal is None:
            self.goal = Goal.M_SPAWN
            self._goal = MotherShipSpawnGoal(self)
        self._goal.reload(map,game)
    
    def update(self, map, dt, game:"Game"):
        return super().update(map, dt, game)

    def onCollide(self, other):
        super().onCollide(other)
        print(self.hp)
type enemytype = typing.Literal['basic','mothership']

def enemyFactory(type:enemytype,pos:glm.vec2,rot):
    if type == 'basic':
        emy = Nenemy(pos,rot)
        emy.atk_1 = BasicEnemyAttack()
        return emy
    elif type== 'mothership':
        emy = Mothership(pos,rot)
        return emy