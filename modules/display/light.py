from const import *

class Light:

    def __init__(self, position: Sequence, color: game.Color = [1.0, 1.0, 1.0, 1.0], light = GL_LIGHT0, **kwargs) -> None:
        self._light = light
        self._position: Sequence = position
        self._color: game.Color = color

        self.load()

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value):
        self._position = value
        self.load()

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        self._color = value
        self.load()

    def load(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(self._light)
        glLightfv(self._light, GL_POSITION, list(self._position))
        glLightfv(self._light, GL_DIFFUSE, list(self._color))
    