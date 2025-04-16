from Controllers.Controller import Controller
from Entities.Spaceship import Spaceship

class FighterController(Controller):
    def init(self,entity:Spaceship): ...

    def update(self,entity:Spaceship): ...
    