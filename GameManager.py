import typing
from ChunkManager import *
from Nenemy import enemyFactory
if typing.TYPE_CHECKING:
    from game import Game
from Asteroid import Asteroid, ChickenJockey

asteroid_img = pygame.image.load('./Images/Hazards/asteroid.png')
chicken_jockey_img = pygame.image.load('./Images/ChickenJockey/chicken_jockey.png')
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

        self.kill_count_intervals = [0,20,40,70,100,200,400,600,800,1000,1400,99999999999999999]
        self.player_lvl = 1

        self.level_up_sfx = pygame.Sound('./music/sfx/lvl_up.mp3')
        self.level_up_sfx.set_volume(pygame.mixer_music.get_volume())

        self.mothership = None
    
    def start_game(self):
        pass
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
            self.game.player.atk_1.reload_time *= 0.8
            self.level_up_sfx.play()
            self.level_up_sfx.fadeout(550)

    def spawnMothership(self):
        self.mothership = enemyFactory('mothership',glm.vec2(MAP.centerx,MAP.top+500),0)
        self.game.spawnEntity(self.mothership)


    def post_update(self,map:MapType):
        pass
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
                
            print(glm.normalize(dir)*300,(pos.x-arrow.get_width()//2,pos.y-arrow.get_height()//2))
            self.screen.blit(arrow,(pos.x-arrow.get_width()//2,pos.y-arrow.get_height()//2))


