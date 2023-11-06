import numpy as np
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from OpenGL.GLUT import *
from pygame.locals import *
import pygame as game
from typing import Sequence, Union
import random
import os

class const:
    display = (0, 0)
    fovy = 90
    zNear = .0005
    zFar = 2000.
    title = "Micro vita 2d"
    version = "demo 1.0"
    caption = f"{title} {version}"
    _NORM = np.linalg.norm
    _UNIT = lambda u: np.array(u) / const._NORM(np.array(u))

def compile_shader(path):
    with open(path + '.frag', "r") as file:
        frag = compileShader(file.read(), GL_FRAGMENT_SHADER)
    file.close()
    with open(path + '.vert', "r") as file:
         vert = compileShader(file.read(), GL_VERTEX_SHADER)
    file.close()
    return frag, vert

def clamp_number(num,a,b):
    return max(min(num, max(a, b)), min(a, b))

def rotate_vector(u, v, deg=None, rad=None) -> Sequence:
    "空间向量v绕轴向量u旋转deg度或rad弧度"
    u, v = np.array(u), np.array(v)
    if deg is not None:
        rad = np.deg2rad(deg)
    # 单位化
    u = (1 / const._NORM(u)) * u

    # 投影向量
    v_proj = np.dot(v, u) * u
    v = v - np.dot(v, u) * u
    
    #叉乘计算旋转平面内的y轴方向(这里写成w)
    w = np.cross(u, v)

    #计算旋转后的向量
    v = np.cos(rad) * v + np.sin(rad) * w
    return v + v_proj