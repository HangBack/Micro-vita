from const import *
import modules as config


def __import(self):
    global gaming
    import gaming

class Game:

    def __init__(self) -> None:
        game.init()
        self.__scene: 'gaming.scene.Scene'
        flags = DOUBLEBUF | OPENGL | FULLSCREEN
        self.DISPLAY = (0, 0)
        self.window = game.display.set_mode(self.DISPLAY, flags) # 游戏窗口
        self._SCREEN_W = self.window.get_width() # 游戏窗口宽度
        self._SCREEN_H = self.window.get_height() # 游戏窗口高度
        self._ASPECT = self.SCREEN_W / self.SCREEN_H # 游戏窗口宽高比
        self._center_pos = self.SCREEN_W / 2, self.SCREEN_H / 2 # 游戏窗口中心坐标
        self._ZNEAR: float = .0005
        self._ZFAR: float = 2000.0

        
        self._tick: int = 10


        game.display.set_caption(const.CAPTION) # 游戏标题

        self.events: _Events = _Events([]) # 游戏事件列表
        self.cyclers: _Cyclers = _Cyclers([]) # 循环任务列表
        self.players: _Players = _Players([]) # 玩家列表


        self._user: 'gaming.entity.player.Player' # 用户玩家

    
    @property
    def SCREEN_W(self):
        return self._SCREEN_W

    @property
    def SCREEN_H(self):
        return self._SCREEN_H

    @property
    def ASPECT(self):
        return self._ASPECT

    @property
    def center_pos(self):
        return self._center_pos

    @property
    def tick(self):
        return self._tick
        

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

    def init(self, scene: 'gaming.scene.Scene', **kwargs):
        if not hasattr(self, '_user'):
            raise ValueError('初始化游戏之前必须指定一名用户玩家')
        
        
        # 投影
        self.projection = pyrr\
            .matrix44\
                .create_perspective_projection_matrix(
                    self.user.settings.video.fovy, 
                    self._ASPECT, 
                    self._ZNEAR, 
                    self._ZFAR
                )
        self.__scene = scene(self).bind_game(self).init()
        self._tick_iter = self._tick
        glCullFace(GL_BACK)
        glEnable(GL_DEPTH_TEST)  # 启用深度测试
        game.key.set_repeat(10, 15) # 按键重复

    @property
    def tick(self) -> bool:
        self._tick_iter -= 1
        if self._tick_iter == 0:
            self._tick_iter = self._tick
            return True
        else:
            return False

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
        return self.__scene

    @scene.setter
    def scene(self, scene: 'gaming.scene.Scene'):
        self.init(scene)
        self.__scene = scene

    def __reset_canvas(self) -> None:
        "重置画布"
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def __update_display(self) -> None:
        "更新画布"
        game.display.flip()
        game.time.wait(10)  # 更新频率







    """每个游戏实例都必须通过start方法开始游戏"""
    def start(self) -> NoReturn:
        "游戏开始"
        while True:
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






class _Players(object):

    def __init__(self, players: list['gaming.entity.player.Player']) -> None:
        self.__players = players
        pass

    def __iter__(self):
        for player in self.__players:
            yield player

    def append(self, __object: 'gaming.entity.player.Player'):
        self.__players.append(__object)


class _Events(object):

    def __init__(self, events: list['gaming.event.Event']) -> None:
        self.__events = events
        pass

    def __iter__(self):
        for event in self.__events:
            yield event

    def append(self, __object: 'gaming.event.Event'):
        self.__events.append(__object)


class _Cyclers(object):

    def __init__(self, cyclers: list['Callable']) -> None:
        self.__cyclers = cyclers
        pass

    def __iter__(self):
        for cycler in self.__cyclers:
            yield cycler

    def append(self, __object: 'Callable'):
        self.__cyclers.append(__object)