import typing
from ChunkManager import *
if typing.TYPE_CHECKING:
    from game import Game

class GameManager:
    def __init__(self,game:"Game",window:pygame.Window):
        self.game = game
        self.window = window
    
    def start_game(self):
        pass
    def pre_update(self,map:MapType):
        pass
    def post_update(self,map:MapType):
        pass
    def ui_draw(self):
        pass