from const import *
from ..setting import Setting

def __import():
    global Game
    from game import Game

class Settings(Setting):


    def __init__(self, **kwargs) -> None:
        self.context = kwargs['context']
        kwargs = kwargs['context']['video']
        self.anti_aliasing: Sequence[str | None] = kwargs["anti_aliasing"]
        self._fovy: Sequence[str | None] = kwargs["fovy"]

        self.load()
        pass

    def load(self):
        anti_aliasing: list[str] | list[None] = self.anti_aliasing[0].split(' ') if self.anti_aliasing[0] != None else [None]
        match anti_aliasing[0]:
            case "MSAA":
                # MSAA抗锯齿，第二个选项是采样倍率
                game.display.gl_set_attribute(GL_MULTISAMPLEBUFFERS, int(anti_aliasing[1]))
            case "FXAA":
                ...
            case None:
                ...
            
    def bind_game(self, game: 'Game'):
        self.game = game

    @property
    def fovy(self):
        return self._fovy

    @fovy.setter
    def fovy(self, value):
        self._fovy = value
        self.game.FOVY = value
        self.context['fovy'] = value