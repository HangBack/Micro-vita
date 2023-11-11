import pygame as game
from pygame.locals import *
import numpy as np
from OpenGL.GL import *
from const import compile_shader
import pyrr
import random
import math

class Game:

    def __init__(self, shader_path, caption) -> None:
        game.init()
        self.window = game.display.set_mode(
            (0, 0),
            DOUBLEBUF | OPENGL | FULLSCREEN
        )
        game.display.set_caption(caption)
        self.shader = compile_shader(shader_path)
        # with open(f'{shader_path}.vert', 'r') as file:
        #     vert = compileShader(file.read(), GL_VERTEX_SHADER),
        # file.close()
        # with open(f'{shader_path}.frag', 'r') as file:
        #     frag = compileShader(file.read(), GL_FRAGMENT_SHADER),
        # file.close()
        # self.shader = compileProgram(vert, frag)

    def load_cube(self):
        self.projection = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        self.model = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        self.view = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        self.vertices = np.array([
            [-0.5, -0.5, -0.5], # 0
            [+0.5, -0.5, -0.5], # 1
            [+0.5, +0.5, -0.5], # 2
            [-0.5, +0.5, -0.5], # 3
            [-0.5, -0.5, +0.5], # 4
            [+0.5, -0.5, +0.5], # 5
            [+0.5, +0.5, +0.5], # 6
            [-0.5, +0.5, +0.5]  # 7
        ], dtype=np.float32)
        self.indices = np.array([
            0, 1, 2, 0, 3, 2, # 前面
            4, 5, 6, 4, 7, 6, # 后面
            0, 4, 7, 0, 3, 7, # 左面
            1, 5, 6, 1, 2, 6, # 右面
            0, 4, 5, 0, 1, 5, # 上面
            3, 7, 6, 3, 2, 6  # 下面
        ], dtype=np.uint32)
        self.positions = []
        for ii in range(50):
            for jj in range(50):
                x = np.array([
                    math.sin(math.pi * ii / 50) *
                    math.cos(math.pi * 2.0 * jj / 50),
                    math.cos(math.pi * ii / 50),
                    math.sin(math.pi * ii / 50) *
                    math.sin(math.pi * 2.0 * jj / 50)
                ]) * random.random() * 5
                self.positions.extend(tuple(x))
        self.positions = []
        for _ in range(2500):
            x =  [random.random() * random.randrange(-1, 2, 2) * 3 for _ in range(3)]
            self.positions.extend(tuple(x))
        self.positions = np.array(self.positions, dtype=np.float32)
        self.colors = []
        for i in range(2500):
            x =  [random.random() * 1 for _ in range(3)]
            self.colors.extend(tuple(x))
        self.colors = np.array(self.colors, dtype=np.float32)
        self.scale = []
        for i in range(2500):
            x =  [random.random() / 2 for _ in range(3)]
            self.scale.extend(tuple(x))
        self.scale = np.array(self.scale, dtype=np.float32)
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.EBO = glGenBuffers(1)
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes + self.positions.nbytes + self.scale.nbytes + self.colors.nbytes,
                        None, GL_STATIC_DRAW)
        glBufferSubData(GL_ARRAY_BUFFER, 0,
                        self.vertices.nbytes, self.vertices)
        
        glBufferSubData(GL_ARRAY_BUFFER, self.vertices.nbytes,
                        self.positions.nbytes, self.positions)
        
        glBufferSubData(GL_ARRAY_BUFFER, self.vertices.nbytes + self.positions.nbytes,
                        self.scale.nbytes, self.scale) # 第二个参数是起始位，第三个参数是偏移量
        
        glBufferSubData(GL_ARRAY_BUFFER, self.vertices.nbytes + self.positions.nbytes + self.scale.nbytes,
                        self.colors.nbytes, self.colors)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes,
                        self.indices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT,
                            GL_FALSE, 12, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT,
                            GL_FALSE, 12, ctypes.c_void_p(self.vertices.nbytes))
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT,
                            GL_FALSE, 12, ctypes.c_void_p(self.vertices.nbytes + self.positions.nbytes))
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 3, GL_FLOAT,
                            GL_FALSE, 12, ctypes.c_void_p(self.vertices.nbytes + self.positions.nbytes + self.scale.nbytes))
        glVertexAttribDivisor(1, 1)
        glVertexAttribDivisor(2, 1)
        glVertexAttribDivisor(3, 1)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def draw(self, deg):
        glBindVertexArray(self.VAO)
        glUseProgram(self.shader)
        self.view_loc = glGetUniformLocation(self.shader, "view")
        self.model_loc = glGetUniformLocation(self.shader, "model")
        self.projection_loc = glGetUniformLocation(self.shader, "projection")
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, pyrr.matrix44.create_from_x_rotation(deg) @ pyrr.matrix44.create_from_y_rotation(deg) @ pyrr.matrix44.create_from_z_rotation(deg))
        glUniformMatrix4fv(self.projection_loc, 1, GL_FALSE, pyrr.matrix44.create_perspective_projection(90, self.window.get_rect().width / self.window.get_rect().height, 0.0001, 2000., dtype=np.float32))
        glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, pyrr.matrix44.create_look_at((0, 0, 10), (0, 0, 0), (1, 0, 1)))
        glDrawElementsInstanced(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None, 2500)
        glUseProgram(0)


def main():
    GAME = Game('resources/assets/shaders/core/regular/cube', 'Demo')
    GAME.load_cube()
    glClearColor(0.1, 0.5, 1.0, 1.0)
    glCullFace(GL_BACK)
    glEnable(GL_DEPTH_TEST)
    deg = 0
    while True:
        deg += 0.05
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        GAME.draw(deg)

        game.display.flip()
        game.time.wait(10)


if __name__ == "__main__":
    main()
