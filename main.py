import pygame as game

from OpenGL.GLU import *
from OpenGL.GL import *
import random
from pygame.locals import *
from modules import create_model

import const

def init():
    game.init()
    game.display.set_mode(
        const.display, 
        DOUBLEBUF|OPENGL,
    )
    gluPerspective(const.fovy, (const.aspect), const.zNear, const.zFar)
    glTranslatef(0.0, 0.0, -7)
    glTranslatef(0.0, 0.0, -7)
    glCullFace(GL_BACK)
    glEnable(GL_DEPTH_TEST)

def update_display():
    game.display.flip()


def main():
    # 初始化
    init()

    # 游戏循环
    while True:
        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                quit()

        # 重置画面
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)



        # 刷新画面
        update_display()

if __name__ == "__main__":
    main()