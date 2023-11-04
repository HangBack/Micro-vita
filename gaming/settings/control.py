from const import *

class Settings:


    def __init__(self, **kwargs) -> None:
        self.forward = eval(f"{kwargs['forward']}")
        self.backward = eval(f"{kwargs['backward']}")
        self.move_left = eval(f"{kwargs['move_left']}")
        self.move_right = eval(f"{kwargs['move_right']}")
        pass