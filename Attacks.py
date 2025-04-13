from ChunkManager import *

#Here make a bunch of subclasses of Attack
class BasicEnemyAttack(Attack):
    reload_time = 1
    next_atk_time = 0
    bullet_power = 1
    
    def makeBullet(self,pos,bvel,rot):
        b = Bullet(pos,rot)
        b.vel += bvel
        return b

class Level2Attack(Attack):
    reload_time = 0.4
    next_atk_time = 0
    bullet_power = 2

    def makeBullet(self, pos, bvel, rot):
        b = Bullet(pos, rot)
        b.vel += bvel
        b.dmg = self.bullet_power
        return b

class Level3Attack(Attack): ...
