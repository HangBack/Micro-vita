import abc
from engine.const import *


def __import():
    global events, Game
    from . import events
    from game import Game


class Event(metaclass=abc.ABCMeta):

    def bind_game(self, game: 'Game'):
        self.game = game
        self.game.add_event(self)
        
    @abc.abstractmethod
    def trigger(self):
        "触发器"
        ...
        
    @abc.abstractmethod
    def init(self):
        "初始化"
        ...