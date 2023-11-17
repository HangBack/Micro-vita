from engine.game import Game
from const import *




def main():
    GAME = Game() # 创建游戏实例
    GAME.init( # 初始化游戏
        resource_path = RESOURCEPATH # 资源路径
    )
    GAME.start() # 开始游戏



if __name__ == "__main__":
    main()

