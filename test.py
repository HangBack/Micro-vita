from engine.modules.models.regular import cube as Cube
from engine.modules.models.regular import sphere as Sphere
from engine.gaming.scene import Scene
import random
import pygame as pg
from OpenGL.GL import *
import numpy as np
import math

def __import():
    global Game
    from engine.game import Game

def gradient(A, B, Step):
    return [
        (
            A[0] + (B[0] - A[0]) / Step * N,
            A[1] + (B[1] - A[1]) / Step * N,
            A[2] + (B[2] - A[2]) / Step * N
        )
        for N in range(Step + 1)
    ]

def test() -> Scene:
    cubes: list[Cube] = []
    mm = 100
    ml = mm * 7
    grad = [
        *gradient((0, 0, 0), (0, 0, 255), mm),
        *gradient((0, 0, 255), (0, 255, 0), mm),
        *gradient((0, 255, 0), (0, 255, 255), mm),
        *gradient((0, 255, 255), (255, 0, 0), mm),
        *gradient((255, 0, 0), (255, 0, 255), mm),
        *gradient((255, 0, 255), (255, 255, 0), mm),
        *gradient((255, 255, 0), (255, 255, 255), mm)
    ]
    for i in range(ml):
        
        cube = Cube(*[10 for _ in range(3)], colors=[grad[i][0]/ 255,grad[i][1]/ 255,grad[i][2]/ 255])
        cubes.append(cube)
    for i, cube in enumerate(cubes):
        cube.move(*np.array([
            i * 10, i * 10, i * 10
        ]))
        # cube.rotate(*[random.randrange(0, 361) for _ in range(3)])
    return Scene(cubes)
