import abc
from const import *


class Event(metaclass=abc.ABCMeta):

    def __import():
        global events, Game
        from . import events
        from game import Game

    def bind_game(self, game: 'Game'):
        self.game = game

    @abc.abstractmethod
    def trigger(self, tick):
        "触发器"
        ...