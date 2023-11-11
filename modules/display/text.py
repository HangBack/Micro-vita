from const import *

class Text:

    def __init__(self) -> None:
        self.vertices = np.array([
            -0.5, -0.5, 0, 0.0, 0.0,
            -0.5, +0.5, 0, 0.0, 1.0,
            +0.5, +0.5, 0, 1.0, 1.0
            +0.5, -0.5, 0, 1.0, 0.0
        ], dtype=np.float32)
        pass