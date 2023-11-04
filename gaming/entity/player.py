import json
import numpy as np
from typing import Sequence

from modules import create_model
from const import *

class Player:

    class Camera:

        def __init__(self, **kwargs) -> None:
            self._look_at: Sequence = kwargs["camera"]["look_at"]
            self._position: Sequence = kwargs["camera"]["position"]
            self._up: Sequence = kwargs["camera"]["up"]
            self._pitch: float = kwargs["camera"]["pitch"]
            self._yaw: float = kwargs["camera"]["yaw"]
            self._roll: float = kwargs["camera"]["roll"]
            pass

        @property
        def yaw(self):
            return self._yaw

        @yaw.setter   
        def yaw(self, value):
            "仰俯角，达到阈值复位"
            if self._yaw > 360.0:
                self._yaw -= 360.0
            elif self._yaw < 0.0:
                self._yaw += 360.0
            else:
                self._yaw = value

        @property
        def pitch(self):
            return self._pitch

        @pitch.setter   
        def pitch(self, value):
            "y 夹在上下限"
            self._pitch = clamp_number(value, -90.0, 90.0)

        @property
        def roll(self):
            return self._roll

        @roll.setter   
        def roll(self, value):
            "z 达到阈值复位"
            if self.roll > 360.0:
                self.roll = 0.0
            elif self.roll < 0.0:
                self.roll = 360.0
            else:
                self.roll = value

        @property
        def up(self):
            return self._up

        @up.setter   
        def up(self, value):
            self._up = value

        @property
        def position(self):
            return self._position

        @position.setter   
        def position(self, value):
            self._position = value

        @property
        def look_at(self):
            return self._look_at
        
        @look_at.setter
        def look_at(self, value):
            self._look_at = value

    def __init__(self, path=None, **kwargs) -> None:
        if path is not None:
            with open(path, "r+", encoding="utf-8") as file:
                kwargs: dict = json.load(file)
            file.close()
        else:
            kwargs = kwargs
        
        self.name: str = kwargs["name"]
        self.position: Sequence = np.array(kwargs["position"])
        self.camera: Player.Camera = Player.Camera(**kwargs)
        self.role: str = kwargs["role"]
        self.collision: Sequence = kwargs["collision"]
        self.model = kwargs["model"]
        self.init()

    def init(self):
        self.model = [create_model.cube(*value) for value in self.model.values()]


    def draw(self):
        for obj in self.model:
            obj.draw()

    def move(self, x, y, z):
        self.position += np.array([x, y, z])
        glTranslatef([x, y, z])

    def rotate(self, x, y, z, *, deg = None, rad = None):
        ...

    def run(self):
        "玩家循环任务"
        # 更新玩家视角
        gluLookAt(
            *self.camera.position,
            *self.camera.look_at,
            *self.camera.up
        )