from const import *
from test import test



# 初始化
game.init()
display = game.display.set_mode(
    const.display, 
    DOUBLEBUF|OPENGL|FULLSCREEN,
)
SCREEN_W, SCREEN_H = display.get_rect()[2:]
game.display.set_caption(const.caption)
gluPerspective(const.fovy, (SCREEN_W / SCREEN_H), const.zNear, const.zFar)
glTranslatef(0.0, 0.0, 0.0)
glCullFace(GL_BACK)
glEnable(GL_DEPTH_TEST)



def update_display():
    game.display.flip()
    game.time.wait(10)

def main():
    # 游戏过程
    while True:

        cubes = test()
        for event in const.events:
            event_arguments = {
                "pygame_events": game.event.get(),
                "screen_width": SCREEN_W,
                "screen_height": SCREEN_H
            }
            event.trigger(**event_arguments)
        
        
        # 重置画面
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for cube in cubes:
            cube.draw()
        
        
        

        # 刷新画面
        update_display()

if __name__ == "__main__":
    main()