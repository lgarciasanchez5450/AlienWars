import gui
import sys
import time
import pygame
import random
import physics
from collections import defaultdict,Counter

from EntityTags import *
from ChunkManager import * 
from Builder import Builder
from Entities.Entity import Entity
from GameManager import GameManager
from Attacks import BasicEnemyAttack
from gui.utils.utils import useCache
from Entities.Spaceship import Spaceship
from background_image_generator import generate
from Controllers.PlayerController import PlayerController

def formatBytes(b:int):
    i = 0
    while b >= 1024:
        i += 1
        b >>= 10
    return f'{b} {['B','KiB','MiB','GiB'][i]}'

# WINDOW_SIZE = 1280,720
WINDOW_SIZE = 900,600
window = pygame.Window('GAME',WINDOW_SIZE)
screen = window.get_surface()

FPS = 70

type Coroutine[T] = typing.Generator[typing.Any,typing.Any,T]
from collections import deque
class AsyncContext:
    def __init__(self) -> None:
        self.coros:deque[Coroutine] = deque()

    def update(self) -> tuple[Coroutine,typing.Any]|None:
        if not self.coros: return
        coro = self.coros.popleft()
        try:
            next(coro)
        except StopIteration as e:
            return coro,e.value
        else:
            self.coros.append(coro)

    def addCoroutine(self,coro:Coroutine):
        self.coros.append(coro)

    def getNumCoros(self):
        return len(self.coros)
    

half_screen_size = glm.vec2(window.size)/2
class Game:
    def __init__(self):
        self.background = {}
        self.entities:list[Entity] = []
        self.assets = {}
        self.clock = pygame.time.Clock()
        self.builder = Builder()
        self.builder.buildEnemy(glm.vec2(),glm.vec2(),None,'A',1,**self.builder.fighter)

        self.camera_pos = glm.vec2()
        self.player = Spaceship(
            glm.vec2(MAP.centerx+random.randint(-500,500),MAP.centery+random.randint(-500,500)),
            glm.vec2(),
            pi/2,
            1,
            pygame.image.load('./Images/TeamA/Ship/0.png').convert_alpha(),
            E_IS_PLAYER|E_CAN_BOUNCE,
            30,
            'A',
            PlayerController()
        )
        
        self.player.atk_1 = BasicEnemyAttack()


        self.entities.append(self.player)
        self.player.regenerate_physics()
        self.dt = 0
        self.frame = 0
        self.to_spawn:list[Entity] = []

        self.asyncCtx = AsyncContext()

    def spawnEntity(self,entity:Entity):
        self.to_spawn.append(entity)
    
    def spawnEntities(self, entities:list[Entity]):
        self.to_spawn.extend(entities)

    def toWorldCoords(self,screen_cords:glm.vec2|tuple[int,int]):
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
            time_frame= False
        while True:
            t_start = time.perf_counter()
            self.time = time.perf_counter()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN: #TODO move some of this logic to player class and 
                    if event.mod& pygame.KMOD_CTRL:
                        if event.key == pygame.K_d:
                            self.player.hp = self.player.hp_max = 9999999
                    if __debug__:
                        if event.key == pygame.K_F3:
                            f3_mode = not f3_mode
                        if event.key == pygame.K_F4:
                            time_frame = True
                        if event.key == pygame.K_F5:
                            from pympler import asizeof
                            mem_self,mem_enities,mem_bg,mem_player,mem_async = asizeof.asizesof(self, #type: ignore
                                                                                                self.entities,
                                                                                                self.background,
                                                                                                self.player,
                                                                                                self.asyncCtx)
                            print(f'Memory Breakdown (total {formatBytes(mem_self)})')
                            print(f'\tEntities      {formatBytes(mem_enities)}')
                            print(f'\tBackground    {formatBytes(mem_bg)}')
                            print(f'\tPlayer        {formatBytes(mem_player)}')
                            print(f'\tAsync         {formatBytes(mem_async)}')
            if __debug__:
                if time_frame:
                    time_a = time.perf_counter()
            self.scene_manager.pre_update()
            if __debug__:
                if time_frame:
                    time_b = time.perf_counter() 
            self.entities.extend(self.to_spawn)
            for e in self.to_spawn:
                if e.dirty:
                    e.regenerate_physics()
                    e.dirty = False
            self.to_spawn.clear()
            if __debug__:
                if time_frame:
                    time_c = time.perf_counter()
            better_map = build_map_better(self.entities)
            if __debug__:
                if time_frame:
                    time_d = time.perf_counter()
            # update all entities
            for e in self.entities:
                e.update(better_map, self.dt, self)
            if __debug__:
                if time_frame:
                    time_e = time.perf_counter()
            self.scene_manager.post_update(better_map)
            if __debug__:
                if time_frame:
                    time_f = time.perf_counter()
            if __debug__:
                regen_physics_by_type = defaultdict(float)
                for e in self.entities:
                    if e.dirty:
                        t_rstart = time.perf_counter()
                        e.regenerate_physics()
                        e.dirty = False
                        t_rend = time.perf_counter()
                        regen_physics_by_type[type(e)] += t_rend-t_rstart
            else:
                for e in self.entities:
                    if e.dirty:
                        e.regenerate_physics()
                        e.dirty = False
            if __debug__:
                if time_frame:
                    time_g = time.perf_counter()
            #do physics
            physics.calc_collision_map(better_map)
            if __debug__:
                if time_frame:
                    time_h = time.perf_counter()
            #remove dead entities
            for i in range(len(self.entities)-1,-1,-1):
                if self.entities[i].dead:
                    self.kill_count+=1  
                    del self.entities[i]    
            if __debug__:
                if time_frame:
                    time_i = time.perf_counter()
            self.draw(better_map)
            if __debug__:
                if time_frame:
                    time_j = time.perf_counter()
            self.asyncCtx.update()
            if __debug__:
                if f3_mode:
                    screen.blit(dbg_font.render(f'{self.player.pos.x:.0f}/{self.player.pos.y:.0f}',True,'white'))
                if time_frame:
                    print(f'Frame Time Breakdown: (total {1000*(time_h-time_a):.2f} ms)') #type: ignore
                    print(f'\tPre Update        {1000*(time_b-time_a):.2f} ms') #type: ignore
                    print(f'\tSpawn             {1000*(time_c-time_b):.2f} ms') #type: ignore
                    print(f'\tBuild Map         {1000*(time_d-time_c):.2f} ms') #type: ignore
                    print(f'\tUpdate            {1000*(time_e-time_d):.2f} ms') #type: ignore
                    print(f'\tPost Update       {1000*(time_f-time_e):.2f} ms') #type: ignore
                    print(f'\tPre Physics       {1000*(time_g-time_f):.2f} ms') #type: ignore
                    print(f'\tPhysics           {1000*(time_h-time_g):.2f} ms') #type: ignore
                    print(f'\tClean Entities    {1000*(time_i-time_h):.2f} ms') #type: ignore
                    print(f'\tDraw              {1000*(time_j-time_i):.2f} ms') #type: ignore
                    print('Misc Data: ')
                    print(f'\tMost Common Physics Regeneration:\n\t{[f"{c.__name__}: {regen_physics_by_type[c]*1000:.2f} ms" for c,n in (Counter(regen_physics_by_type).most_common())]})')
                    from Entities.Entity import EntityCachedPhysics
                    print(f'\tSize of Global Entity Cache:',len(EntityCachedPhysics._global_physics_cache))
                    time_frame = False
            t_end = time.perf_counter()
            window.flip()
            t_final = time.perf_counter()
            dt = self.clock.tick(FPS) 
            window.title = str(round(1000*(t_end-t_start),2)).ljust(4)+' ms   ' + str(round(1000*(t_final-t_end),2)).ljust(4) + 'ms'
            self.dt  = dt / 1000
            self.frame += 1

    def draw(self,map):
        self.camera_pos = self.player.pos
        self.screen_rect.center = self.camera_pos
        self.ent_draw_rect.center = self.camera_pos
        i = 0
        for cpos in physics.collide_chunks2d(self.screen_rect.left,self.screen_rect.top,self.screen_rect.right,self.screen_rect.bottom,BG_CHUNK_SIZE):
            surf = useCache(generate,cpos,self.background)
            i+=1
            screen.blit(surf,glm.floor(half_screen_size+(cpos[0]*BG_CHUNK_SIZE-self.camera_pos.x,cpos[1]*BG_CHUNK_SIZE-self.camera_pos.y))) #type: ignore
        es = 0
        for e in physics.get_colliding(self.ent_draw_rect,map):
            es += 1
            surf = e.surf
            screen.blit(surf,e.pos-self.camera_pos+half_screen_size-glm.vec2(surf.get_size())//2)
        self.scene_manager.ui_draw()

class MainMenu:
    def __init__(self):
        import ResourceManager
        bg_image = ResourceManager.loadOpaque('./Images/T8g30s.png')
        bg_image = pygame.transform.scale(bg_image,window.size)
        pygame.mixer_music.set_volume(0.0)
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
    if sys.argv[-1] != '-d':
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
            black_scren.setAlpha(int(255*max(1-transition_time/1,0)))
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
        transition_time = 1
        g = Game()
        g.start()
        while transition_time > 0:
            inp = gui.utils.getInput()
            if inp.quitEvent:
                sys.exit()
            black_scren.setAlpha(int(255*transition_time/1))
            pygame.mixer.music.set_volume(gui.utils.utils.lerp(volume,0,transition_time/1))
            map = build_map(g.entities)
            g.draw(map)
            transition_time -= dt
            l.draw(screen)
            window.flip()
            dt = clock.tick(60) / 1000
        g.run()
        pygame.mixer.music.set_volume(volume)
    else:
        g = Game()
        g.start()
        g.run()