from engine.const import *
from ..model import Model

class Cube(Model):

    shader = const.SHADER_PATH(__name__, 'cube')

    def __init__(
        self,
        length: int | float,
        width: int | float,
        height: int | float,
        texture: str | None = None,
        colors: Sequence[int | float] = (1, 1, 1, 1),
        position: Sequence[int | float] = (0, 0, 0),
        mode: str = 'solid'
    ) -> None:
        super().__init__(position=position)
        """
        立方体
        """
        # 大小矢量
        self.scale = np.array([length, width, height], dtype=np.float32)
        # 单位立方体顶点
        self.vertices = np.array([
            [-0.5, -0.5, -0.5], # 0
            [+0.5, -0.5, -0.5], # 1
            [+0.5, +0.5, -0.5], # 2
            [-0.5, +0.5, -0.5], # 3
            [-0.5, -0.5, +0.5], # 4
            [+0.5, -0.5, +0.5], # 5
            [+0.5, +0.5, +0.5], # 6
            [-0.5, +0.5, +0.5]  # 7
        ], dtype=np.float32)
        self.indices = np.array([
            0, 1, 2, 0, 3, 2, # 前面
            4, 5, 6, 4, 7, 6, # 后面
            0, 4, 7, 0, 3, 7, # 左面
            1, 5, 6, 1, 2, 6, # 右面
            0, 4, 5, 0, 1, 5, # 上面
            3, 7, 6, 3, 2, 6  # 下面
        ], dtype=np.uint32)
        """
        立方体索引
            4-------5
           /|      /|
          / |     / |
         /  7----/--6
        0--/----1  /
        | /     | /
        |/      |/
        3-------2
        
        """
        # 满足颜色需求
        self.colors = colors
        self.texture = texture
        self.mode = mode

    def export(self, path: str | os.PathLike = None, mode: str = 'get') -> str | None:
        data = {}
        keys = get_attributes(self)
        for key in keys:
            value = getattr(self, key)
            if isinstance(value, np.ndarray):
                value = value.tolist()
            data.__setitem__(key, value)
        # 模式判断
        if path is None and mode == 'get': # 模式为get时返回字典数据
            return data
        elif mode == 'file':
            if path is None:
                raise ValueError('使用file模式时必须指定一个文件路径')
            with open(path, 'w+') as file:
                json.dump(data)
            file.close()
        else:
            raise ValueError('path不能在mode为get时传入值')

    @property
    def modelType(self):
        "模型权重：0"
        return 0