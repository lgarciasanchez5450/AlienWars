import glm
class Input:
    camera_pos:glm.vec2
    screen_size:glm.vec2
    
    def toWorldCoords(self,screen_cords:glm.vec2):
        return screen_cords - self.camera_pos - self.screen_size/2
    