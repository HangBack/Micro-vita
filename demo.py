import pygame as gaming

from const import *
from modules import create_model

import const

def init():
    gaming.init()
    gaming.display.set_mode(
        const.display, 
        DOUBLEBUF|OPENGL|FULLSCREEN,
    )
    gaming.display.set_caption(const.caption)
    gluPerspective(const.fovy, (const.aspect), const.zNear, const.zFar)
    glTranslatef(0.0, 0.0, 0.0)
    glCullFace(GL_BACK)
    glEnable(GL_DEPTH_TEST)

def main():
    gaming.init()
    display = (1680, 1050)
    gaming.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(90, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, 0.0)
    glCullFace(GL_BACK)
    glEnable(GL_DEPTH_TEST)
    end_pos = (0,0)
    left = False
    right = False
    deg = 1
    cubes = [
        create_model.cube(x * (1 + random.random()), y * (1 + random.random()), z * (1 + random.random()), (r / 2 + 0.5, g / 2 + 0.5, b / 2 + 0.5)) 
        for r, x in enumerate([1, -1])
        for g, y in enumerate([1, -1])
        for b, z in enumerate([1, -1])
    ]
    for cube in cubes:
        cube.move(0, -2, 0)
    while True:
        for event in gaming._event.get():
            if event.type == gaming.QUIT:
                gaming.quit()
                quit()

            if event.type == KEYDOWN:
                key = gaming.key.get_pressed()
                match key:
                    case K_ESCAPE:
                        gaming.quit()
                        quit()
            
            if event.type == MOUSEBUTTONDOWN:
                left, middle, right = gaming.mouse.get_pressed()
                if left:
                    start_pos = np.array(gaming.mouse.get_pos())

                if right:
                    start_pos = np.array(gaming.mouse.get_pos())
            
            if event.type == MOUSEBUTTONUP:
                if left and gaming.mouse.get_pressed()[0] == False:
                    left = False
                    end_pos = np.array(gaming.mouse.get_pos())
                    rot_vec = end_pos - start_pos
                    deg = 1

                if right and gaming.mouse.get_pressed()[2] == False:
                    right = False
                    end_pos = np.array(gaming.mouse.get_pos())
                    rot_vec = end_pos - start_pos
            
            if event.type == MOUSEWHEEL:
                glTranslatef(0.0, 0.0, event.y / 2)
        if left:
            end_pos = np.array(gaming.mouse.get_pos())
            rot_vec = end_pos - start_pos
            if deg < 4:
                deg += 0.1
            if not (rot_vec == np.array([0, 0])).all():
                for cube in cubes:
                    cube.rotate(1 * (1 + abs(rot_vec[1])), 1 * (1 + abs(rot_vec[0])), 0, deg=deg)
            start_pos = np.array(gaming.mouse.get_pos())

        if right:
            end_pos = np.array(gaming.mouse.get_pos())
            rot_vec = end_pos - start_pos
            rot_vec = rot_vec / np.linalg.norm(rot_vec)
            if not (end_pos == start_pos).all():
                glTranslatef(rot_vec[0] / 10, rot_vec[1] / -10, 0.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for cube in cubes:
            cube.draw()
        gaming.display.flip()
        gaming.time.wait(1)

if __name__ == "__main__":
    main()