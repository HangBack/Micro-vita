from modules.models.regular import cube as Cube
from modules.models.regular import sphere as Sphere
from gaming.scene import Scene
import random

def test() -> Scene:
    cubes = [
        # Cube(0.025 * 2 * 100, 1.25 * 2 * 100, 0.025 * 2 * 100, color=(0, 0, 1)),
        # Cube(0.025 * 2 * 100, 0.025 * 2 * 100, 1.25 * 2 * 100, color=(0, 1, 0)),
        # Cube(1.25 * 2 * 100, 0.025 * 2 * 100, 0.025 * 2 * 100, color=(1, 0, 0)),
        # *[
        #     Sphere((random.random() * 10, random.random() * 10, random.random() * 10), random.random() * 100)
        #     for _ in range(100)
        # ],
        *[
            Cube(*[random.random() * 10 for _ in range(3)], color=[[random.random() for _ in range(3)] for _ in range(8)])
            for i in range(1000)
        ]
    ]
    for cube in cubes[4:]:
        cube.move(*[random.random()* 1000 * random.randrange(-1, 2, 2) for _ in range(3)])
        cube.rotate(*[random.randrange(0, 361) for _ in range(3)])
    return Scene(cubes)

scene = test()