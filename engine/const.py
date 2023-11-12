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
from typing import Callable
from typing import NoReturn
from typing import NewType
from typing import Union

import os
import abc
import time
import math
import pyrr
import json
import random
import logging


class const:
    TITLE = "Micro vita 2d"
    VERSION = "demo 1.0"
    CAPTION = f"{TITLE} {VERSION}"
    INFINITY = math.inf
    SHADER_PATH_PREFFIX = 'resources/assets/shaders/core'

    @staticmethod
    def normalize(u: Sequence) -> Sequence:
        "输入向量u，返回单位向量v"
        u_vector = np.array(u)
        v = u_vector / np.linalg.norm(u_vector)
        return v

    @staticmethod
    def SHADER_PATH(_dir, name):
        prefix = const.SHADER_PATH_PREFFIX
        module = _dir.split('.')[-1]
        return eval(f"f'{prefix}/{module}/'") + name


def compile_shader(path: os.PathLike):
    mapping = {
        ".vert": GL_VERTEX_SHADER,
        ".vs": GL_VERTEX_SHADER,
        ".frag": GL_FRAGMENT_SHADER,
        ".fs": GL_VERTEX_SHADER,
        ".gs": GL_GEOMETRY_SHADER,
        ".geom": GL_GEOMETRY_SHADER,
        ".comp": GL_COMPUTE_SHADER,
        ".tesc": GL_TESS_CONTROL_SHADER,
        ".tese": GL_TESS_EVALUATION_SHADER,
        ".rgen": GL_REFERENCED_BY_FRAGMENT_SHADER,
        # ".rint": "",
        # ".rahit": "",
        # ".rchit": "",
        # ".rmiss": "",
        # ".rcall": ""
        # ".mesh": "",
        # ".task": ""
    }
    __exist = os.path.exists

    def reader(path, typer):
        with open(path, 'r') as file:
            glsl = compileShader(file.read(), typer)
        file.close()
        return glsl
    shaders = [
        reader(f"{path}{ext}", typer)
        for ext, typer in mapping.items()
        if __exist(f"{path}{ext}")
    ]
    if shaders:
        return compileProgram(*shaders)


def clamp_number(
        num: float | int,
        a: float | int,
        b: float | int
) -> float | int:
    "将数值num限制在[a, b]或[b, a]之间"
    return max(min(num, max(a, b)), min(a, b))


def rotate_vector(
        u: Sequence,
        v: Sequence,
        deg: float | int = None,
        rad: float | int = None
) -> Sequence:
    """
    空间向量v绕轴向量u旋转deg度或rad弧度
    """
    u, v = np.array(u), np.array(v)
    if deg is not None:
        rad = np.deg2rad(deg)
    # 单位化
    u = const.normalize(u)

    # 投影向量
    v_proj = np.dot(v, u) * u
    v = v - np.dot(v, u) * u

    # 叉乘计算旋转平面内的y轴方向(这里写成w)
    w = np.cross(u, v)

    # 计算旋转后的向量
    v = np.cos(rad) * v + np.sin(rad) * w
    return v + v_proj


__log_file = f'../logs/{time.strftime("%Y-%m-%d", time.localtime(time.time()))}.log'
__log_format = '[%(levelname)s][%(asctime)s.%(msecs)03d]( %(filename)s > %(funcName)s ): %(message)s'
__log_datefmt = '%H:%M:%S'


if os.path.exists(__log_file):
    with open(__log_file, 'a', encoding='utf-8') as file:
        file.write('\n\n')
        file.close()
    logging.basicConfig(filename=__log_file,
                        format=__log_format,
                        level=logging.INFO,
                        datefmt=__log_datefmt,
                        encoding='utf-8')
else:
    if not os.path.isdir('../logs/'):
        os.makedirs('../logs/')
    with open(__log_file, 'a', encoding='utf-8') as file:
        file.close()
    logging.basicConfig(filename=__log_file,
                        format=__log_format,
                        level=logging.INFO,
                        datefmt=__log_datefmt,
                        encoding='utf-8')
