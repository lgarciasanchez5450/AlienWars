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
    bullet_power = 4

    def getBullets(self, pos, bvel, rot):
        b = Bullet(pos, rot)
        b.vel += bvel
        b.dmg = self.bullet_power
        return [b]
    
class Level3Attack(Attack):
    reload_time = 0.4
    next_atk_time = 0
    bullet_power = 4

    def getBullets(self, pos, bvel, rot):
        bullets = []
        direction_angles = [-15*pi/180, 0, 15*pi/180]
        for i in range(3):
            new_rot = rot+ direction_angles[i]
            p_rot = rot+direction_angles[i]*2
            dir = glm.vec2(glm.cos(-p_rot), glm.sin(-p_rot))
            new_bullet = Bullet(pos + 15 * dir,new_rot)
            new_bullet.vel += bvel
            bullets.append(new_bullet)
        return bullets
    

class Level4Attack(Attack):
    reload_time = 0.4
    next_atk_time = 0
    bullet_power = 6

    def getBullets(self, pos, bvel, rot):
        bullets = []
        direction_angles = [-45*pi/180, -15*pi/180, 0, 15*pi/180, 45*pi/180]
        for i in range(5):
            new_rot = rot+direction_angles[i]
            p_rot = rot+direction_angles[i]*2
            dir = glm.vec2(glm.cos(-p_rot), glm.sin(-p_rot))
            new_bullet = BlueBullet(pos + 30 * dir,new_rot)
            new_bullet.vel += bvel
            bullets.append(new_bullet)
        return bullets

class EightShotPassive(Attack):
    reload_time = 0.1
    next_atk_time = 0
    bullet_power = 8

    def getBullets(self, pos, bvel, rot):
        bullets = []
        direction_angles = [0, pi/4, pi/2, 3*pi/4, pi, 5*pi/4, 3*pi/2, 7*pi/4]
        for i in range(8):
            new_rot = rot+direction_angles[i]
            p_rot = rot+direction_angles[i]
            dir = glm.vec2(glm.cos(-p_rot), glm.sin(-p_rot))
            new_bullet = BlueBullet(pos + 70 * dir,new_rot)
            new_bullet.vel += bvel
            bullets.append(new_bullet)
        return bullets


# make subclasses for different Bullets

class BlueBullet(Bullet):
    def __init__(self, pos, rot):
        super().__init__(pos, rot)
        self.dir = glm.vec2(math.cos(rot),math.sin(-rot))
        self._surf = pygame.Surface((10,5))
        self._surf.set_colorkey('black')
        self._surf.fill('aqua')
        self._surf.set_at((0,0),'black')
        self.t = 5
        self.vel = self.dir *  300
        self.rect = pygame.Rect()
