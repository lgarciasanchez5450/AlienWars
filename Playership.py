import ChunkManager
import pygame

class Playership(ChunkManager.Spaceship):
    def __init__(self, pos, rot, hp):
        super().__init__(pos, rot, hp)
        self._surf = pygame.Surface((20,20))
        self._surf.fill("blue")

    def update(self,map:ChunkManager, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.pos -= 500 * dt
        if keys[pygame.K_s]:
            self.pos += 500 * dt
        if keys[pygame.K_a]:
            self.pos -= 500 * dt
        if keys[pygame.K_d]:
            self.pos += 500 * dt
        pass

    def get_surf(self):
        return pygame.transform.rotate(self._surf,self.rot)
