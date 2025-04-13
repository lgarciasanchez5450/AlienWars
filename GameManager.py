import typing
from ChunkManager import *
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
    
    def start_game(self):
        pass
    def pre_update(self,map:MapType):

        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_c]:
            self.game.spawnEntity(ChickenJockey(self.game.player.pos+glm.circularRand(200), 1, chicken_jockey_img))
            chicken_jockey_sound = pygame.mixer.Sound('./music/sfx/chicken_jockey_sound.mp3')
            chicken_jockey_sound.play()

        self.asteroid_time_counter -= self.game.dt
        if self.asteroid_time_counter <= 0:
            self.game.spawnEntity(Asteroid(self.game.player.pos+glm.circularRand(200), 1, asteroid_img))
            self.asteroid_time_counter = 2

    def post_update(self,map:MapType):
        pass
    def ui_draw(self):
        pass