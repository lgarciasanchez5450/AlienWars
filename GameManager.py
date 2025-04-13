import typing
from ChunkManager import *
from Nenemy import enemyFactory
if typing.TYPE_CHECKING:
    from game import Game
from Asteroid import Asteroid, ChickenJockey
import random
from Attacks import *
import time

asteroid_img = pygame.image.load('./Images/Hazards/asteroid.png')
chicken_jockey_img = pygame.image.load('./Images/ChickenJockey/chicken_jockey.png')
pygame.font.init()
main_font = pygame.font.Font('./font/Pixeltype.ttf', 50)

class GameManager:
    def __init__(self,game:"Game",window:pygame.Window):
        self.game = game
        self.window = window
        self.asteroid_time_counter = 2
        self.screen = self.window.get_surface()

        global chicken_jockey_img
        chicken_jockey_img =chicken_jockey_img.convert()
        chicken_jockey_img.set_colorkey((255,255,255))

        self.arrow = pygame.image.load('./Images/arrow.png').convert()
        self.arrow.set_colorkey((0,0,0))

        self.level_up_sfx = pygame.Sound('./music/sfx/lvl_up.mp3')
        self.level_up_sfx.set_volume(pygame.mixer_music.get_volume())

        self.kill_count_intervals = [0,20,40,70,100,200,400,600,800,1000,1400,99999999999999999]
        self.player_lvl = 1

        self.mothership = None
        self.just_spawned = False
    
    def start_game(self):
        #spawn a bunch of random enemies 
        import random
        for i in range(200):
            rx = random.randint(0,MAP.w)
            ry = random.randint(0,MAP.h)
            self.game.spawnEntity(enemyFactory('basic',glm.vec2(rx,ry),random.random()*2*pi))

    def pre_update(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_c]:
            self.game.spawnEntity(ChickenJockey(self.game.player.pos+glm.circularRand(200), 1, chicken_jockey_img))
            chicken_jockey_sound = pygame.mixer.Sound('./music/sfx/chicken_jockey_sound.mp3')
            chicken_jockey_sound.set_volume(pygame.mixer_music.get_volume())
            chicken_jockey_sound.play()

        self.asteroid_time_counter -= self.game.dt
        if self.asteroid_time_counter <= 0:
            self.game.spawnEntity(Asteroid(self.game.player.pos+glm.circularRand(300), 1, asteroid_img.convert_alpha()))
            self.asteroid_time_counter = 5

        if self.game.kill_count >= self.kill_count_intervals[self.player_lvl]:
            self.player_lvl += 1
            if self.player_lvl == 2:
                self.spawnMothership()
                self.game.player.atk_1 = Level2Attack()
                self.game.player.hp = self.game.player.hp_max
                self.level_up_sfx.play()


            if self.player_lvl == 3:
                self.spawnMothership()
                self.game.player.atk_1 = Level3Attack()
                self.game.player.hp = self.game.player.hp_max
                self.level_up_sfx.play()


            if self.player_lvl == 4:
                self.spawnMothership()
                self.game.player.atk_1 = Level4Attack()
                self.game.player.hp = self.game.player.hp_max
                self.level_up_sfx.play()

            
            if self.player_lvl == 5:
                self.spawnMothership()
                

    def spawnMothership(self):
        self.mothership = enemyFactory('mothership',glm.vec2(MAP.centerx,MAP.top+500),0)
        self.game.spawnEntity(self.mothership)
        self.just_spawned = True
        mothership_sound = pygame.mixer.Sound('./music/sfx/boss_spawn.mp3')
        mothership_sound.set_volume(pygame.mixer_music.get_volume())
        mothership_sound.play()


    def post_update(self,map:MapType):
        if self.mothership is not None and self.mothership.dead:
            self.mothership = enemyFactory('mothership',glm.vec2(MAP.centerx, random.random() * MAP.width),0)
            self.game.spawnEntity(self.mothership)

    def ui_draw(self):
        """ I need help fixing the progress bar, sorry """
        # Create progress bar
        progress_bar = pygame.Rect((0, 0, 800, 30))
        progress_bar.center = (1280 // 2, 650)
        pygame.draw.rect(self.screen, 'gray', progress_bar)
        # Max width of the progress bar
        MAX_FILL = 785  

        # scale width based on kill count (value of 10 kills is full width)
        offset = self.kill_count_intervals[self.player_lvl-1]
        current_width = min(((self.game.kill_count-offset) / (self.kill_count_intervals[self.player_lvl]-offset)) * MAX_FILL, MAX_FILL)
        

        # Create the filled progress bar
        bar_fill = progress_bar.inflate(-10,-6)
        bar_fill.width = current_width
        
        # progress_bar_fill = pygame.Rect(progress_bar.left + 10, progress_bar.top + 6, current_width, 28)
        pygame.draw.rect(self.screen, 'darkgreen', bar_fill)

        #draw arrow
        if self.mothership and not self.mothership.dead:
            dir = self.mothership.pos - self.game.player.pos
            if glm.length(dir) > 700: 
                arrow = pygame.transform.rotate(self.arrow,pygame.Vector2(dir).angle_to((1,0)))
                pos = glm.vec2(self.screen.get_size())//2 + glm.normalize(dir)*500
                if pos.x < 0:
                    pos.x = 0
                elif pos.x >= self.screen.get_width():
                    pos.x = self.screen.get_width()
                if pos.y < 0:
                    pos.y = 0
                elif pos.y >= self.screen.get_height():
                    pos.y = self.screen.get_height()
                self.screen.blit(arrow,(pos.x-arrow.get_width()//2,pos.y-arrow.get_height()//2))
        
        hp_surf = main_font.render('HP: ' + str(self.game.player.hp), False, 'White')
        hp_rect = hp_surf.get_rect(topleft = (15, 15))
        self.screen.blit(hp_surf, hp_rect)

        level_surf = main_font.render('LEVEL: ' + str(self.player_lvl), False, 'White')
        level_rect = level_surf.get_rect(topleft = (self.screen.width - 135, 15))
        self.screen.blit(level_surf, level_rect)

        if self.just_spawned:
            spawned_surf = main_font.render('The Mothership has arrived!', False, 'White')
            spawned_rect = spawned_surf.get_rect(center = (self.screen.width // 2, self.screen.height - 120))
            self.screen.blit(spawned_surf, spawned_rect)
            
            def spawn_text_timer():
                starttime = time.perf_counter()

                while time.perf_counter() < starttime + 5:
                    self.screen.blit(spawned_surf, spawned_rect)
                    yield

            self.game.asyncCtx.addCoroutine(spawn_text_timer())
            self.just_spawned = False
