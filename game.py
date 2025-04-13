import sys
import time
import random
import pygame
from ChunkManager import * 
from Playership import Playership
import physics
from Nenemy import enemyFactory
from Input import Input
from background_image_generator import generate
from gui.utils.utils import useCache
from GameManager import GameManager
import gui
if not __debug__:
    import builtins
    def _(*args,**kwargs):...
    builtins.print = _

window = pygame.Window('GAME',(900,600),)
screen = window.get_surface()

FPS = 700

bg_image = pygame.image.load('./Images/T8g30s.png')
bg_image = pygame.transform.scale_by(bg_image,5).convert()



half_screen_size = glm.vec2(window.size)/2
dt = 0
clock = pygame.time.Clock()
inp = Input()
inp.screen_size = glm.vec2(window.size)
inp.camera_pos = glm.vec2()

class Game:
    def __init__(self):
        self.background = {}
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


        
    def run(self):
        scene_manager = GameManager(self,window)
        scene_manager.start_game()
        screen_rect = pygame.Rect(0,0,window.size[0]+1,window.size[1]+1)
        ent_draw_rect = pygame.Rect(0,0,window.size[0]+1+CHUNK_SIZE,window.size[1]+1+CHUNK_SIZE)
        self.kill_count = 0
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
            scene_manager.pre_update(map)
            # update all entities
            for e in self.entities:
                e.update(map, self.dt, inp,self)
            scene_manager.post_update(map)

            for e in self.entities:
                if e.dirty:
                    e.regenerate_physics()
                    e.dirty = False

            #do physics
            physics.do_physics(self.entities,map)
            for i in range(len(self.entities)-1,-1,-1):
                if self.entities[i].dead:
                    del self.entities[i]
                    self.kill_count+=1
            inp.camera_pos = self.player.pos
            screen_rect.center = inp.camera_pos
            ent_draw_rect.center = inp.camera_pos
            for cpos in physics.collide_chunks2d(screen_rect.left,screen_rect.top,screen_rect.right,screen_rect.bottom,BG_CHUNK_SIZE):
                surf = useCache(generate,cpos,self.background)
                screen.blit(surf,half_screen_size+(cpos[0]*BG_CHUNK_SIZE-inp.camera_pos.x,cpos[1]*BG_CHUNK_SIZE-inp.camera_pos.y))
            for e in physics.get_colliding(ent_draw_rect,map):
                surf = e.surf
                screen.blit(surf,e.pos-inp.camera_pos+half_screen_size-glm.vec2(surf.get_size())//2)
            scene_manager.ui_draw(map)

            if __debug__:
                if f3_mode:
                    screen.blit(dbg_font.render(f'{self.player.pos.x:.0f}/{self.player.pos.y:.0f}',True,'white'))
            t_end = time.perf_counter()
            window.flip()
            t_final = time.perf_counter()
            dt = clock.tick(FPS) 
            window.title = str(round(1000*(t_end-t_start),2))+'ms' + str(round(1000*(t_final-t_start),2)) + 'ms'
            self.dt  = dt/ 1000
            self.frame += 1


class MainMenu:
    def __init__(self):
        pygame.mixer_music.set_volume(0.5)
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
                        gui.ui.Button((0,55-25),(100,50),cs,None,self.goToSettings),
                        'Settings','white',pygame.font.SysFont('Arial',20)
                    ),
                    0.5,0.5
                ),
            alpha=200
            ),
            gui.ui.WithAlpha(
                gui.ui.positioners.Aligner(
                    gui.ui.AddText(
                        gui.ui.Button((0,2*55-25),(100,50),cs,self.quit),
                        'Quit','white',pygame.font.SysFont('Arial',20)
                    ),
                    0.5,0.5
                ),
            alpha=200
            )
        )

        self.settings_layer = gui.Layer(window.size)
        self.settings_layer.space.addObjects(
            gui.ui.Image((-50,-50),pygame.transform.scale_by(pygame.image.load('./Images/T8g30s.png'),2)),
            gui.ui.positioners.Resizer(
                a:=gui.ui.Slider((0,0),(100,20),gui.ColorLayout((255,255,255),(50,50,50)),pygame.mixer.music.set_volume).setValue(pygame.mixer_music.get_volume()),
                '20%','50%','80%','~+30'
            ),
            gui.ui.positioners.WithRespectTo(
                gui.ui.Text((0,-20),'Volume','white',pygame.font.SysFont('Arial',20)),
                a,0.5,0.5
            ),
            gui.ui.positioners.Resizer(
                gui.ui.AddText(
                    gui.ui.Button((0,-20),(1,1),cs,None,self.goToMain),
                    'Back',(255,255,255),pygame.font.SysFont('Arial',20)
                ),
                '0','0','~+60','~+60'
            )
        )
    
    def goToSettings(self):
        self.cur_layer = self.settings_layer
    def goToMain(self):
        self.cur_layer = self.layer

    def toGame(self):
        self.running = False
    
    def quit(self):
        sys.exit()

    def run(self):
        self.running = True
        self.cur_layer = self.layer
        while self.running:
            inp = gui.utils.getInput()
            if inp.quitEvent:
                sys.exit()
            self.cur_layer.update(inp)
            self.cur_layer.draw(screen)
            window.flip()
            dt = clock.tick(60) 
            self.dt  = dt / 1000


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