

# class StateMachineController(Controller):
#     counter = 0
#     __slots__ = 'state','next_state','uid'
#     def init(self,entity:Spaceship):
#         self.uid = StateMachineController.counter
#         StateMachineController.counter += 1

#         self.next_state = None
#         if not hasattr(self,'state'):
#             self.setState(StateWander(entity))

#     def update(self,entity:Spaceship,map:MapType,game:GameType):
#         if game.frame % 100 == self.uid % 100:
#             self.state.think(self,entity,map,game)
#         if self.next_state:
#             self.state = self.next_state
#             self.state.think(self,entity,map,game)
#             self.next_state = None
#         else:
#             self.state.update(self,entity,map,game)

#     def onCollide(self, entity: Spaceship, other: EntityType, collision_normal: Vec2):
#         if type(self.state) is not StateAttack:
#             if type(other) is Bullet:
#                 if other.shooter:
#                     return self.setState(StateAttack(entity,other.shooter))    
#             else:
#                 self.setState(StateAttack(entity,other))

#     def setState(self,state:State):
#         self.next_state = state

#     def copy(self):
#         return type(self)()
