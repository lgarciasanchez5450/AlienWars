import sys
import time
import random
import pygame
from ChunkManager import * 
from Playership import Playership
import physics
from Nenemy import Nenemy
from Input import Input
import gui

window = pygame.Window('GAME')
screen = window.get_surface()

FPS = 70

bg_image = pygame.image.load('./Images/T8g30s.png')
bg_image = pygame.transform.scale_by(bg_image,5)



camera_pos = glm.vec2()


half_screen_size = glm.vec2(window.size)/2
dt = 0
clock = pygame.time.Clock()
inp = Input()
inp.screen_size = glm.vec2(window.size)
inp.camera_pos = glm.vec2()

class Game:
    def __init__(self):
        self.entities:list[Entity] = []
        self.clock = clock
        self.input = Input()

        self.player = Playership(
            glm.vec2(0,0),
            pi/2,
            10
        )
        self.entities.append(self.player)
        self.dt = 0
        self.frame = 0

    def run(self):
        while True:
            t_start = time.perf_counter()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN: #TODO move some of this logic to player class and 
                    if event.key == pygame.K_SPACE:
                        pass
                        # self.entities.append(Bullet(glm.vec2(player.pos)+30*glm.vec2(glm.cos(-player.rot),glm.sin(-player.rot)),player.vel,player.rot))    
                    if event.key == pygame.K_q:
                        self.entities.append(
                            Nenemy(player.pos+glm.circularRand(100),glm.linearRand(0,2*pi),player)
                        )

            map = build_map(self.entities)
            # update all entities
            for e in self.entities:
                e.update(map, self.dt, inp,self)

            for e in self.entities:
                if e.dirty:
                    e.regenerate_physics()

            #do physics
            physics.do_physics(self.entities,map)
            self.entities = list(filter(lambda x:not x.dead, self.entities))

            inp.camera_pos = self.player.pos
            screen.blit(bg_image,-inp.camera_pos+half_screen_size-glm.vec2(bg_image.get_size())//2)

            for e in self.entities:
                surf = e.surf
                # if type(e) is Bullet:
                #     print(e.pos-camera_pos+half_screen_size-glm.vec2(surf.get_size())//2,surf.get_size())
                screen.blit(surf,e.pos-inp.camera_pos+half_screen_size-glm.vec2(surf.get_size())//2)
            t_end = time.perf_counter()

            window.flip()
            dt = clock.tick(FPS) 
            window.title = str(round(1000*(t_end-t_start),2))+'ms'
            self.dt  = dt/ 1000
            self.frame += 1


class MainMenu:
    def __init__(self):
        cs = gui.ColorScheme(100,100,100)
        self.layer = gui.Layer(window.size)
        self.layer.space.addObjects(
            gui.ui.Image((-50,-50),pygame.transform.scale_by(pygame.image.load('./Images/T8g30s.png'),2)),
            gui.ui.WithAlpha(
                gui.ui.positioners.Aligner(
                    gui.ui.AddText(
                        gui.ui.Button((0,-25),(100,50),cs,None,self.toGame),
                        'Play','white',pygame.font.SysFont('Arial',20)
                    ),
                    0.5,0.5
                ),
                alpha=200
            ),
            gui.ui.WithAlpha(

            gui.ui.positioners.Aligner(
                gui.ui.AddText(
                    gui.ui.Button((0,55-25),(100,50),cs,self.quit),
                    'Quit','white',pygame.font.SysFont('Arial',20)
                ),
                0.5,0.5
            ),
            alpha=200
            )
        )

    def toGame(self):
        self.running = False
    
    def quit(self):
        sys.exit()

    def run(self):
        self.running = True
        while self.running:
            inp = gui.utils.getInput()
            if inp.quitEvent:
                sys.exit()
            self.layer.update(inp)
            self.layer.draw(screen)
            window.flip()
            dt = clock.tick(60) 
            # self.quit()
            self.dt  = dt/ 1000


if __name__=='__main__':
    pygame.init()

    m = MainMenu()
    m.run()


    g = Game()
    g.run()