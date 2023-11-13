from engine.const import *

from engine.gaming.settings.control import Settings as ControlSettings
from engine.gaming.settings.video import Settings as VideoSettings

from engine.gaming.events.player import Event

import uuid

def __import():
    global Game
    from game import Game

class Player:

    def __init__(self, path=None, **kwargs) -> None:
        if path is not None:

            with open(path + ".json", "r+", encoding="utf-8") as file:
                kwargs: dict = json.load(file)
            file.close()

            with open(path + ".settings.json", "r+", encoding="utf-8") as file:
                # 设置
                context = json.load(file)
                self.settings: Player.Settings = Player.Settings(
                    context = context,
                    control = ControlSettings(context=context),
                    video = VideoSettings(context=context)
                )
            file.close()
        
        self.name: str = kwargs["name"]
        self.position: Iterable = kwargs["position"]
        self.role: str = kwargs["role"]
        self.collision: Iterable = kwargs["collision"]
        self.model = kwargs["model"]
        self.scene = "gaming_type"
        self.camera: Player.Camera = Player.Camera(**kwargs)
        self.behavior: Player.Behavior = Player.Behavior(kwargs["behavior"])
        self.event: Event = Event()
        self.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, 'micro_vita')

    def init(self):
        self.event.bind_player(self)
        self._speed = 0 # 默认速度
        self._start_speed = 0 # 初始速度
        self._accelerate_speed = 0.1 # 加速度
        self._max_speed = 1.0 # 最大速度
    
    @property
    def speed(self):
        "玩家当前速度"
        return self._speed
    
    @speed.setter
    def speed(self, value):
        if value > self.max_speed:
            self._speed = self.max_speed
        else:
            self._speed = value
    
    @property
    def start_speed(self):
        "玩家初速度"
        return self._start_speed
    
    @start_speed.setter
    def start_speed(self, value):
        self._start_speed = value

    @property
    def accelerate_speed(self):
        "玩家加速度"
        return self._accelerate_speed
    
    @accelerate_speed.setter
    def accelerate_speed(self, value):
        self._accelerate_speed = value

    @property
    def max_speed(self):
        "玩家最大速度"
        return self._max_speed
    
    @max_speed.setter
    def max_speed(self, value):
        self._max_speed = value

    @property
    def center_pos(self):
        return self._center_pos
    
    @center_pos.setter
    def center_pos(self, value):
        self._center_pos = value

    def draw(self):
        for obj in self.model:
            obj.draw()

    def move(self, x, y, z):
        "玩家移动方法"
        # 更新物理位置
        self.position = list(
            np.array(self.position) +
            np.array([x, y, z])
        )
        # 更新摄像机位置
        self.camera.position = list(
            np.array(self.camera.position) +
            np.array([x, y, z])
        )

    def rotate(self, rotation: Sequence):
        "玩家转向方法"

        self.camera.pitch = self.camera.pitch - rotation[1] # 减是因为上下颠倒
        self.camera.yaw = self.camera.yaw + rotation[0]

    def bind_game(self, game: 'Game'):
        self.game = game
        self.game.add_player(self)
        self.game.add_cycler(self.run)
        self.settings.bind_game(game)
        self.event.bind_game(game)

    def move_forward(self):
        "玩家向前移动"
        front = self.camera.front
        self.speed = clamp_number(self.speed + self.accelerate_speed, self.start_speed, self.max_speed)
        motion = self.behavior * (front * self.speed)
        self.move(*motion)

    def move_backward(self):
        "玩家向后移动"
        front = self.camera.front
        self.speed = clamp_number(self.speed + self.accelerate_speed, self.start_speed, self.max_speed)
        motion = self.behavior * (front * -self.speed)
        self.move(*motion)

    def move_right(self):
        "玩家向右移动"
        front = const.normalize(np.cross(self.camera.front, self.camera.up))
        self.speed = clamp_number(self.speed + self.accelerate_speed, self.start_speed, self.max_speed)
        motion = self.behavior * (front * self.speed)
        self.move(*motion)

    def move_left(self):
        "玩家向左移动"
        front = const.normalize(np.cross(self.camera.front, self.camera.up))
        self.speed = clamp_number(self.speed + self.accelerate_speed, self.start_speed, self.max_speed)
        motion = self.behavior * (front * -self.speed)
        self.move(*motion)

    def move_up(self):
        "玩家向上移动"
        front = np.array([0, 1, 0], dtype=np.float32)
        self.speed = clamp_number(self.speed + self.accelerate_speed, self.start_speed, self.max_speed)
        motion = (front * self.speed)
        self.move(*motion)

    def move_down(self):
        "玩家向下移动"
        front = np.array([0, 1, 0], dtype=np.float32)
        self.speed = clamp_number(self.speed + self.accelerate_speed, self.start_speed, self.max_speed)
        motion = (front * -self.speed)
        self.move(*motion)

    def turn_the_perspective(self, rotation):
        "转动视角事件"
        self.rotate(rotation)
        game.mouse.set_pos(self.game.center_pos) # 重置鼠标中心坐标

    def run(self):
        "玩家循环任务"
        # 更新玩家视角
        gluLookAt(
            *self.camera.position,
            *(np.array(self.camera.look_at) + np.array(self.camera.position)), # 重要，待研究
            *self.camera.up
        )


        

    class Settings:

        def __init__(self, **kwargs) -> None:
            self.control: ControlSettings = kwargs["control"]
            self.video: VideoSettings = kwargs["video"]
            pass

        def bind_game(self, game):
            self.control.bind_game(game)
            self.video.bind_game(game)

    class Behavior(object):

        def __init__(self, args: Iterable) -> None:
            self.args = args

        def __mul__(self, value) -> Iterable:
            result = []
            if isinstance(value, Iterable) and len(value) == 3:
                return [self.args[i] * x for i, x in enumerate(value)]
            else:
                raise ValueError("Need a 3 element Iterable.")



        def __iter__(self):
            for element in self.args:
                yield element

    class Camera:

        def __init__(self, **kwargs) -> None:
            self._position: Iterable = np.array(kwargs["camera"]["position"], dtype=np.float32)
            self._look_at: Iterable = np.array(kwargs["camera"]["look_at"], dtype=np.float32)
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
            self.front = True # 更新摄像机前方向向量

        @property
        def pitch(self):
            "仰俯角"
            return self._pitch

        @pitch.setter   
        def pitch(self, value):
            "仰俯角,夹在上下限"
            self._pitch = clamp_number(value, -89.9, 89.9)
            self.front = True # 更新摄像机前方向向量

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
            self.front = True # 更新摄像机前方向向量

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
            self.view_matrix = True # 更新视图矩阵

        @property
        def position(self):
            "摄像机位置"
            return self._position

        @position.setter   
        def position(self, value):
            self._position = np.array(value, dtype=np.float32)
            self.look_at = True # 更新视点

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
            self.z_vector = True # 更新z轴向量

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
            self.x_vector = True # 更新x轴向量

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