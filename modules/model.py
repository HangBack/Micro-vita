import abc
from const import *

class Model(metaclass=abc.ABCMeta):

    shader: os.PathLike

    def __import(self):
        global Model, Scene, ShaderProgram
        from modules.model import Model
        from gaming.scene import Scene
        from OpenGL.GL.shaders import ShaderProgram

    class Material:

        def __init__(self, **kwargs) -> None:
            self.diffuse = kwargs["diffuse"] # 漫反射颜色
            self.specular = kwargs["specular"] # 高光反射颜色
        
    @abc.abstractmethod
    def draw(self):
        "绘制模型"
        ...
        
    @abc.abstractmethod
    def modelType(self):
        "模型类型，决定模型的优先级"
        ...

    def __init__(self):
        self.vertices: 'np.ndarray'
        self._position: 'np.ndarray' = np.zeros(3, dtype=np.float32)
        self._scale: 'np.ndarray' = np.array([1., 1., 1.], dtype=np.float32)
        self._color: 'np.ndarray' = np.zeros(3, dtype=np.float32)
        
    
    def __lt__(self, other):
        if hasattr(other, 'modelType'):
            if self.modelType < self.modelType:
                return True
            else:
                return False

    def update(self):
        self.load()

    def move(self, x: float | int, y: float | int, z: float | int):
        self.position += np.array([x, y, z], dtype=np.float32)

    def rotate(self, x: float | int = None, y: float | int = None, z: float | int = None):
        for v in self.vertices:
            if x is not None:
                rotate_vector((1, 0, 0), v, deg=x)
            if y is not None:
                rotate_vector((0, 1, 0), v, deg=y)
            if z is not None:
                rotate_vector((0, 0, 1), v, deg=z)

    def bind_scene(self, scene: 'Scene'):
        "绑定场景实例"
        self.scene = scene
        return self
        
    @property
    def view_matrix(self):
        return self._view_matrix

    @view_matrix.setter
    def view_matrix(self, value):
        self._view_matrix = np.array(value, dtype=np.float32)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = np.array(value, dtype=np.float32)

    @property
    def translation(self):
        return self._translation
    
    @translation.setter
    def translation(self, value):
        self._translation = np.array(value, dtype=np.float32)
        self.position = self.position + self._translation

    @property
    def pitch(self):
        return self._pitch

    @pitch.setter
    def pitch(self, value):
        self._pitch = value

    def __x_rotation(self):
        return

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value