import time
import pygame
import random
from math import pi
from Attacks import *
from gametypes import *
from EntityTags import *
from Nenemy import enemyFactory
from Entities.Asteroid import Asteroid, ChickenJockey
from Entities.Spaceship import Spaceship
from Controllers.PlayerController import PlayerController
import ResourceManager



pygame.font.init()
main_font = pygame.font.Font('./font/Pixeltype.ttf', 26)

class GameManager:
    def __init__(self,game:GameType,window:pygame.Window):
        self.game = game
        self.window = window
        self.asteroid_time_counter = 9999999999999
        self.screen = self.window.get_surface()

        pygame.init()
        self.chicken_jockey_img = ResourceManager.loadOpaque('./Images/ChickenJockey/chicken_jockey.png')
        self.chicken_jockey_img.set_colorkey((255,255,255))
        self.asteroid_img = ResourceManager.loadAlpha('./Images/Hazards/asteroid.png')
        self.enemy_ship_img = ResourceManager.loadAlpha('./Images/TeamB/0.png')

        self.atk_frame = ResourceManager.loadColorKey('./Images/attack_pics/basic_atk.png',(0,0,0))


        self.arrow = ResourceManager.loadOpaque('./Images/arrow.png')
        self.arrow.set_colorkey((0,0,0))
        self.player_img_path = './Images/TeamA/Ship/0.png'

        self.level_up_sfx = pygame.Sound('./music/sfx/lvl_up.mp3')
        self.level_up_sfx.set_volume(pygame.mixer_music.get_volume())

        self.kill_count_intervals = [0,20,40,70,100,200,400,600,800,1000,1400,99999999999999999]
        self.player_lvl = 1

        self.mothership = None
        self.just_spawned = False


    
    def start_game(self):
        #spawn player
        self.player = Spaceship(
            glm.vec2(50),
            glm.vec2(),
            pi/2,
            8,
            pygame.image.load(self.player_img_path).convert_alpha(),
            E_IS_PLAYER|E_CAN_BOUNCE,
            30,
            'A',
            [NamedGun((35,0),0,90,'Test_Name',self.atk_frame)],
            5000,
            PlayerController(),
        )

        self.game.spawnEntity(self.player)
        #spawn a bunch of random enemies 
 

        # import random
        # for i in range(500):
        #     rx = random.randint(0,MAP.w)
        #     ry = random.randint(0,MAP.h)
        #     enemy = self.game.builder.buildEnemy(
        #         glm.vec2(rx,ry),glm.vec2(),None,'B',**self.game.builder.fighter
        #     )
        #     self.game.spawnEntity(enemy)s

    def pre_update(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_c]:
            self.game.spawnEntity(ChickenJockey(self.player.pos+glm.circularRand(200),glm.circularRand(100),1, 1, self.chicken_jockey_img,E_CAN_BOUNCE))
            chicken_jockey_sound = pygame.mixer.Sound('./music/sfx/chicken_jockey_sound.mp3')
            chicken_jockey_sound.set_volume(pygame.mixer_music.get_volume())
            chicken_jockey_sound.play()
        if keys[pygame.K_1]:
            self.game.spawnEntity(
                self.game.builder.buildEnemy(self.player.pos + glm.circularRand(200),glm.vec2(),0,'B',**self.game.builder.warship)
            )
        if keys[pygame.K_2]:
            self.game.spawnEntity(
                self.game.builder.buildEnemy(self.player.pos + glm.circularRand(200),glm.vec2(),0,'B',**self.game.builder.fighter)
            )
        self.asteroid_time_counter -= self.game.dt
        if self.asteroid_time_counter <= 0:
            self.game.spawnEntity(Asteroid(self.player.pos+glm.circularRand(300),
                                           glm.circularRand(random.uniform(50, 150)),
                                           random.random()*2*pi,
                                           3,
                                           self.asteroid_img,
                                           E_CAN_BOUNCE))
            self.asteroid_time_counter = 5

        if self.game.kill_count >= self.kill_count_intervals[self.player_lvl]:
            self.player_lvl += 1
            # if self.player_lvl == 2:
            #     self.spawnMothership()
            #     self.player.atk_1 = Level2Attack()
            #     self.player.hp = self.player.hp_max
            #     self.level_up_sfx.play()
            # if self.player_lvl == 3:
            #     self.spawnMothership()
            #     self.player.atk_1 = Level3Attack()
            #     self.player.hp = self.player.hp_max
            #     self.level_up_sfx.play()


            # if self.player_lvl == 4:
            #     self.spawnMothership()
            #     self.player.atk_1 = Level4Attack()
            #     self.player.hp = self.player.hp_max
            #     self.level_up_sfx.play()

            
            # if self.player_lvl == 5:
            #     self.spawnMothership()
            #     self.player.atk_1 = EightShotPassive()
            #     self.player.hp = self.player.hp_max
            #     self.level_up_sfx.play()

    def post_update(self,map:MapType): ...

    def spawnMothership(self):
        return
        self.mothership = enemyFactory('mothership',glm.vec2(MAP.centerx, random.random() * MAP.width), 0)
        self.game.spawnEntity(self.mothership)
        self.just_spawned = True
        mothership_sound = pygame.mixer.Sound('./music/sfx/boss_spawn.mp3')
        mothership_sound.set_volume(pygame.mixer_music.get_volume())
        mothership_sound.play()


    def pre_draw(self):
        self.game.camera_pos = self.player.pos

    def ui_draw(self):
        """ I need help fixing the progress bar, sorry """
        #draw arrow
        if self.mothership and not self.mothership.dead:
            dir = self.mothership.pos - self.player.pos
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

        #draw lvl
        lvl_bar = pygame.Rect(5, 30, 200, 20)
        lvl_bar_fill = lvl_bar.inflate( -6,-6)
        offset = self.kill_count_intervals[self.player_lvl-1]
        lvl_bar_fill.w = min(((self.game.kill_count-offset) / (self.kill_count_intervals[self.player_lvl]-offset)) * lvl_bar_fill.w, lvl_bar_fill.w)

        pygame.draw.rect(self.screen, 'gray', lvl_bar)
        pygame.draw.rect(self.screen, 'darkgreen', lvl_bar_fill)

        #draw hp
        hp_bar = pygame.Rect(5, 5, 200, 20)
        hp_bar_filled = hp_bar.inflate(-6,-6)
        hp_bar_filled.w = min((self.player.hp / self.player.hp_max) * hp_bar_filled.w, hp_bar_filled.w)

        pygame.draw.rect(self.screen, 'gray', hp_bar)
        pygame.draw.rect(self.screen, 'darkred', hp_bar_filled)
        hp_surf = main_font.render(str(self.player.hp), False, 'White')
        self.screen.blit(hp_surf,hp_bar_filled)


        level_surf = main_font.render('LEVEL: ' + str(self.player_lvl), False, 'White')
        level_rect = level_surf.get_rect(topright = (self.screen.width-5 , 5))
        self.screen.blit(level_surf, level_rect)

        x,y = 30,self.screen.height - 100
        p_ctrlr = self.player.controller
        assert type(p_ctrlr) is PlayerController
        for action in [p_ctrlr.a_shoot,p_ctrlr.a_charge]:

            size = action.img.get_size()
            self.screen.fill((50,50,50),(x,y,*size))
            self.screen.blit(action.img,(x,y))    
            if not action.isAvailable(self.game.time):
                percent_left = action.percentLeft(self.game.time)
                b = y + size[1]
                t = int(b - percent_left * size[1] )
                self.screen.fill((127,127,172),(x,t,size[0],b-t),pygame.BLEND_MULT)
            x += action.img.get_width()+5