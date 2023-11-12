from engine.const import *


def __import():
    global gaming
    import gaming


class Game:

    __Players = NewType('Players', list['gaming.entity.player.Player'])  # 玩家容器
    __Cyclers = NewType('Cyclers', list['Callable'])                    # 循环容器
    __Events = NewType('Events',   list['gaming.event.Event'])          # 事件容器
    __Scenes = NewType('Scenes',   list['gaming.scene.Scene'])          # 场景容器

    def __init__(self) -> None:
        game.init()  # 初始化pygame

        "类型声明"
        self.__scene: 'gaming.scene.Scene'           # 游戏场景
        self._user:   'gaming.entity.player.Player'  # 用户玩家

        "初始化属性"
        self._DISPLAY = (0, 0)                                    # 窗口尺寸
        flags = DOUBLEBUF | OPENGL | FULLSCREEN                   # 窗口属性
        self.window = game.display.set_mode(self._DISPLAY, flags)  # 游戏窗口

        self._SCREEN_W = self.window.get_width()   # 游戏窗口宽度
        self._SCREEN_H = self.window.get_height()  # 游戏窗口高度

        self._center_pos = self.SCREEN_W / 2, self.SCREEN_H / 2  # 游戏窗口中心坐标
        self._ASPECT = self.SCREEN_W / self.SCREEN_H             # 游戏窗口宽高比

        self._ZNEAR: float = .000_5  # 近平面
        self._ZFAR:  float = 2_000.  # 远平面
        self._FOVY:  float = 75.     # 视野

        self._tick: int = 10  # 游戏刻

        game.display.set_caption(const.CAPTION)  # 游戏标题

        self.cyclers: Game.__Cyclers = Game.__Cyclers([])  # 循环列表
        self.players: Game.__Players = Game.__Players([])  # 玩家列表
        self.events: Game.__Events = Game.__Events([])     # 事件列表
        self.scenes: Game.__Scenes = Game.__Scenes([])     # 场景列表

    """
    游戏属性
    """

    # ---- 窗口相关

    @property
    def SCREEN_W(self) -> int:                    # 窗口宽度
        return self._SCREEN_W

    @SCREEN_W.setter
    def SCREEN_W(self, value):
        self._SCREEN_W = value

    # ----

    @property
    def SCREEN_H(self) -> int:                    # 窗口高度
        return self._SCREEN_H

    @SCREEN_H.setter
    def SCREEN_H(self, value):
        self._SCREEN_H = value

    # ----

    @property
    def ASPECT(self) -> float:                    # 窗口屏占比
        return self._ASPECT

    @ASPECT.setter
    def ASPECT(self, value):
        self._ASPECT = value
        self.projection = True

    # ----

    @property
    def center_pos(self) -> tuple[float, float]:  # 窗口中心坐标
        return self._center_pos

    @center_pos.setter
    def center_pos(self, value):
        self._center_pos = value

    # ---- 用户视野相关

    @property
    def ZNEAR(self) -> float:  # 视野远平面
        return self._ZNEAR

    @ZNEAR.setter
    def ZNEAR(self, value):
        self._ZNEAR = value
        self.projection = True

    # ----

    @property
    def ZFAR(self) -> float:   # 视野近平面
        return self._ZFAR

    @ZFAR.setter
    def ZFAR(self, value):
        self._ZFAR = value
        self.projection = True

    # ----

    @property
    def FOVY(self) -> float:   # 视野
        return self._FOVY

    @FOVY.setter
    def FOVY(self, value):
        self._FOVY = value
        self.projection = True

    # ----

    @property
    def projection(self) -> pyrr.Matrix44:
        return self._projection

    @projection.setter
    def projection(self, value):
        if value is True:
            self._projection = pyrr\
                .matrix44\
                .create_perspective_projection_matrix(
                    self._FOVY,
                    self._ASPECT,
                    self._ZNEAR,
                    self._ZFAR
                )
        else:
            raise ValueError('投影不可直接修改。')

    # ---- 游戏进程相关

    @property
    def tick(self) -> int:  # 游戏tick
        return self._tick

    @tick.setter
    def tick(self, value):
        self._tick = value

    # ---- 操作用户相关

    @property
    def user(self) -> 'gaming.entity.player.Player':  # 用户
        return self._user

    @user.setter
    def user(self, value: 'gaming.entity.player.Player'):
        if hasattr(self, '_user'):
            self.players.remove(self._user)
            del self._user
        self._user = value
        self._user.bind_game(self)

    # ---- 游戏场景相关

    @property
    def scene(self) -> 'gaming.scene.Scene':
        return self.__scene

    @scene.setter
    def scene(self, scene: 'gaming.scene.Scene'):
        self.init(scene)
        self.__scene = scene

    """
    游戏进程
    """

    def init(self, **kwargs):
        """
        初始化游戏

        `每个游戏实例都必须通过init方法初始化游戏`
        """
        logging.info("游戏初始化")
        if not hasattr(self, '_user'):
            raise ValueError('初始化游戏之前必须指定一名用户玩家')

        # 投影
        self.FOVY = self.user.settings.video.fovy  # 视野更改
        self._projection = pyrr\
            .matrix44\
            .create_perspective_projection_matrix(
                self._FOVY,
                self._ASPECT,
                self._ZNEAR,
                self._ZFAR
            )
        self.__scene = self.scenes[0]  # 场景绑定并初始化
        self._tick_iter = self._tick  # 游戏tick迭代

        glCullFace(GL_BACK)          # 剔除背面
        glEnable(GL_DEPTH_TEST)      # 启用深度测试
        game.key.set_repeat(10, 15)  # 按键重复

        self.__main_cycler = True    # 允许主游戏循环

    def start(self) -> NoReturn:
        """
        开始游戏

        `每个游戏实例都必须通过start方法开始游戏`
        """
        logging.info("游戏开始")
        while self.__main_cycler:
            "主循环"
            # 重置画布
            self.__reset_canvas()

            # 循环部分
            for cycler in self.cyclers:
                # 事件
                for event in self.events:
                    event.trigger(self.tick)
                cycler()

            # 绘制场景
            self.__scene.draw()

            # 更新画面
            self.__update_display()

    def end(self):
        """
        结束游戏

        `每个游戏实例都必须通过end方法结束游戏`
        """
        self.__main_cycler = False   # 终止主游戏循环
        self.save()  # 自动保存
        game.quit()
        logging.info("游戏结束")
        quit()

    def save(self, archive_path: os.PathLike = 'Default') -> None:
        "保存游戏"
        logging.info("保存游戏中...")

    def add_player(     # 加入玩家
            self,
            player: 'gaming.entity.player.Player'
    ) -> 'gaming.entity.player.Player':

        self.players.append(player)
        return player

    def add_event(      # 加入事件
            self,
            event: 'gaming.event.Event'
    ) -> 'gaming.event.Event':

        self.events.append(event)
        return event

    def add_cycler(     # 加入循环
            self,
            cycler: 'Callable'
    ) -> 'Callable':

        self.cyclers.append(cycler)
        return cycler

    def add_scene(      # 加入场景
            self,
            scene: 'gaming.scene.Scene'
    ) -> 'gaming.scene.Scene':
        if callable(scene):
            scene = scene()
        scene.bind_game(self).init()
        self.scenes.append(scene)
        return scene

    """
    功能方法
    """

    def __reset_canvas(self) -> None:
        "重置画布"
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def __update_display(self) -> None:
        "更新画布"
        game.display.flip()
        game.time.wait(10)  # 更新频率
