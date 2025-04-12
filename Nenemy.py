from ChunkManager import *
img= pygame.image.load('./Images/nship.png')

class Nenemy(Spaceship):
    def __init__(self, pos, rot,player:Spaceship):
        super().__init__(pos, rot, 3,img)
        self.player = player
    def update(self, map, dt, camera_pos):
        dpos = self.player.pos - self.pos
        trot = glm.atan(-dpos.y,dpos.x)
        drot = trot - self.rot
        if drot:
            self.rot += max(-1,min(drot,1)) * dt * 2
            self.dirty = True