import pygame as pg

from OpenGL.GLU import *
from OpenGL.GL import *
import random
from pygame.locals import *
from modules import create_model
def main():
    pg.init()
    display = (1680, 1050)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -7)
    cubes = [
        create_model.cube(x * (1 + random.random()), y * (1 + random.random()), z * (1 + random.random()), (r / 2 + 0.5, g / 2 + 0.5, b / 2 + 0.5)) 
        for r, x in enumerate([1, -1])
        for g, y in enumerate([1, -1])
        for b, z in enumerate([1, -1])
    ]
    glCullFace(GL_BACK)
    glEnable(GL_DEPTH_TEST)
    glPolygonOffset(-1.0, -1)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        glRotatef(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for cube in cubes:
            cube.draw()
            cube.move(random.random() / 10 * [1, -1][random.randint(0, 1)], random.random() / 10 * [1, -1][random.randint(0, 1)],random.random() / 10 * [1, -1][random.randint(0, 1)])
        pg.display.flip()
        pg.time.wait(10)

if __name__ == "__main__":
    main()