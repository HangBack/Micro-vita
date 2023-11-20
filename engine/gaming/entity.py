import abc
from engine.const import *


def __import():
    global Game, gaming
    from engine.game import Game
    from engine import gaming


class Camera:

    def __init__(self, **kwargs) -> None:
        self._position: Iterable = np.array(
            kwargs["camera"]["position"], dtype=np.float32)
        self._look_at: Iterable = np.array(
            kwargs["camera"]["look_at"], dtype=np.float32)
        self._up: Iterable = np.array(kwargs["camera"]["up"], dtype=np.float32)
        self._pitch: float = kwargs["camera"]["pitch"]
        self._yaw: float = kwargs["camera"]["yaw"]
        self._roll: float = kwargs["camera"]["roll"]
        self._front = np.array([0., 0., -1.], dtype=np.float32)

        self.z_vector = const.normalize(self._position - self._look_at)
        self.x_vector = const.normalize(np.cross(
            np.array([0, 1, 0], dtype=np.float32), self._z_vector
        ))
        self.up = np.cross(self._z_vector, self._x_vector)

        self.front = True
        self.view_matrix = True
        pass

    @property
    def view_matrix(self):
        return pyrr.matrix44.create_look_at(*self._view_matrix)

    @view_matrix.setter
    def view_matrix(self, value):
        if value is True:
            self._view_matrix = [self._position, self._look_at, self._up]
        else:
            raise ValueError("视图矩阵不可直接更改")

    @property
    def front(self):
        "摄像机前向量"
        return self._front

    @front.setter
    def front(self, value):
        if value is True:
            pitch_rad, yaw_rad = np.deg2rad([self._pitch, self._yaw])
            self._front[0] = np.cos(pitch_rad) * np.cos(yaw_rad)
            self._front[1] = np.sin(pitch_rad)
            self._front[2] = np.cos(pitch_rad) * np.sin(yaw_rad)
        else:
            self._front = np.array(value, dtype=np.float32)
        self.look_at = True

    @property
    def yaw(self):
        "偏航角"
        return self._yaw

    @yaw.setter
    def yaw(self, value):
        "偏航角，达到阈值复位"
        if self._yaw > 360.0:
            self._yaw -= 360.0
        elif self._yaw < 0.0:
            self._yaw += 360.0
        else:
            self._yaw = value
        self.front = True  # 更新摄像机前方向向量

    @property
    def pitch(self):
        "仰俯角"
        return self._pitch

    @pitch.setter
    def pitch(self, value):
        "仰俯角,夹在上下限"
        self._pitch = clamp_number(value, -89.9, 89.9)
        self.front = True  # 更新摄像机前方向向量

    @property
    def roll(self):
        "滚转角"
        return self._roll

    @roll.setter
    def roll(self, value):
        "滚转角，达到阈值复位"
        if self.roll > 360.0:
            self.roll -= 360.0
        elif self.roll < 0.0:
            self.roll += 360.0
        else:
            self.roll = value
        self.front = True  # 更新摄像机前方向向量

    @property
    def up(self):
        "摄像机y轴向量"
        return self._up

    @up.setter
    def up(self, value):
        if value is True:
            self._up = np.cross(self._z_vector, self._x_vector)
        else:
            self._up = np.array(value, dtype=np.float32)
        self.view_matrix = True  # 更新视图矩阵

    @property
    def position(self):
        "摄像机位置"
        return self._position

    @position.setter
    def position(self, value):
        self._position = np.array(value, dtype=np.float32)
        self.look_at = True  # 更新视点

    @property
    def look_at(self):
        "摄像机视点"
        return self._look_at

    @look_at.setter
    def look_at(self, value):
        if value is True:
            self._look_at = self._position + self._front
        else:
            self._look_at = np.array(value, dtype=np.float32)
        self.z_vector = True  # 更新z轴向量

    @property
    def z_vector(self):
        "摄像机z轴向量"
        return self._z_vector

    @z_vector.setter
    def z_vector(self, value):
        if value is True:
            self._z_vector = const.normalize(self._position - self._look_at)
        else:
            self._z_vector = np.array(value, dtype=np.float32)
        self.x_vector = True  # 更新x轴向量

    @property
    def x_vector(self):
        "摄像机x轴向量"
        return self._x_vector

    @x_vector.setter
    def x_vector(self, value):
        if value is True:
            self._x_vector = const.normalize(np.cross(
                np.array([0, 1, 0], dtype=np.float32), self._z_vector
            ))
        else:
            self._x_vector = np.array(value, dtype=np.float32)
        self.up = True


class Entity(metaclass=abc.ABCMeta):

    def __init__(self) -> None:
        self._position: np.ndarray = np.zeros(3, dtype=np.float32)
        self._scene: 'gaming.scene.Scene'

    @abc.abstractmethod
    def move(self, x: float | int, y: float | int, z: float | int):
        "移动"
        ...

    @property
    def position(self) -> np.ndarray:
        "位置"
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def scene(self) -> 'gaming.scene.Scene':
        "所处场景"
        return self._scene

    @scene.setter
    def scene(self, value):
        "所处场景"
        self._scene = value

    def move_with_collision(self,
                            x: float | int,
                            y: float | int,
                            z: float | int):
        if not hasattr(self.game.scene, 'current_node'):
            self.game.scene.current_node = self.game.scene.octree
        dimension = self.game.scene.current_node

        while True:
            if isinstance(dimension.children, Iterable):
                dimension = dimension.children[self.in_which]         # 更新所处最小包围盒
            elif ...: # 未发生碰撞则移动
                x = clamp_number(x, ..., ...)
                y = clamp_number(y, ..., ...)
                z = clamp_number(z, ..., ...)
                self.move(x, y, z)
                break
            else:
                dimension = dimension.parent
    @property
    def in_which(self) -> int:
        self.game.scene

    def bind_game(self, game: 'Game'):
        self.game = game
