import numpy as np
from OpenGL.GLU import *
from OpenGL.GL import *
from pygame.locals import *
import pygame as game
import random
class const:
    display = (0, 0)
    fovy = 90
    zNear = .1
    zFar = 50.
    title = "Micro vita 2d"
    version = "demo 1.0"
    caption = f"{title} {version}"
    _NORM = np.linalg.norm
    _UNIT = lambda u: np.array(u) / const._NORM(np.array(u))

def clamp_number(num,a,b):
    return max(min(num, max(a, b)), min(a, b))