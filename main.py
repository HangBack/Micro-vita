from const import *
from test import test
import gaming


# 初始化
game.init()
display = game.display.set_mode(
    const.display, 
    DOUBLEBUF|OPENGL|FULLSCREEN,
)
SCREEN_W, SCREEN_H = display.get_rect()[2:]
game.display.set_caption(const.caption)
glCullFace(GL_BACK)
glEnable(GL_DEPTH_TEST)
game.key.set_repeat(10, 15)


player = gaming.entity.player.Player('resources/player/test')
events = [
    gaming.events.player.Event(player)
]
game.mouse.set_visible(False)

def reset_canvas():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluPerspective(const.fovy, (SCREEN_W / SCREEN_H), const.zNear, const.zFar)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

def update_display():
    game.display.flip()
    game.time.wait(10) # 更新频率

cyclers = [
    player.run
]

def main():
    # 游戏过程
    cubes = test()
    while True:
        for event in events:
            event_arguments = {
                "pygame_events": game.event.get(),
                "screen_width": SCREEN_W,
                "screen_height": SCREEN_H
            }
            event.trigger(**event_arguments)
        
        
        # 重置画布
        reset_canvas()

        # 循环事件部分
        for cycler in cyclers:
            cycler()
        for cube in cubes:
            cube.draw()
        
        

        # 更新画面
        update_display()

if __name__ == "__main__":
    main()