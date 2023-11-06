import abc
from const import *


class Event(metaclass=abc.ABCMeta):

    def __import(self):
        global events
        from . import events

    def bind_game(self, game: 'Game'):
        self.game = game

    @abc.abstractmethod
    def trigger(self):
        "触发器，必选"
        ...
from game import Game