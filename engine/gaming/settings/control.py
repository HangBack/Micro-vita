from engine.const import *
from engine.gaming.setting import Setting

def __import():
    global Game
    from game import Game

class Settings(Setting):


    def __init__(self, **kwargs) -> None:
        self.context = kwargs['context']
        kwargs = kwargs['context']['control']
        self.move_forward = eval(f"{kwargs['move_forward']}")
        self.move_backward = eval(f"{kwargs['move_backward']}")
        self.move_left = eval(f"{kwargs['move_left']}")
        self.move_right = eval(f"{kwargs['move_right']}")
        self.move_up = eval(f"{kwargs['move_up']}")
        self.move_down = eval(f"{kwargs['move_down']}")
        self.mapping = {
            key: eval(value) 
            for key, value in kwargs.items() 
            if isinstance(value, str)
        }
        pass

    def bind_game(self, game: 'Game'):
        self.game = game