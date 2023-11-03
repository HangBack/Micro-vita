from modules import create_model
import random
def test():
    cubes = [
        create_model.cube(x * (2), y * (2), z * (2), (r / 2 + 0.5, g / 2 + 0.5, b / 2 + 0.5)) 
        for r, x in enumerate([1, -1])
        for g, y in enumerate([1, -1])
        for b, z in enumerate([1, -1])
    ]
    for cube in cubes:
        cube.move(0, -2, 0)
    return cubes