import gaming
from game import Game
from test import test




def main():
    GAME = Game() # 创建游戏实例
    GAME.user = gaming.entity.player.Player('resources/player/test')
    GAME.init(test) # 初始化游戏
    GAME.start() # 开始游戏



if __name__ == "__main__":
    main()