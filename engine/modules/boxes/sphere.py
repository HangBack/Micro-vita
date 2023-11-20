from ..box import Box
from engine.const import *

class Sphere(Box):

    def __init__(self, radius: float | int, position: Sequence[float | int]) -> None:
        self.radius = radius
        self.position = np.array(position, dtype=np.float32)

    def is_collided(self, other: Box):
        from engine.modules import boxes
        if isinstance(other, boxes.Sphere):
            return ((self.position - other.position) ** 2).sum() > (self.radius + other.radius) ** 2
        elif isinstance(other, boxes.Cube):
            p1 = self.position - other.size / 2
            p2 = self.position 
            return [
                
            ].any()