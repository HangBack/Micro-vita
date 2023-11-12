from engine.const import *
from .. import model
import time



class cube(model.Model):

    shader = const.SHADER_PATH(__name__, 'cube')

    def __init__(
        self,
        length: int | float,
        width: int | float,
        height: int | float,
        texture: ImageObject.Image | None = None,
        colors: Sequence[Sequence[int | float]] |
        Sequence[int | float] = (1, 1, 1),
        mode: str = 'solid'
    ) -> None:
        super().__init__()
        """
        Regular hexahadron
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
        矩阵索引
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

    @property
    def modelType(self):
        "cube优先级：0"
        return 0
    



class sphere(model.Model):

    def __get_vertices(self, mode, slices=25, stacks=25):
        slices = clamp_number(int(math.ceil(slices)), 25, const.INFINITY)
        stacks = clamp_number(int(math.ceil(stacks)), 25, const.INFINITY)

        vertices = [
            (
                math.sin(math.pi * i / slices) *
                math.cos(math.pi * 2.0 * j / stacks),
                math.cos(math.pi * i / slices),
                math.sin(math.pi * i / slices) *
                math.sin(math.pi * 2.0 * j / stacks)
            )
            for i in range(slices + 1)
            for j in range(stacks + 1)
        ]

        return np.array(vertices, float)

    def __init__(self, center: Sequence, radius: float | int, amount: int = 50, texture=(1, 1, 1), mode: str = 'solid', **kwargs) -> None:
        self.center = center
        self.vertices = self.__get_vertices(
            mode, amount, amount) * float(radius) + self.center
        self.textrue = [texture for _ in range(len(self.vertices))]
        self.mode = mode
        super().__init__()

    def init(self):
        "预加载"

    def load(self):
        "加载"

    def draw(self):
        ...

    def update(self):
        ...

    @property
    def modelType(self):
        "cube优先级：1"
        return 1
    

def vertice_norm(vertices: list[list[float | int]], colors):
    vertices = [list(vertice) for vertice in vertices]
    result: np.ndarray[np.float32] = np.array([
        # [[coordinate + rgb]...] -> [[*coordinate, *rgb]...]
        tuple(coordinate + list(colors[i]))
        for i, coordinate in enumerate(vertices)
    ], dtype=np.float32)
    return result