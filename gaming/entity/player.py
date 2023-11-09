import json
import numpy as np
from typing import Iterable

from modules.models.regular import cube as Cube
from ..settings.control import Settings as ControlSettings
from ..settings.video import Settings as VideoSettings
from const import *

class Player:

    class Settings:

        def __init__(self, **kwargs) -> None:
            self.control = kwargs["control"]
            self.video = kwargs["video"]
            pass

    class Behavior(object):

        def __init__(self, args: Iterable) -> None:
            self.args = args

        def __mul__(self, value) -> Iterable:
            result = []
            if isinstance(value, Iterable) and len(value) == 3:
                return [self.args[i] * x for i, x in enumerate(value)]
            else:
                raise ValueError("Need a 3 element Iterable.")



        def __iter__(self):
            for element in self.args:
                yield element

    class Camera:

        def __init__(self, **kwargs) -> None:
            self._look_at: Iterable = np.array(kwargs["camera"]["look_at"], dtype=np.float32)
            self._position: Iterable = np.array(kwargs["camera"]["position"], dtype=np.float32)
            self._up: Iterable = np.array(kwargs["camera"]["up"], dtype=np.float32)
            self._pitch: float = kwargs["camera"]["pitch"]
            self._yaw: float = kwargs["camera"]["yaw"]
            self._roll: float = kwargs["camera"]["roll"]

            self.z_vector = const._UNIT(self._position - self._look_at)
            self.x_vector = const._UNIT(np.cross(
                np.array([0, 1, 0], dtype=np.float32), self._z_vector
            ))
            self.up = np.cross(self._z_vector, self._x_vector)
            pass

        @property
        def view_matrix(self):
            return pyrr.matrix44.create_look_at(self._position, self._look_at, self._up)

        def _change_euler_angle(self):
            "改变欧拉角，自动更新look_at"
            pitch_rad, yaw_rad = np.deg2rad([self._pitch, self._yaw])
            self.Front = np.array([0, 0, -1], dtype=np.float32)
            self.Front[0] = np.cos(pitch_rad) * np.cos(yaw_rad)
            self.Front[1] = np.sin(pitch_rad)
            self.Front[2] = np.cos(pitch_rad) * np.sin(yaw_rad)
            self.Front = const._UNIT(self.Front)
            self.look_at = self.position + self.Front


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
            self._pitch = clamp_number(value, -89.9, 89.9)
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
            self._up = np.array(value, dtype=np.float32)
            self.view_matrix # 更新视图矩阵

        @property
        def position(self):
            return self._position

        @position.setter   
        def position(self, value):
            self._position = np.array(value, dtype=np.float32)
            self.look_at = self._position + self.Front
            self.z_vector = const._UNIT(self._position - self._look_at)
            self.view_matrix # 更新视图矩阵

        @property
        def look_at(self):
            return self._look_at
        
        @look_at.setter
        def look_at(self, value):
            self._look_at = np.array(value, dtype=np.float32)
            self.z_vector = const._UNIT(self._position - self._look_at)
            self.view_matrix # 更新视图矩阵

        @property
        def z_vector(self):
            return self._z_vector

        @z_vector.setter
        def z_vector(self, value):
            self._z_vector = np.array(value, dtype=np.float32)
            self.x_vector = const._UNIT(np.cross(
                np.array([0, 1, 0], dtype=np.float32), self._z_vector
            ))

        @property
        def x_vector(self):
            return self._x_vector
        
        @x_vector.setter
        def x_vector(self, value):
            self._x_vector = np.array(value, dtype=np.float32)
            self.up = np.cross(self._z_vector, self._x_vector)

    def __init__(self, path=None, **kwargs) -> None:
        if path is not None:

            with open(path + ".json", "r+", encoding="utf-8") as file:
                kwargs: dict = json.load(file)
            file.close()

            with open(path + ".settings.json", "r+", encoding="utf-8") as file:
                # 设置
                context = json.load(file)
                self.settings: Player.Settings = Player.Settings(
                    control = ControlSettings(**context['control']),
                    video = VideoSettings(**context['video'])
                )
            file.close()
        
        self.name: str = kwargs["name"]
        self.position: Iterable = kwargs["position"]
        self.role: str = kwargs["role"]
        self.collision: Iterable = kwargs["collision"]
        self.model = kwargs["model"]
        self.scene = "gaming_type"
        self.camera: Player.Camera = Player.Camera(**kwargs)
        self.behavior: Player.Behavior = self.Behavior(kwargs["behavior"])
        self.init()

    def init(self):
        self.attribute() # 定义属性
        
    def attribute(self):
        self._start_speed = 0 # 初始速度
        self._accelerate_speed = 0.1 # 加速度
        self._max_speed = 1.0 # 最大速度
    
    @property
    def start_speed(self):
        return self._start_speed
    
    @start_speed.setter
    def start_speed(self, value):
        self._start_speed = value

    @property
    def accelerate_speed(self):
        return self._accelerate_speed
    
    @accelerate_speed.setter
    def accelerate_speed(self, value):
        self._accelerate_speed = value

    @property
    def max_speed(self):
        return self._max_speed
    
    @max_speed.setter
    def max_speed(self, value):
        self._max_speed = value

    @property
    def center_pos(self):
        return self._center_pos
    
    @center_pos.setter
    def center_pos(self, value):
        self._center_pos = value

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

    def rotate(self, rotation: Iterable):
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