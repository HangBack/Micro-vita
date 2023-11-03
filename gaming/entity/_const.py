import numpy as np
from OpenGL.GLU import *
from OpenGL.GL import *
import pygame as game
from pygame.locals import *
class const:
    _NORM = np.linalg.norm
    _UNIT = lambda u: np.array(u) / const._NORM(np.array(u))

def clamp_number(num,a,b):
    return max(min(num, max(a, b)), min(a, b))