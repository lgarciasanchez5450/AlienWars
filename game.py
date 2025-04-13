import sys
import time
import random
import pygame
from ChunkManager import * 
from Playership import Playership
import physics
from Nenemy import enemyFactory
from Input import Input

import gui
if not __debug__:
    import builtins
    def _(*args,**kwargs):...
    builtins.print = _

window = pygame.Window('GAME',(900,600))
screen = window.get_surface()

FPS = 70

bg_image = pygame.image.load('./Images/T8g30s.png')
bg_image = pygame.transform.scale_by(bg_image,5).convert()



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
        self.to_spawn = []

    def spawnEntity(self,entity:Entity):
        self.to_spawn.append(entity)

    def startScene(self):
        # enemy_mother = enemyFactory('mothership',MAP.midtop,-pi/2)
        # self.entities.append(enemy_mother)
        # for i in range(10):
        #     enemy_mother.spawnShip(self)
        pass
        
    def run(self):
        self.startScene()
        if __debug__:
            f3_mode = False
            dbg_font = pygame.font.SysFont('Arial',18)
        while True:
            t_start = time.perf_counter()
            self.time = time.perf_counter()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN: #TODO move some of this logic to player class and 
                    if event.key == pygame.K_q:
                        self.entities.append(
                            enemyFactory('basic',self.player.pos+glm.circularRand(200),glm.linearRand(0,2*pi))
                        )
                    elif event.key == pygame.K_m:
                        self.entities.append(
                            enemyFactory('mothership',self.player.pos+glm.circularRand(100),glm.linearRand(2,2*pi))
                        )
                    if __debug__:
                        if event.key == pygame.K_F3:
                            f3_mode = True
            self.entities.extend(self.to_spawn)
            self.to_spawn.clear()
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
            if __debug__:
                screen.fill('black')
            inp.camera_pos = self.player.pos
            screen.blit(bg_image,-inp.camera_pos+half_screen_size-glm.vec2(bg_image.get_size())//2)

            for e in self.entities:
                surf = e.surf
                screen.blit(surf,e.pos-inp.camera_pos+half_screen_size-glm.vec2(surf.get_size())//2)
            if __debug__:
                if f3_mode:
                    screen.blit(dbg_font.render(f'{self.player.pos.x:.0f}/{self.player.pos.y:.0f}',True,'white'))
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
    pygame.mixer.music.load('music/song 2.mp3')
    pygame.mixer_music.play()
    m = MainMenu()
    m.run()
    pygame.mixer.music.unload()
    pygame.mixer.music.load('music/song 1.mp3')
    pygame.mixer_music.play()
    g = Game()
    g.run()