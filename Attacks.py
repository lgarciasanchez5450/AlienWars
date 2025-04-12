from ChunkManager import *

#Here make a bunch of sublcasses of Attack
class BasicEnemyAttack(Attack):
    reload_time = 1
    next_atk_time = 0
    bullet_power = 1
    
    def makeBullet(self,pos,bvel,rot):
        b = Bullet(pos,rot)
        b.vel += bvel
        return b
