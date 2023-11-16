from engine.game import Game
from engine import gaming
from const import *




def main():
    GAME = Game() # 创建游戏实例
    GAME.resource_path = RESOURCEPATH
    GAME.init()  # 初始化游戏
    GAME.start() # 开始游戏



if __name__ == "__main__":
    main()

