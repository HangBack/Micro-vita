import pygame as pg

from OpenGL.GLU import *
from OpenGL.GL import *
import random, numpy
from pygame.locals import *
from modules import create_model
def main():
    pg.init()
    display = (1680, 1050)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -7)
    glCullFace(GL_BACK)
    glEnable(GL_DEPTH_TEST)
    glPolygonOffset(-1.0, -1)
    end_pos = (0,0)
    left = False
    deg = 1
    cubes = [
        create_model.cube(x * (1 + random.random()), y * (1 + random.random()), z * (1 + random.random()), (r / 2 + 0.5, g / 2 + 0.5, b / 2 + 0.5)) 
        for r, x in enumerate([1, -1])
        for g, y in enumerate([1, -1])
        for b, z in enumerate([1, -1])
    ]
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            
            if event.type == MOUSEBUTTONDOWN:
                left, middle, right = pg.mouse.get_pressed()
                if left:
                    start_pos = numpy.array(pg.mouse.get_pos())
            
            if event.type == MOUSEBUTTONUP:
                if left and pg.mouse.get_pressed()[0] == False:
                    left = False
                    end_pos = numpy.array(pg.mouse.get_pos()) - start_pos
                    deg = 1
            
            if event.type == MOUSEWHEEL:
                glTranslatef(0.0, 0.0, event.y)
        if left:
            if deg < 4:
                deg += 0.1
            end_pos = numpy.array(pg.mouse.get_pos()) - start_pos
            glRotatef(deg, end_pos[1], end_pos[0], 0)
        glPolygonOffset(-1.0, -1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for cube in cubes:
            cube.draw()
            cube.move(random.random() / 10 * [1, -1][random.randint(0, 1)], random.random() / 10 * [1, -1][random.randint(0, 1)],random.random() / 10 * [1, -1][random.randint(0, 1)])
        pg.display.flip()
        pg.time.wait(1)

if __name__ == "__main__":
    main()