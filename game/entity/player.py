import json
import numpy as np
from typing import Sequence

import pygame as game

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
        self.model: dict = self.file["model"]
        self.init()

    def init(self):
        model = []
        for key, value in self.model.items():
            ...

    def camera(self, x, y, z):
        ...


    def draw(self):
        self.model

    def move(self, x, y, z):
        self.position += np.array([x, y, z])
        self.