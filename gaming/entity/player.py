import json
import numpy as np
from typing import Sequence

from modules import create_model
from .. import settings
from ._const import *

class Player:

    def __init__(self, settings: settings, path=None, **kwargs) -> None:
        if path is not None:
            with open(path, "r+", encoding="utf-8") as file:
                self.file: dict = json.load(file)
            file.close()
        else:
            self.file = kwargs
        
        self.name: str = self.file["name"]
        self.position: Sequence = np.array(self.file["position"])
        self._rotation: Sequence = np.array(self.file["rotation"])
        self.role: str = self.file["role"]
        self.collision: Sequence = self.file["collision"]
        self.model = self.file["model"]
        self.control_settings = settings.control.Settings(self.file[""])
        self.init()

    @property
    def rotation(self):
        return self._rotation
    
    @rotation.setter
    def rotation(self, value):
        # x 达到阈值复位
        if self._rotation[0] > 360.0:
            self._rotation[0] = 0.0
        elif self._rotation[0] < 0.0:
            self._rotation[0] = 360.0
        # y 夹在上下限
        self._rotation[1] = clamp_number(self._rotation[1], -89.0, 89.0)

        # z 达到阈值复位
        if self._rotation[2] > 360.0:
            self._rotation[2] = 0.0
        elif self._rotation[2] < 0.0:
            self._rotation[2] = 360.0

    def init(self):
        self.model = [create_model.cube(*value) for value in self.model.values()]

    def camera(self, x, y, z):
        ...


    def draw(self):
        for obj in self.model:
            obj.draw()

    def move(self, x, y, z):
        self.position += np.array([x, y, z])
        glTranslatef([x, y, z])

    def rotate(self, x, y, z, *, deg = None, rad = None):
        ...