from .._event import Event as parent
from ..entity.player import Player
from ._const import *
class Event(parent):

    def __init__(self, player: Player, **kwargs) -> None:
        self.player = player
        pass

    def trigger(self, **kwargs):
        self.center_pos = np.array([kwargs["screen_width"] / 2, kwargs["screen_height"] / 2])
        for event in kwargs["pygame_events"]:
            if event.type == MOUSEMOTION:
                self.rotation = np.array(event.rel)
                if not (self.rotation == np.array([0, 0])).all():
                    self.turn_the_perspective(const._UNIT(self.rotation), **kwargs)
            if event.type == game.QUIT:
                game.quit()
                quit()

            if event.type == KEYDOWN:
                game.quit()
                quit()
        ...

    def turn_the_perspective(self, rotation, **kwargs):
        "转动视角事件"
        self.player.settings.controls.Sensitivity
        self.player.rotation += np.array([*rotation, 0])
        x_deg, y_deg, _ = self.Player.rotation
        x_rad, y_rad = np.deg2rad([x_deg, y_deg])
        game.mouse.set_pos(self.center_pos)
        