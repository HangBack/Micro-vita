from engine.gaming.event import Event as parent
from engine.const import *

import uuid

def __import():
    global gaming
    import gaming

class Event(parent):

    def __init__(self) -> None:
        self.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, 'micro_vita') # 生成UUID
        self.player: 'gaming.entities.player.Player'
        self.tasks: dict[str, 'Callable'] = {}
        
    def init(self):
        "初始化"
        if not hasattr(self, 'player'):
            raise ValueError("无法在绑定玩家前完成初始化")
        self._move_forward = game.event.Event(
            USEREVENT,
            {
                'source': self.player.uuid,
                'callback': self.player.move_forward
            }
        )
        
        self._move_backward = game.event.Event(
            USEREVENT,
            {
                'source': self.player.uuid,
                'callback': self.player.move_backward
            }
        )
        
        self._move_left = game.event.Event(
            USEREVENT,
            {
                'source': self.player.uuid,
                'callback': self.player.move_left
            }
        )
        
        self._move_right = game.event.Event(
            USEREVENT,
            {
                'source': self.player.uuid,
                'callback': self.player.move_right
            }
        )
        
        self._move_up = game.event.Event(
            USEREVENT,
            {
                'source': self.player.uuid,
                'callback': self.player.move_up
            }
        )
        
        self._move_down = game.event.Event(
            USEREVENT,
            {
                'source': self.player.uuid,
                'callback': self.player.move_down
            }
        )
        
        self._turn_the_perspective = game.event.Event(
            USEREVENT,
            {
                'source': self.player.uuid,
                'callback': self.player.turn_the_perspective
            }
        )

    @property
    def move_forward(self):
        "前进事件"
        return self._move_forward

    @property
    def move_backward(self):
        "后退事件"
        return self._move_backward

    @property
    def move_left(self):
        "左移事件"
        return self._move_left

    @property
    def move_right(self):
        "右移事件"
        return self._move_right

    @property
    def move_up(self):
        "左移事件"
        return self._move_up

    @property
    def move_down(self):
        "右移事件"
        return self._move_down

    @property
    def turn_the_perspective(self):
        "视角转动事件"
        return self._turn_the_perspective

    def trigger(self) -> None:

        for task in self.tasks.values():
            task() # 执行任务
        if self.game.user.uuid == self.player.uuid:
            for event in game.event.get():
                
                if event.type == USEREVENT:
                    
                    if event.target == self.uuid:
                        event.callback()
                            
                if event.type == MOUSEMOTION:
                    game.mouse.set_visible(False)
                    rotation = np.array(event.rel)
                    if not (rotation == np.array([0, 0])).all():
                        self.player.turn_the_perspective(rotation / 10)


            # 控制模块
            keys = game.key.get_pressed()
            for key, value in self.player.settings.control.mapping.items():
                if keys[value]:
                    event: Event.__actionEvent = getattr(self, key)
                    event.callback()


    def bind_player(self, player: 'gaming.entities.player.Player') -> None:
        self.player = player
        return None
    
    class __actionEvent:

        source: uuid.UUID

        @classmethod
        def callback() -> Any: ...