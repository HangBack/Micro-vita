import json
import numpy as np
from typing import Sequence

import pygame as game
from OpenGL.GL import *
from OpenGL.GLU import *

from modules import create_model

class Player:

    def __init__(self, path=None, **kwargs) -> None:
        if path is not None:
            with open(path, "w+", encoding="utf-8") as file:
                self.file: dict = json.load(file)
            file.close()
        else:
            self.file = kwargs
        
        self.name: str = self.file["name"]
        self.position: Sequence = np.array(self.file["position"])
        self.role: str = self.file["role"]
        self.collision: Sequence = self.file["collision"]
        self.model = self.file["model"]
        self.init()

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