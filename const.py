import numpy as np
from OpenGL.GLU import *
from OpenGL.GL import *
from pygame.locals import *
import pygame as game
import gaming
import random
class const:
    display = (1680, 1050)
    aspect = display[0] / display[1]
    fovy = 90
    zNear = .1
    zFar = 50.
    title = "Micro vita 2d"
    version = "demo 1.0"
    caption = f"{title} {version}"
    _NORM = np.linalg.norm
    _UNIT = lambda u: (1 / const._NORM(u)) * u
    events = [
        gaming.events.player.Event(np.array([0, 0]))
    ]