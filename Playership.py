import ChunkManager
import pygame

class Playership(ChunkManager.Spaceship):
    def __init__(self, pos, rot, hp):
        super().__init__(pos, rot, hp)
        self._surf = pygame.Surface((20,20))
        self._surf.fill("blue")

    def update(self,map:ChunkManager):
        pass

    def get_surf(self):
        return pygame.transform.rotate(self._surf,self.rot)
