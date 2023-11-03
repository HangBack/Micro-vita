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
gluPerspective(const.fovy, (const.aspect), const.zNear, const.zFar)
glTranslatef(0.0, 0.0, -7)
glCullFace(GL_BACK)
glEnable(GL_DEPTH_TEST)



def update_display():
    game.display.flip()
    game.time.wait(10)

def main():
    # 游戏过程
    while True:
        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                quit()

            if event.type == KEYDOWN:
                key = game.key.get_pressed()
                match key:
                    case K_ESCAPE:
                        game.quit()
                        quit()
        
        
        
        # 重置画面
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        for event in const.events:
            event_arguments = {
                "rotation": np.array(
                    game.mouse.get_pos()
                )
            }
            event.trigger(**event_arguments)

        for cube in test():
            cube.draw()
        
        
        

        # 刷新画面
        update_display()

if __name__ == "__main__":
    main()