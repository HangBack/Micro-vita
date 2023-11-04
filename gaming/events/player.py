from .._event import Event as parent
from ..entity.player import Player
from const import *

class Event(parent):

    def __init__(self, player: Player, **kwargs) -> None:
        self.player = player
        self.tasks = {}
        pass

    def trigger(self, **kwargs):
        for task in self.tasks.values():
            if callable(task):
                task()
        self.center_pos = np.array([kwargs["screen_width"] / 2, kwargs["screen_height"] / 2])
        for event in kwargs["pygame_events"]:
            if event.type == game.QUIT:
                game.quit()
                quit()

            if self.player.scene == "gaming_type":
                    
                key = self.player.settings

                if event.type == KEYDOWN:
                    if event.key == key.forward:
                        self.tasks.__setitem__("forward", self.forward)
                    if event.key == key.backward:
                        self.tasks.__setitem__("backward", self.backward)
                    if event.key == key.move_left:
                        self.tasks.__setitem__("move_left", self.move_left)
                    if event.key == key.move_right:
                        self.tasks.__setitem__("move_right", self.move_right)

                if event.type == KEYUP:

                    if event.key == K_ESCAPE:
                        game.quit()
                        quit()
                        
                    if event.key == key.forward:
                        if hasattr(self, "_fb_speed_iter"):
                            del self._fb_speed_iter
                        del self.tasks["forward"]
                        
                    if event.key == key.backward:
                        if hasattr(self, "_fb_speed_iter"):
                            del self._fb_speed_iter
                        del self.tasks["backward"]
                        
                    if event.key == key.move_left:
                        if hasattr(self, "_fb_speed_iter"):
                            del self._fb_speed_iter
                        del self.tasks["move_left"]
                        
                    if event.key == key.move_right:
                        if hasattr(self, "_fb_speed_iter"):
                            del self._fb_speed_iter
                        del self.tasks["move_right"]

                if event.type == MOUSEMOTION:
                    rotation = np.array(event.rel)
                    if not (rotation == np.array([0, 0])).all():
                        self.turn_the_perspective(rotation / 10, **kwargs)
        ...

    def turn_the_perspective(self, rotation, **kwargs):
        "转动视角事件"
        # 调用玩家转动方法
        self.player.rotate(rotation)
        # 重置鼠标中心
        game.mouse.set_pos(self.center_pos)

    def forward(self, accelerate_speed=None, max_speed=None, **kwargs):
        "玩家前进事件"
        if not hasattr(self, "_fb_speed_iter"):
            self._fb_speed_iter = 0

        if accelerate_speed is None:
            accelerate_speed = self.player.accelerate_speed
        
        if max_speed is None:
            max_speed = self.player.max_speed

        self._fb_speed_iter = clamp_number(self._fb_speed_iter + accelerate_speed, 0, self.player.max_speed)
        speed = self._fb_speed_iter

        look_at = self.player.behavior * self.player.camera.look_at

        motion = np.array(look_at) * speed
        self.player.move(*motion)

    def backward(self, accelerate_speed=None, max_speed=None, **kwargs):
        "玩家后退事件"
        if not hasattr(self, "_fb_speed_iter"):
            self._fb_speed_iter = 0

        if accelerate_speed is None:
            accelerate_speed = self.player.accelerate_speed
        
        if max_speed is None:
            max_speed = self.player.max_speed

        self._fb_speed_iter = clamp_number(self._fb_speed_iter - accelerate_speed, -self.player.max_speed, 0)
        speed = self._fb_speed_iter

        look_at = self.player.behavior * self.player.camera.look_at

        motion = np.array(look_at) * speed
        self.player.move(*motion)

    def move_left(self, accelerate_speed=None, max_speed=None, **kwargs):
        "玩家左移动事件"
        if not hasattr(self, "_lr_speed_iter"):
            self._lr_speed_iter = 0

        if accelerate_speed is None:
            accelerate_speed = self.player.accelerate_speed
        
        if max_speed is None:
            max_speed = self.player.max_speed

        self._lr_speed_iter = clamp_number(self._lr_speed_iter + accelerate_speed, 0, self.player.max_speed)
        speed = self._lr_speed_iter
        print(self._lr_speed_iter)

        look_at = self.player.behavior * self.player.camera.look_at

        motion = rotate_vector([0, 1, 0], look_at, 90) * speed
        
        self.player.move(*motion)

    def move_right(self, accelerate_speed=None, max_speed=None, **kwargs):
        "玩家右移动事件"
        if not hasattr(self, "_lr_speed_iter"):
            self._lr_speed_iter = 0

        if accelerate_speed is None:
            accelerate_speed = self.player.accelerate_speed
        
        if max_speed is None:
            max_speed = self.player.max_speed

        self._lr_speed_iter = clamp_number(self._lr_speed_iter - accelerate_speed, -self.player.max_speed, 0)
        speed = self._lr_speed_iter

        look_at = self.player.behavior * self.player.camera.look_at

        motion = rotate_vector([0, 1, 0], look_at, 90) * speed
        
        self.player.move(*motion)

        

        