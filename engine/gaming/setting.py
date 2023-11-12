import abc
from engine.const import *

class Setting:

    @abc.abstractmethod
    def bind_game(self):
        "绑定游戏实例"