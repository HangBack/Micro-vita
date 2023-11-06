from const import *
import modules as config
from test import test

class Game:

    def __import(self):
        global gaming
        import gaming

    def __init__(self) -> None:
        game.init()
        self.window = game.display.set_mode(
            const.display, 
            DOUBLEBUF|OPENGL|FULLSCREEN,
        )
        self.SCREEN_W, self.SCREEN_H = self.window.get_rect()[2:]
        game.display.set_caption(const.caption)
        self.players: list['gaming.entity.player.Player'] = []
        self.events: list['gaming.event.Event'] = []
        self.cyclers: Sequence = []
        self._user: 'gaming.entity.player.Player'
        self.center_pos = self.SCREEN_W / 2, self.SCREEN_H / 2

    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, value):
        self._user = value

    def init(self):
        glCullFace(GL_BACK)
        glEnable(GL_DEPTH_TEST) # 启用深度测试
        game.key.set_repeat(10, 15)

    def start(self):
        cubes = test()
        while True:

            # 事件
            for event in self.events:
                event.trigger()



            # 重置画布
            self.reset_canvas()

            # 循环事件部分
            for cycler in self.cyclers:
                cycler()
            for cube in cubes:
                cube.draw()
            
            

            # 更新画面
            self.update_display()


    def add_player(self, player: 'gaming.entity.player.Player'):
        self.players.append(player) # 玩家加入游戏
        self.cyclers.append(player.run) # 将玩家循环添加到游戏中

    def add_event(self, event: 'gaming.event.Event'):
        self.events.append(event)
        return event

    def change_scene(self):
        ...

    def reset_canvas(self):
        "重置画布"
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluPerspective(const.fovy, (self.SCREEN_W / self.SCREEN_H), const.zNear, const.zFar)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    def update_display(self):
        "更新画布"
        game.display.flip()
        game.time.wait(10) # 更新频率