import pygame as game
import numpy as np


from OpenGL.GL import *
from OpenGL.GLU import *

from const import *

class polyhedron:
    
    def __init__(self) -> None:
        pass

class cube(object):
    
    def __init__(self, length, width, height, texture = None) -> None:
        """
        Regular hexahadron
        """
        # 大小矢量
        self.vector = np.array((length, width, height), dtype=float)
        # 顶点
        # 以进位形式表达一个直四棱柱矩阵，x为第一位，y为第二位，z为第三位 其结果乘以三个分量即为该块最终的形状
        self.vertices = np.array([
            (x * length, y * width, z * height) 
            for x in [0, 1] 
            for y in [0, 1] 
            for z in [0, 1]
        ], dtype=float)
        # 边
        self.edges = [
            (0, 1), (0, 2), (0, 4),
            (1, 3), (1, 5),
            (2, 3), (2, 6),
            (3, 7),
            (4, 5), (4, 6),
            (5, 7),
            (6, 7)
        ]
        # 面
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
        glDisable(GL_LIGHTING)
        if self.texture:
            glBegin(GL_QUADS)
            glColor(self.texture) # 先设置颜色，再绘制
            for quad in self.quads:
                for vertex in quad:
                    glVertex3fv(self.vertices[vertex])
            glEnd()
        else:
            glBegin(GL_LINES)
            for edge in self.edges:
                for vertex in edge:
                    glVertex3fv(self.vertices[vertex])
            glEnd()
        glEnable(GL_LIGHTING)
    
    def move(self, x: float | int, y: float | int, z: float | int):
        self.vertices += np.array([x, y, z])

    def rotate(self, /, x: float | int, y: float | int, z: float | int, *, deg: float = None, rad: float = None):
        if deg is not None:
            rad = np.deg2rad(deg)
        u = [x, y, z] # 轴向量
        
        for i, v in enumerate(self.vertices):
            self.vertices[i] = rotate_vector(u, v, rad=rad)

    def scale(self, amount: float, x: float = 1, y: float = 1, z: float = 1):
        self.vertices *= np.array([x, y, z]) * amount

    def __iter__(self):
        for element in self.vertices:
            yield element