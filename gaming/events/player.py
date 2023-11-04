from .._event import Event as parent
from ..entity.player import Player
from const import *

class Event(parent):

    def __init__(self, player: Player, **kwargs) -> None:
        self.player = player
        pass

    def trigger(self, **kwargs):
        self.center_pos = np.array([kwargs["screen_width"] / 2, kwargs["screen_height"] / 2])
        for event in kwargs["pygame_events"]:
            if event.type == MOUSEMOTION:
                rotation = np.array(event.rel)
                if not (rotation == np.array([0, 0])).all():
                    self.turn_the_perspective(rotation / 10, **kwargs)
            if event.type == game.QUIT:
                game.quit()
                quit()

            if event.type == KEYDOWN:
                game.quit()
                quit()
        ...

    def turn_the_perspective(self, rotation, **kwargs):
        "转动视角事件"
        rotation = list(reversed(rotation))

        self.player.camera.pitch = self.player.camera.pitch - rotation[0] # 减是因为上下颠倒
        self.player.camera.yaw = self.player.camera.yaw + rotation[1]

        pitch_rad, yaw_rad = np.deg2rad([self.player.camera.pitch, self.player.camera.yaw])

        self.player.camera.look_at[0] = np.sin(yaw_rad) * np.cos(pitch_rad)
        self.player.camera.look_at[1] = np.sin(pitch_rad)
        self.player.camera.look_at[2] = -np.cos(yaw_rad) * np.cos(pitch_rad)

        game.mouse.set_pos(self.center_pos)

    def forward(self, amount, **kwargs):
        ...
        