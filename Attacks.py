from ChunkManager import *

#Here make a bunch of subclasses of Attack
class BasicEnemyAttack(Attack):
    reload_time = 1
    next_atk_time = 0
    bullet_power = 1
    
    def getBullets(self,pos,bvel,rot):
        b = Bullet(pos,rot)
        b.vel += bvel
        return [b]

class Level2Attack(Attack):
    reload_time = 0.4
    next_atk_time = 0
    bullet_power = 2

    def getBullets(self, pos, bvel, rot):
        b = Bullet(pos, rot)
        b.vel += bvel
        b.dmg = self.bullet_power
        return [b]
    
class Level3Attack(Attack):
    reload_time = 0.4
    next_atk_time = 0
    bullet_power = 2

    def getBullets(self, pos, bvel, rot):
        bullets = []
        offset = [90*pi/180, 0, -90*pi/180]
        direction_angles = [-15*pi/180, 0, 15*pi/180]
        for i in range(3):
            new_bullet = Bullet(pos + 15 * glm.vec2(glm.cos(offset[i]), glm.sin(offset[i])), rot + direction_angles[i])
            new_bullet.vel += bvel
            bullets.append(new_bullet)
        return bullets

