from ..box import Box
from engine.const import *


class Cube(Box):

    def __init__(self, size: Sequence[float | int], position: Sequence[float | int]) -> None:
        self.size = np.array(size, dtype=np.float32)
        self.position = np.array(position, dtype=np.float32)
        self.vertices = np.array([
            [-0.5, -0.5, -0.5], # 0
            [+0.5, -0.5, -0.5], # 1
            [+0.5, +0.5, -0.5], # 2
            [-0.5, +0.5, -0.5], # 3
            [-0.5, -0.5, +0.5], # 4
            [+0.5, -0.5, +0.5], # 5
            [+0.5, +0.5, +0.5], # 6
            [-0.5, +0.5, +0.5]  # 7
        ], dtype=np.float32) * self.size + self.position
        self.planes = np.array([
            Box.get_plane(self.vertices[0], self.vertices[1], self.vertices[3]),
            Box.get_plane(self.vertices[0], self.vertices[1], self.vertices[4]),
            Box.get_plane(self.vertices[0], self.vertices[3], self.vertices[4]),
            Box.get_plane(self.vertices[6], self.vertices[7], self.vertices[2]),
            Box.get_plane(self.vertices[6], self.vertices[7], self.vertices[5]),
            Box.get_plane(self.vertices[6], self.vertices[2], self.vertices[5])
        ], dtype=np.float32)
        """
        立方体索引
            4-------5
           /|      /|
          / |     / |
         /  7----/--6
        0--/----1  /
        | /     | /
        |/      |/
        3-------2
        
        """

    def is_collided(self, other: Box):
        from engine.modules import boxes
        if isinstance(other, boxes.Sphere):
            return ...
        elif isinstance(other, boxes.Cube):
            return ...
