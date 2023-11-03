from .._event import Event as parent
from ._const import *

class Event(parent):

    def __init__(self, rotation) -> None:
        rotation = rotation
        self.rotation_last = rotation
        self.rotation = rotation
        pass

    def trigger(self, **kwargs):
        self.rotation_last = self.rotation
        self.rotation = kwargs["rotation"]
        # 视角变化
        if not (self.rotation_last == self.rotation).all():
            self.turn_the_perspective(**kwargs)
        ...

    def turn_the_perspective(self, **kwargs):
        "转动视角事件"
        # 转动角度
        deg = 1
        rotation = list(reversed(const._UNIT(self.rotation)))
        glRotatef(deg, *rotation, 0)
        