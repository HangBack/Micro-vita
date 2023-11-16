from engine.game import Game
from engine import gaming
from test import test




def main():
    GAME = Game() # 创建游戏实例
    GAME.user = gaming.entities.player.Player('resources/player/test')
    GAME.add_scene(test)
    GAME.init()  # 初始化游戏
    GAME.start() # 开始游戏



if __name__ == "__main__":
    main()

