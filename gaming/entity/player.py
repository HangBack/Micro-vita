import json
import numpy as np
from typing import Sequence

from modules import create_model
from ..settings.control import Settings as ControlSettings
from const import *

class Player:

    class Behavior(object):

        def __init__(self, args: Sequence) -> None:
            self.args = args

        def __mul__(self, value) -> Sequence:
            result = []
            if isinstance(value, Sequence) and len(value) == 3:
                return [self.args[i] * x for i, x in enumerate(value)]
            else:
                raise ValueError("Need a 3 element Sequence.")



        def __iter__(self):
            for element in self.args:
                yield element

    class Camera:

        def __init__(self, **kwargs) -> None:
            self._look_at: Sequence = kwargs["camera"]["look_at"]
            self._position: Sequence = kwargs["camera"]["position"]
            self._up: Sequence = kwargs["camera"]["up"]
            self._pitch: float = kwargs["camera"]["pitch"]
            self._yaw: float = kwargs["camera"]["yaw"]
            self._roll: float = kwargs["camera"]["roll"]
            pass

        def _change_euler_angle(self):
            "改变欧拉角，自动更新look_at"
            pitch_rad, yaw_rad = np.deg2rad([self._pitch, self._yaw])

            self._look_at[0] = np.sin(yaw_rad) * np.cos(pitch_rad)
            self._look_at[1] = np.sin(pitch_rad)
            self._look_at[2] = -np.cos(yaw_rad) * np.cos(pitch_rad)


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
            self._change_euler_angle() # 改变欧拉角

        @property
        def pitch(self):
            return self._pitch

        @pitch.setter   
        def pitch(self, value):
            "y 夹在上下限"
            self._pitch = clamp_number(value, -90.0, 90.0)
            self._change_euler_angle() # 改变欧拉角

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
            self._change_euler_angle() # 改变欧拉角

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

            with open(path + ".json", "r+", encoding="utf-8") as file:
                kwargs: dict = json.load(file)
            file.close()

            with open(path + ".settings.json", "r+", encoding="utf-8") as file:
                self.settings: ControlSettings = ControlSettings(**json.load(file)['control'])
            file.close()
        
        self.name: str = kwargs["name"]
        self.position: Sequence = kwargs["position"]
        self.role: str = kwargs["role"]
        self.collision: Sequence = kwargs["collision"]
        self.model = kwargs["model"]
        self.scene = "gaming_type"

        self.camera: Player.Camera = Player.Camera(**kwargs)
        self.behavior: Player.Behavior = self.Behavior(kwargs["behavior"])
        self.init()

    def init(self):
        self.model = [create_model.cube(*value) for value in self.model.values()]

        # 加速度和最大速度
        self.accelerate_speed = 0.1
        self.max_speed = 1.0


    def draw(self):
        for obj in self.model:
            obj.draw()

    def move(self, x, y, z):
        "玩家移动方法"
        # 更新物理位置
        self.position = list(
            np.array(self.position) +
            np.array([x, y, z])
        )
        # 更新摄像机位置
        self.camera.position = list(
            np.array(self.camera.position) +
            np.array([x, y, z])
        )

    def rotate(self, rotation: Sequence):
        "玩家转向方法"
        rotation = list(reversed(rotation))

        self.camera.pitch = self.camera.pitch - rotation[0] # 减是因为上下颠倒
        self.camera.yaw = self.camera.yaw + rotation[1]

    def run(self):
        "玩家循环任务"
        # 更新玩家视角
        gluLookAt(
            *self.camera.position,
            *(np.array(self.camera.look_at) + np.array(self.camera.position)), # 重要，待研究
            *self.camera.up
        )