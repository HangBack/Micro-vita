from const import *

class Settings:


    def __init__(self, **kwargs) -> None:
        self.move_forward = eval(f"{kwargs['move_forward']}")
        self.move_backward = eval(f"{kwargs['move_backward']}")
        self.move_left = eval(f"{kwargs['move_left']}")
        self.move_right = eval(f"{kwargs['move_right']}")
        self.move_up = eval(f"{kwargs['move_up']}")
        self.move_down = eval(f"{kwargs['move_down']}")
        pass