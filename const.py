import numpy as np
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from pygame.locals import *

from OpenGL.GL.shaders import compileShader
from OpenGL.GL.shaders import compileProgram

from PIL import Image as ImageObject

import pygame as game
from typing import Sequence
from typing import Iterable
from typing import NoReturn
from typing import Union

import math
import random
import os
import pyrr


class const:
    DISPLAY = (0, 0)
    FOVY = 90
    ZNEAR = .0005
    ZFAR = 2000.
    TITLE = "Micro vita 2d"
    VERSION = "demo 1.0"
    CAPTION = f"{TITLE} {VERSION}"
    _NORM = np.linalg.norm
    def _UNIT(u: Sequence) -> Sequence:
        "输入向量u，返回单位向量v"
        v = np.array(u) / const._NORM(np.array(u))
        return v
    INFINITY = math.inf
    SHADER_PATH_PREFFIX = 'resources/assets/shaders/core/'


def compile_shader(path: os.PathLike):
    with open(path + '.frag', "r") as file:
        frag = compileShader(file.read(), GL_FRAGMENT_SHADER)
    file.close()
    with open(path + '.vert', "r") as file:
        vert = compileShader(file.read(), GL_VERTEX_SHADER)
    file.close()
    return compileProgram(vert, frag)


def clamp_number(num, a, b):
    return max(min(num, max(a, b)), min(a, b))


def rotate_vector(u, v, deg=None, rad=None) -> Sequence:
    "空间向量v绕轴向量u旋转deg度或rad弧度"
    u, v = np.array(u), np.array(v)
    if deg is not None:
        rad = np.deg2rad(deg)
    # 单位化
    u = const._UNIT(u)

    # 投影向量
    v_proj = np.dot(v, u) * u
    v = v - np.dot(v, u) * u

    # 叉乘计算旋转平面内的y轴方向(这里写成w)
    w = np.cross(u, v)

    # 计算旋转后的向量
    v = np.cos(rad) * v + np.sin(rad) * w
    return v + v_proj

def is_glError():
    error_code = glGetError()
    if error_code != GL_NO_ERROR:
        raise ValueError("错误")