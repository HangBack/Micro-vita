from ..event import Event as parent
from const import *

class Event(parent):
    def __init__(self) -> None:
        self.tasks = {}

    def trigger(self, tick, **kwargs):
        for task in self.tasks.values():
            if callable(task):
                task()

        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                quit()

            if self.game.user.scene == "gaming_type":

                game.mouse.set_visible(False)
                    
                keys = [
                    {key: getattr(self.game.user.settings.control, key)}
                    for key in 
                        dir(self.game.user.settings.control) 
                    if not key.startswith('__')
                ]
                if event.type == KEYDOWN:
                    for key in keys:
                        if event.key == list(*key.items())[1]:
                            self.tasks.__setitem__(
                                list(*key.items())[0], # 被按的键位
                                getattr(self, list(*key.items())[0] + "_pressed") # 键位映射的函数名
                            )

                if event.type == KEYUP:

                    if event.key == K_ESCAPE:
                        game.quit()
                        quit()

                    for key in keys:
                        if event.key == list(*key.items())[1]:
                            callback = getattr(self, list(*key.items())[0] + "_released") # 键位映射的函数名
                            if callable(callback):
                                callback()

                if event.type == MOUSEMOTION:
                    rotation = np.array(event.rel)
                    if not (rotation == np.array([0, 0])).all():
                        self.turn_the_perspective(rotation / 10, **kwargs)
        ...

    def turn_the_perspective(self, rotation, **kwargs):
        "转动视角事件"
        # 调用玩家转动方法
        self.game.user.rotate(rotation)
        # 重置鼠标中心
        game.mouse.set_pos(self.game.center_pos)

    def move_forward_pressed(self, accelerate_speed=None, start_speed=None, max_speed=None, **kwargs):
        "玩家按压前进事件"
        if not hasattr(self, "_fb_speed_iter"):
            self._fb_speed_iter = 0

        if start_speed is None:
            start_speed = self.game.user.start_speed

        if accelerate_speed is None:
            accelerate_speed = self.game.user.accelerate_speed
        
        if max_speed is None:
            max_speed = self.game.user.max_speed

        self._fb_speed_iter = clamp_number(self._fb_speed_iter + accelerate_speed, start_speed, max_speed)
        speed = self._fb_speed_iter

        look_at = self.game.user.behavior * self.game.user.camera._front

        motion = np.array(look_at, dtype=np.float32) * speed
        self.game.user.move(*motion)

    def move_backward_pressed(self, accelerate_speed=None, start_speed=None, max_speed=None, **kwargs):
        "玩家按压后退事件"

        if start_speed is None:
            start_speed = self.game.user.start_speed

        if accelerate_speed is None:
            accelerate_speed = self.game.user.accelerate_speed
        
        if max_speed is None:
            max_speed = self.game.user.max_speed

        self.move_forward_pressed(-accelerate_speed, -start_speed, -max_speed)

    def move_right_pressed(self, accelerate_speed=None, start_speed=None, max_speed=None, **kwargs):
        "玩家按压右移动事件"
        if not hasattr(self, "_lr_speed_iter"):
            self._lr_speed_iter = 0

        if start_speed is None:
            start_speed = self.game.user.start_speed

        if accelerate_speed is None:
            accelerate_speed = self.game.user.accelerate_speed
        
        if max_speed is None:
            max_speed = self.game.user.max_speed

        self._lr_speed_iter = clamp_number(self._lr_speed_iter + accelerate_speed, start_speed, max_speed)
        speed = self._lr_speed_iter

        look_at = self.game.user.behavior * const.normalize(np.cross(self.game.user.camera._front, self.game.user.camera.up))

        motion = np.array(look_at, dtype=np.float32) * speed
        
        self.game.user.move(*motion)

    def move_left_pressed(self, accelerate_speed=None, start_speed=None, max_speed=None, **kwargs):
        "玩家按压左移动事件"

        if start_speed is None:
            start_speed = self.game.user.start_speed

        if accelerate_speed is None:
            accelerate_speed = self.game.user.accelerate_speed
        
        if max_speed is None:
            max_speed = self.game.user.max_speed
        
        self.move_right_pressed(-accelerate_speed, -start_speed, -max_speed)

    def move_up_pressed(self, accelerate_speed=None, start_speed=None, max_speed=None, **kwargs):
        "玩家按压上移动事件"
        if not hasattr(self, "_ud_speed_iter"):
            self._ud_speed_iter = 0
        
        if start_speed is None:
            start_speed = self.game.user.start_speed
        
        if accelerate_speed is None:
            accelerate_speed = self.game.user.accelerate_speed
        
        if max_speed is None:
            max_speed = self.game.user.max_speed
        
        self._ud_speed_iter = clamp_number(self._ud_speed_iter + accelerate_speed, start_speed, max_speed)
        speed = self._ud_speed_iter

        motion = np.array([0, 1, 0]) * speed
        
        self.game.user.move(*motion)

    def move_down_pressed(self, accelerate_speed=None, start_speed=None, max_speed=None, **kwargs):
        "玩家按压下移动事件"
        if start_speed is None:
            start_speed = self.game.user.start_speed
        
        if accelerate_speed is None:
            accelerate_speed = self.game.user.accelerate_speed
        
        if max_speed is None:
            max_speed = self.game.user.max_speed
        
        self.move_up_pressed(-accelerate_speed, -start_speed, -max_speed)

    def move_forward_released(self):
        if hasattr(self, '_fb_speed_iter'):
            del self._fb_speed_iter
        if "move_forward" in self.tasks:
            del self.tasks["move_forward"]

    def move_backward_released(self):
        if hasattr(self, '_fb_speed_iter'):
            del self._fb_speed_iter
        if "move_backward" in self.tasks:
            del self.tasks["move_backward"]

    def move_left_released(self):
        if hasattr(self, '_lr_speed_iter'):
            del self._lr_speed_iter
        if "move_left" in self.tasks:
            del self.tasks["move_left"]

    def move_right_released(self):
        if hasattr(self, '_lr_speed_iter'):
            del self._lr_speed_iter
        if "move_right" in self.tasks:
            del self.tasks["move_right"]

    def move_up_released(self):
        if hasattr(self, '_ud_speed_iter'):
            del self._ud_speed_iter
        if "move_up" in self.tasks:
            del self.tasks["move_up"]

    def move_down_released(self):
        if hasattr(self, '_ud_speed_iter'):
            del self._ud_speed_iter
        if "move_down" in self.tasks:
            del self.tasks["move_down"]
