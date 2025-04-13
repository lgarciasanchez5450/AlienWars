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

window = pygame.Window('GAME',(1280,720))
screen = window.get_surface()

FPS = 70

bg_image = pygame.image.load('./Images/T8g30s.png')
bg_image= pygame.transform.scale(bg_image,window.size).convert()
# bg_image = pygame.transform.scale_by(bg_image,5).convert()



half_screen_size = glm.vec2(window.size)/2

class Game:
    def __init__(self):
        self.background = {}
        self.entities:list[Entity] = []
        self.clock = pygame.time.Clock()

        self.camera_pos = glm.vec2()
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
    
    def spawnEntities(self, entities:list[Entity]):
        self.to_spawn.extend(entities)

    def toWorldCoords(self,screen_cords:glm.vec2):
        return screen_cords + self.camera_pos - half_screen_size
    
    def start(self):
        self.scene_manager = GameManager(self,window)
        self.scene_manager.start_game()
        self.screen_rect = pygame.Rect(0,0,window.size[0]+1,window.size[1]+1)
        self.ent_draw_rect = pygame.Rect(0,0,window.size[0]+1+CHUNK_SIZE,window.size[1]+1+CHUNK_SIZE)
        self.kill_count = 0
        
            
    def run(self):

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
                    if __debug__:
                        if event.key == pygame.K_F3:
                            f3_mode = True
            
            self.scene_manager.pre_update()
            self.entities.extend(self.to_spawn)
            self.to_spawn.clear()
            map = build_map(self.entities)
            # update all entities
            for e in self.entities:
                e.update(map, self.dt, self)
            self.scene_manager.post_update(map)

            for e in self.entities:
                if e.dirty:
                    e.regenerate_physics()
                    e.dirty = False

            #do physics
            physics.do_physics(self.entities,map)
            #remove dead entities
            for i in range(len(self.entities)-1,-1,-1):
                if self.entities[i].dead:
                    if self.entities[i].count_kill:
                        self.kill_count+=1
                    del self.entities[i]    

            self.draw(map)
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

    def draw(self,map):
        self.camera_pos = self.player.pos
        self.screen_rect.center = self.camera_pos
        self.ent_draw_rect.center = self.camera_pos
        for cpos in physics.collide_chunks2d(self.screen_rect.left,self.screen_rect.top,self.screen_rect.right,self.screen_rect.bottom,BG_CHUNK_SIZE):
            surf = useCache(generate,cpos,self.background)
            screen.blit(surf,glm.floor(half_screen_size+(cpos[0]*BG_CHUNK_SIZE-self.camera_pos.x,cpos[1]*BG_CHUNK_SIZE-self.camera_pos.y)))
        for e in physics.get_colliding(self.ent_draw_rect,map):
            surf = e.surf
            screen.blit(surf,e.pos-self.camera_pos+half_screen_size-glm.vec2(surf.get_size())//2)
        self.scene_manager.ui_draw()

class MainMenu:
    def __init__(self):
        pygame.mixer_music.set_volume(0.5)
        cs = gui.ColorScheme(100,100,100)
        self.layer = gui.Layer(window.size)
        self.layer.space.addObjects(
            gui.ui.Image((-0,-0),bg_image),
            gui.ui.positioners.Aligner(
                gui.ui.Image((0,0),pygame.image.load('Images/title.png').convert_alpha()),
                0.5,0.2

            ),
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
            gui.ui.Image((0,0),bg_image),
            gui.ui.positioners.Aligner(
                gui.ui.Image((0,0),pygame.image.load('Images/title.png').convert_alpha()),
                0.5,0.2

            ),
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
        clock = pygame.time.Clock()
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
    transition_time = 1
    l = gui.Layer(window.size)
    l.space.addObjects(
        black_scren:=gui.ui.WithAlpha(
            gui.ui.ColorArea((0,0),window.size),
        ),
    )
    volume = pygame.mixer.music.get_volume()
    dt = 0
    clock = pygame.Clock()
    while transition_time > 0:
        inp = gui.utils.getInput()
        if inp.quitEvent:
            sys.exit()
        black_scren.setAlpha(255*max(1-transition_time/1,0))
        pygame.mixer.music.set_volume(gui.utils.utils.lerp(volume,0,1-transition_time/1))

        transition_time -= dt
        m.cur_layer.update(inp)
        m.cur_layer.draw(screen)
        l.draw(screen)
        window.flip()
        dt = clock.tick(60) / 1000
    
    pygame.mixer.music.unload()
    pygame.mixer.music.load('music/song 1.mp3')
    pygame.mixer_music.play()
    transition_time =1
    g = Game()
    g.start()
    while transition_time > 0:
        inp = gui.utils.getInput()
        if inp.quitEvent:
            sys.exit()
        black_scren.setAlpha(255*transition_time/1)
        pygame.mixer.music.set_volume(gui.utils.utils.lerp(volume,0,transition_time/1))
        map = build_map(g.entities)
        g.draw(map)
        transition_time -= dt
        l.draw(screen)
        window.flip()
        dt = clock.tick(60) / 1000
    g.run()
    pygame.mixer.music.set_volume(volume)