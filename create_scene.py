from engine.modules.models import Cube
from engine.modules.scenes.threeD import Scene
import random
from OpenGL.GL import *
import numpy as np
import math


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
    # return Scene('resources/scene/demo.json')
    cubes: list[Cube] = []
    mm = 1000
    ml = mm * 7
    m = int(ml ** (1 / 2))
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
            i // m * 10,
            1,
            i % m * 10
        ]))
    scene = Scene('demo', cubes)
    return scene

test().export('resources/scene/demo2.json', 'file')
