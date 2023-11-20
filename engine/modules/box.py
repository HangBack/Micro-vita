import abc
from engine.const import *


class Box(metaclass=abc.ABCMeta):

    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def is_collided(self, other: 'Box'):
        "判断碰撞"
        ...

    @staticmethod
    def get_plane(p1: Sequence[float | int],
                  p2: Sequence[float | int],
                  p3: Sequence[float | int]):
        "传入三个点，获得平面方程系数"
        p1 = np.array(p1, dtype=np.float32)
        p2 = np.array(p2, dtype=np.float32)
        p3 = np.array(p3, dtype=np.float32)
        N = np.cross(p2 - p1, p3 - p1)  # 法向量
        D = -(N * p1).sum()
        return np.array([*N, D], dtype=np.float32)