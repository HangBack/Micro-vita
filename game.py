from const import *
import modules as config


class Game:

    def __import(self):
        global gaming
        import gaming

    def __init__(self) -> None:
        game.init()
        self.window = game.display.set_mode(
            const.DISPLAY,
            DOUBLEBUF | OPENGL | FULLSCREEN,
        )
        self.SCREEN_W, self.SCREEN_H = self.window.get_rect()[2:]
        game.display.set_caption(const.CAPTION)
        self.players: list['gaming.entity.player.Player'] = []
        self.events: list['gaming.event.Event'] = []
        self.cyclers: list = []
        self._user: 'gaming.entity.player.Player'
        self.center_pos = self.SCREEN_W / 2, self.SCREEN_H / 2
        self._tick = 10

    @property
    def user(self) -> 'gaming.entity.player.Player':
        return self._user

    @user.setter
    def user(self, value):
        if hasattr(self, '_user'):
            self.players.remove(self._user)
            del self._user
        self._user = value
        self.add_player(self._user)

    def init(self, scene: 'gaming.scene.Scene'):
        self.projection = pyrr.matrix44.create_perspective_projection_matrix(const.FOVY, self.SCREEN_W / self.SCREEN_H, const.ZNEAR, const.ZFAR)
        self._scene = scene.bind_game(self).init()
        self._tick_iter = self._tick
        glCullFace(GL_BACK)
        glEnable(GL_DEPTH_TEST)  # 启用深度测试
        game.key.set_repeat(10, 15)

    @property
    def tick(self) -> bool:
        self._tick_iter -= 1
        if self._tick_iter == 0:
            self._tick_iter = self._tick
            return True
        else:
            return False

    def start(self) -> NoReturn:
        while True:

            # 重置画布
            self.reset_canvas()

            # 循环部分
            for cycler in self.cyclers:
                # 事件
                for event in self.events:
                    event.trigger(self.tick)
                cycler()

            # 绘制场景
            self._scene.draw()

            # 更新画面
            self.update_display()

    def add_player(self, player: 'gaming.entity.player.Player') -> 'gaming.entity.player.Player':
        self.players.append(player)  # 玩家加入游戏
        self.cyclers.append(player.run)  # 将玩家循环添加到游戏中
        return player

    def add_event(self, event: 'gaming.event.Event') -> 'gaming.event.Event':
        event.bind_game(self)
        self.events.append(event)
        return event

    @property
    def scene(self) -> 'gaming.scene.Scene':
        return self._scene

    @scene.setter
    def scene(self, scene: 'gaming.scene.Scene'):
        self.init(scene)
        self._scene = scene

    def reset_canvas(self) -> None:
        "重置画布"
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def update_display(self) -> None:
        "更新画布"
        game.display.flip()
        game.time.wait(10)  # 更新频率
