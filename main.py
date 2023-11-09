
import gaming
from game import Game
from const import *
from test import scene




def main():
    GAME = Game() # 创建游戏实例
    GAME.user = gaming.entity.player.Player('resources/player/test')
    GAME.add_event(gaming.events.player.Event())
    GAME.init(scene) # 初始化游戏
    GAME.start() # 开始游戏



if __name__ == "__main__":
    main()