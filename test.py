from modules import create_model
import random
def test():
    cubes = [
        create_model.cube(0.05 * 2, 0.05 * 2, 0.05 * 2, (0, 0, 0)),
        create_model.cube(0.05 * 2, 0.05 * 2, 4 * 2, (0, 0, 1)),
        create_model.cube(0.05 * 2, 4 * 2, 0.05 * 2, (0, 1, 0)),
        create_model.cube(4 * 2, 0.05 * 2, 0.05 * 2, (1, 0, 0))
    ]
    for cube in cubes:
        cube.move(-4, -4, -4)
    return cubes