import abc
from engine.const import *



def __import():
    global Model, Scene, ShaderProgram
    from modules.model import Model
    from gaming.scene import Scene
    from OpenGL.GL.shaders import ShaderProgram
    

class Material:

    def __init__(self, **kwargs) -> None:
        self.diffuse = getvalue(kwargs, "diffuse") # 漫反射颜色
        self.specular = getvalue(kwargs, "specular") # 高光反射颜色

    @property
    def diffuse(self):
        return self._diffuse
    
    @diffuse.setter
    def diffuse(self, value):
        if value is True:
            self._diffuse = np.ones(3, dtype=np.float32)
        else:
            self._diffuse = np.array(value, dtype=np.float32)

    @property
    def specular(self):
        return self._specular
    
    @specular.setter
    def specular(self, value):
        if value is True:
            self._specular = np.ones(3, dtype=np.float32)
        else:
            self._specular = np.array(value, dtype=np.float32)
                                      

class Model(metaclass=abc.ABCMeta):

    shader: os.PathLike
        
    @abc.abstractmethod
    def modelType(self):
        "模型类型，决定模型的优先级"
        ...

    def __init__(self, **kwargs):
        self.vertices: 'np.ndarray'
        self.indices: 'np.ndarray'
        self.colors: 'np.ndarray'

        
        self._texture: Material = Material(**kwargs)                 # 模型纹理


        self._position: 'np.ndarray' = np.zeros(3, dtype=np.float32) # 模型位置
        self._center: 'np.ndarray' = np.zeros(3, dtype=np.float32)   # 模型中心点
        self._scale: 'np.ndarray' = np.ones(3, dtype=np.float32)     # 模型缩放率
        
    
    def __lt__(self, other):
        if hasattr(other, 'modelType'):
            if self.modelType < self.modelType:
                return (self.position < other.position).all() # 判断坐标，xyz小的的优先
            else:
                return False

    def update(self):
        self.load()

    def move(self, x: float | int, y: float | int, z: float | int):
        self.position += np.array([x, y, z], dtype=np.float32)

    def rotate(self, x: float | int = 0, y: float | int = 0, z: float | int = 0):
        for v in self.vertices:
            if x:
                rotate_vector((1, 0, 0), v, deg=x)
            if y:
                rotate_vector((0, 1, 0), v, deg=y)
            if z:
                rotate_vector((0, 0, 1), v, deg=z)

    def bind_scene(self, scene: 'Scene'):
        "绑定场景实例"
        self.scene = scene
        return self
        
    @property
    def model_matrix(self):
        "模型矩阵"
        return self._model_matrix

    @model_matrix.setter
    def model_matrix(self, value):
        self._model_matrix = np.array(value, dtype=np.float32)


    @property
    def position(self):
        "位置"
        return self._position

    @position.setter
    def position(self, value):
        self._position = np.array(value, dtype=np.float32)

    @property
    def translation(self):
        "当前位移"
        return self._translation
    
    @translation.setter
    def translation(self, value):
        self._translation = np.array(value, dtype=np.float32)
        self.position = self.position + self._translation

    @property
    def scale(self):
        "缩放率"
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value

    @property
    def pitch(self):
        "仰俯角"
        return self._pitch

    @pitch.setter
    def pitch(self, value):
        self._pitch = value



def getvalue(data: dict, key: str) -> bool:
    if key in data.keys():
        return data[key]
    else:
        return True