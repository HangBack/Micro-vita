from modules.models.regular import cube as Cube
from modules.models.regular import sphere as Sphere
from gaming.scene import Scene
import random
import pygame as pg
from OpenGL.GL import *
import numpy as np

def __import():
    global Game
    from game import Game

def test(game: 'Game') -> Scene:
    cubes: list[Cube] = []

    for i in range(1000):
        cube = Cube(*[random.random() * 10 for _ in range(3)], colors=[random.random() for _ in range(3)])
        cubes.append(cube)
    for cube in cubes:
        cube.move(*np.array([random.random()* 1000 * random.randrange(-1, 2, 2) for _ in range(3)]))
        cube.rotate(*[random.randrange(0, 361) for _ in range(3)])
    return Scene(cubes)
