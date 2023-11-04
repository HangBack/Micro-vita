from modules import create_model
import random
def test():
    cubes = [
        create_model.cube(0.025 * 2 * 100, 0.025 * 2 * 100, 0.025 * 2 * 100, (1, 1, 1)),
        create_model.cube(0.025 * 2 * 100, 1.25 * 2 * 100, 0.025 * 2 * 100, (0, 0, 1)),
        create_model.cube(0.025 * 2 * 100, 0.025 * 2 * 100, 1.25 * 2 * 100, (0, 1, 0)),
        create_model.cube(1.25 * 2 * 100, 0.025 * 2 * 100, 0.025 * 2 * 100, (1, 0, 0))
    ]
    for cube in cubes:
        cube.move(-0.025 * 100, -0.125 * 100, -1.025 * 100)
    cubes[1].move(0, 0.075 * 100, 0)
    cubes[2].move(0, 0, -2.525 * 100)
    cubes[3].move(0.075 * 100, 0, 0)
    return cubes