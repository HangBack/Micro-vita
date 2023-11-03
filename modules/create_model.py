import pygame as game
import numpy as np


from OpenGL.GL import *
from OpenGL.GLU import *

class polyhedron:
    
    def __init__(self) -> None:
        pass

class cube(object):
    
    def __init__(self, length, width, height, texture = None) -> None:
        """
        Regular hexahadron
        """
        self.vector = np.array((length, width, height))
        # 以进位形式表达一个直四棱柱矩阵，x为第一位，y为第二位，z为第三位 其结果乘以三个分量即为该块最终的形状
        self.vertices = np.array([
            (x * length, y * width, z * height) 
            for x in [0, 1] 
            for y in [0, 1] 
            for z in [0, 1]
        ])
        self.edges = [
            (0, 1), (0, 2), (0, 4),
            (1, 3), (1, 5),
            (2, 3), (2, 6),
            (3, 7),
            (4, 5), (4, 6),
            (5, 7),
            (6, 7)
        ]
        self.quads = [
            (0, 1, 3, 2),
            (2, 3, 7, 6),
            (7, 6, 4, 5),
            (4, 5, 1, 0),
            (0, 2, 6, 4),
            (1, 3, 7, 5)
        ]
        self.texture = texture
        

    def draw(self):
        if self.texture:
            glBegin(GL_QUADS)
            for quad in self.quads:
                for vertex in quad:
                    glVertex3fv(self.vertices[vertex])
                    glColor(self.texture)
            glEnd()
        else:
            glBegin(GL_LINES)
            for edge in self.edges:
                for vertex in edge:
                    glVertex3fv(self.vertices[vertex])
            glEnd()
    
    def move(self, x: float | int, y: float | int, z: float | int):
        self.vertices += np.array([x, y, z])

    def rotate(self, /, x: float | int, y: float | int, z: float | int, *, deg: float = None, rad: float = None):
        if deg is not None:
            rad = np.deg2rad(deg)
        _norm = np.linalg.norm
        # 轴
        u = np.array([x, y, z])
        for i, v in enumerate(self.vertices):
            # 单位化
            u = (1 / _norm(u)) * u

            # 投影向量
            v_proj = np.dot(v, u) * u
            v = v - np.dot(v, u) * u
            
            #叉乘计算旋转平面内的y轴方向(这里写成w)
            w = np.cross(u, v)

            #计算旋转后的向量
            v = np.cos(rad) * v + np.sin(rad) * w
            self.vertices[i] = v + v_proj

    def scale(self, amount: float, x: float = 1, y: float = 1, z: float = 1):
        self.vertices *= np.array([x, y, z]) * amount

    def __iter__(self):
        for element in self.vertices:
            yield element