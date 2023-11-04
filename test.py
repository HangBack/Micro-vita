from modules import create_model
import random
def test():
    cubes = [
        create_model.cube(0.025 * 2, 0.025 * 2, 0.025 * 2, (1, 1, 1)),
        create_model.cube(0.025 * 2, 1.25 * 2, 0.025 * 2, (0, 0, 1)),
        create_model.cube(0.025 * 2, 0.025 * 2, 1.25 * 2, (0, 1, 0)),
        create_model.cube(1.25 * 2, 0.025 * 2, 0.025 * 2, (1, 0, 0))
    ]
    for cube in cubes:
        cube.move(-0.025, -0.125, -1.025)
    cubes[1].move(0, 0.075, 0)
    cubes[2].move(0, 0, -2.525)
    cubes[3].move(0.075, 0, 0)
    return cubes