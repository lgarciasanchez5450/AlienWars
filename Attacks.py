from glm import vec2
from ChunkManager import *
from Entities.TimedEntity import Surface
from gametypes import *
from Entities.Bullet import Bullet


class Gun:
    def __init__(
            self,
            pos:glm.vec2|tuple[float,float],
            rot:float,
            rpm:float #rounds per minute
    ):
        self.pos = glm.vec2(pos)
        self.rot = rot
        self.fire_rate = rpm
        self.next_fire_time = 0

    def tryFire(self,curr_time:float):
        if curr_time > self.next_fire_time:
            self.next_fire_time = curr_time + 60/self.fire_rate
            return True
        return False

    def canFire(self,curr_time:float):
        return curr_time > self.next_fire_time
    
    def fire(self,curr_time:float):
        assert self.canFire(curr_time)
        self.next_fire_time = curr_time + 60/self.fire_rate
    
    def copy(self):
        return Gun(self.pos,self.rot,self.fire_rate)

# class Attack:
#     reload_time:float
#     next_atk_time:float
#     bullet_power:int
#     def resetAttackTime(self,cur_time:float):
#         self.next_atk_time = cur_time + self.reload_time
#     def getBullets(self,pos,bvel,rot) -> list[EntityType]: ...

#     def copy(self):
#         cpy = type(self)()
#         cpy.reload_time = self.reload_time
#         cpy.bullet_power = self.bullet_power
#         cpy.next_atk_time = 0
#         return cpy

# #Here make a bunch of subclasses of Attack
# class BasicEnemyAttack(Attack):
#     reload_time = 0.6
#     next_atk_time = 0
#     bullet_power = 2
    
#     def getBullets(self,pos,bvel,rot):
#         b = Bullet.makeDefault(pos,bvel,rot)
#         return [b]




# class Level2Attack(Attack):
#     reload_time = 0.2
#     next_atk_time = 0
#     bullet_power = 4

#     def getBullets(self, pos, bvel, rot):
#         b = Bullet.makeDefaultBlue(pos,bvel*1.5, rot)
#         b.dmg = self.bullet_power
#         return [b]
    
# class Level3Attack(Attack):
#     reload_time = 0.4
#     next_atk_time = 0
#     bullet_power = 4

#     def getBullets(self, pos, bvel, rot):
#         bullets = []
#         direction_angles = [-15*pi/180, 0, 15*pi/180]
#         for i in range(3):
#             new_rot = rot+ direction_angles[i]
#             p_rot = rot+direction_angles[i]*2
#             dir = glm.vec2(glm.cos(-p_rot), glm.sin(-p_rot))
#             new_bullet = Bullet.makeDefaultBlue(pos + 15 * dir,bvel,new_rot)
#             bullets.append(new_bullet)
#         return bullets

# class Level4Attack(Attack):
#     reload_time = 0.4
#     next_atk_time = 0
#     bullet_power = 6

#     def getBullets(self, pos, bvel, rot):
#         bullets = []
#         direction_angles = [-45*pi/180, -15*pi/180, 0, 15*pi/180, 45*pi/180]
#         for i in range(5):
#             new_rot = rot+direction_angles[i]
#             p_rot = rot+direction_angles[i]*2
#             dir = glm.vec2(glm.cos(-p_rot), glm.sin(-p_rot))
#             new_bullet = Bullet.makeDefaultBlue(pos + 30 * dir,bvel,new_rot)
#             # new_bullet.vel += bvel * 1.5
#             bullets.append(new_bullet)
#         return bullets

# class EightShotPassive(Attack):
#     reload_time = 0.1
#     next_atk_time = 0
#     bullet_power = 8

#     def getBullets(self, pos, bvel, rot):
#         bullets = []
#         direction_angles = [0, pi/4, pi/2, 3*pi/4, pi, 5*pi/4, 3*pi/2, 7*pi/4]
#         for i in range(8):
#             new_rot = rot+direction_angles[i]
#             p_rot = rot+direction_angles[i]
#             dir = glm.vec2(glm.cos(-p_rot), glm.sin(-p_rot))
#             new_bullet = Bullet.makeDefaultBlue(pos + 70 * dir,bvel,new_rot)
#             # new_bullet.vel += bvel
#             bullets.append(new_bullet)
#         return bullets


