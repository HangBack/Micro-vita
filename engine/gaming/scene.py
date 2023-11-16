from engine.const import *


def __import():
    global Model, Game
    from modules.model import Model
    from game import Game


class Scene:

    def __init__(self, models: list['Model'] | Callable) -> None:
        if callable(models):
            models: list['Model'] = models()
        self._VBO: list = []  # 顶点缓冲对象
        self._EBO: list = []  # 元素缓冲对象
        self._IBO: list = []  # 实例缓冲对象
        self.__models = models
        self.__flattened_models = models.sort()
        self._position = np.zeros(3, dtype=np.float32)
        self._rotation = np.zeros(3, dtype=np.float32)
        self._scale = np.ones(3, dtype=np.float32)
        pass

    def init(self):
        self.models = Scene.multiModels(self.__models)
        for _ in self.models:
            self._VBO.append(glGenBuffers(1))
            self._EBO.append(glGenBuffers(1))
            self._IBO.append(glGenBuffers(1))
        self.load()
        return self

    def load(self):
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)
        for i in range(len(self._VBO)):
            VBO = self._VBO[i]
            EBO = self._EBO[i]
            IBO = self._IBO[i]
            model = self.models.__getitem__(0)
            glBindBuffer(GL_ARRAY_BUFFER, VBO)
            glBufferData(GL_ARRAY_BUFFER, model.vertices.nbytes,
                         model.vertices, GL_STATIC_DRAW)  # 顶点缓冲

            glBindBuffer(GL_ARRAY_BUFFER, IBO)
            glBufferData(GL_ARRAY_BUFFER, model.positions.nbytes + model.scales.nbytes + model.colors.nbytes,
                         None, GL_STATIC_DRAW)           # 实例缓冲
            glBufferSubData(GL_ARRAY_BUFFER,  # 位置属性
                            0,
                            model.positions.nbytes,
                            model.positions)
            glBufferSubData(GL_ARRAY_BUFFER,  # 缩放属性
                            model.positions.nbytes,
                            model.scales.nbytes,
                            model.scales)
            glBufferSubData(GL_ARRAY_BUFFER,  # 颜色属性
                            model.positions.nbytes + model.scales.nbytes,
                            model.colors.nbytes,
                            model.colors)

            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, model.indices.nbytes,
                         model.indices, GL_STATIC_DRAW)  # 索引缓冲

            glUseProgram(model.shader)

            glBindBuffer(GL_ARRAY_BUFFER, VBO)
            glEnableVertexAttribArray(0)  # 顶点
            glVertexAttribPointer(0, model.vertices.shape[1], GL_FLOAT,
                                  GL_FALSE, model.vertices[0].nbytes, ctypes.c_void_p(0))
            glEnableVertexAttribArray(4)  # 纹理坐标
            glVertexAttribPointer(4, model.vertices.shape[1], GL_FLOAT,
                                  GL_FALSE, model.vertices[0].nbytes, ctypes.c_void_p(0))

            # 实例
            glBindBuffer(GL_ARRAY_BUFFER, IBO)
            # ---
            glEnableVertexAttribArray(1)  # 位置
            glVertexAttribPointer(1, model.positions.shape[1], GL_FLOAT,
                                  GL_FALSE, model.positions[0].nbytes, ctypes.c_void_p(0))
            glVertexAttribDivisor(1, 1)

            glEnableVertexAttribArray(2)  # 缩放
            glVertexAttribPointer(2, model.scales.shape[1], GL_FLOAT,
                                  GL_FALSE, model.scales[0].nbytes, ctypes.c_void_p(model.positions.nbytes))
            glVertexAttribDivisor(2, 1)

            glEnableVertexAttribArray(3)  # 色彩
            glVertexAttribPointer(3, model.colors.shape[1], GL_FLOAT,
                                  GL_FALSE, model.colors[0].nbytes, ctypes.c_void_p(model.positions.nbytes + model.scales.nbytes))
            glVertexAttribDivisor(3, 1)
            # ---

            # 纹理坐标
            # glEnableVertexAttribArray(4)
            # glVertexAttribPointer(4, model.textures.shape[1], GL_FLOAT,
            #                     GL_FALSE, model.textures[0].nbytes * 8, ctypes.c_void_p(model.vertices.nbytes + model.positions.nbytes + model.scales.nbytes + model.colors.nbytes))
            # glVertexAttribDivisor(4, 1)

            glBindBuffer(GL_ARRAY_BUFFER, 0)         # 取消绑定（规范）
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)  # 取消绑定（规范）
            glUseProgram(0)
        glBindVertexArray(0)
        return self

    def draw(self):
        glBindVertexArray(self.VAO)
        for i, model in enumerate(self.models):
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._EBO[i])
            glUseProgram(model.shader)
            self.view_loc = glGetUniformLocation(model.shader, "view")
            glUniformMatrix4fv(self.view_loc, 1, GL_FALSE,
                               self.game.user.camera.view_matrix)

            self.model_loc = glGetUniformLocation(model.shader, "model")
            glUniformMatrix4fv(self.model_loc, 1, GL_FALSE,
                               self.rotate(0, 0, 0))

            self.projection_loc = glGetUniformLocation(
                model.shader, "projection")
            glUniformMatrix4fv(self.projection_loc, 1,
                               GL_FALSE, self.game.projection)
            glDrawElementsInstanced(
                GL_TRIANGLES, model.count, GL_UNSIGNED_INT, None, model.instancecount)
            glUseProgram(0)
        glBindVertexArray(0)

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = np.array(value, dtype=np.float32)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = np.array(value, dtype=np.float32)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = np.array(value, dtype=np.float32)

    def spin(self, 
                 x: float | int = 0, 
                 y: float | int = 0, 
                 z: float | int = 0):
        "旋转"
        self.rotation = self.rotation + np.array([x, y, z], dtype=np.float32)
        rot_x = pyrr.matrix44.create_from_x_rotation(self.rotation[0])
        rot_y = pyrr.matrix44.create_from_y_rotation(self.rotation[1])
        rot_z = pyrr.matrix44.create_from_z_rotation(self.rotation[2])
        return rot_z @ rot_y @ rot_x

    def rotate(self, 
                 x: float | int = 0, 
                 y: float | int = 0, 
                 z: float | int = 0):
        "设置旋转"
        self.rotation = np.array([x, y, z], dtype=np.float32)
        rot_x = pyrr.matrix44.create_from_x_rotation(self.rotation[0])
        rot_y = pyrr.matrix44.create_from_y_rotation(self.rotation[1])
        rot_z = pyrr.matrix44.create_from_z_rotation(self.rotation[2])
        return rot_z @ rot_y @ rot_x

    def resize(self, 
                 x: float | int = 0, 
                 y: float | int = 0, 
                 z: float | int = 0):
        "设置尺寸"
        self.scale = np.array([x, y, z], dtype=np.float32)
        scale = pyrr.matrix44.create_from_scale(self.scale)
        return scale

    def zoom(self, 
                 x: float | int = 0, 
                 y: float | int = 0, 
                 z: float | int = 0):
        "缩放"
        self.scale = self.scale + np.array([x, y, z], dtype=np.float32)
        scale = pyrr.matrix44.create_from_scale(self.scale)
        return scale

    def move(self, 
                 x: float | int = 0, 
                 y: float | int = 0, 
                 z: float | int = 0):
        "转移"
        self.position = self.position + np.array([x, y, z], dtype=np.float32)
        position = pyrr.matrix44.create_from_translation(self.position)
        return position

    def transfer(self,
                 x: float | int = 0,
                 y: float | int = 0,
                 z: float | int = 0):
        "移动"
        self.position = np.array([x, y, z], dtype=np.float32)
        position = pyrr.matrix44.create_from_translation(self.position)
        return position

    def bind_game(self, game: 'Game'):
        self.game = game
        return self

    def __call__(self, *args, **kwds):
        return self
    
    def __getitem__(self, index):
        return self.__flattened_models[index]

    class multiModels(object):

        class Models(object):

            def __init__(self, models: list['Model']) -> None:
                self.shader = compile_shader(type(models[0]).shader)
                self.__models = models

                self.indices: np.ndarray = models[0].indices
                self.count = len(models[0].indices)
                self.instancecount = len(models)

                self.vertices: np.ndarray = models[0].vertices
                self.colors: np.ndarray = np.array(
                    [model.colors for model in models], dtype=np.float32)

                self.positions: np.ndarray = np.array(
                    [model.position for model in models], dtype=np.float32)
                self.scales: np.ndarray = np.array(
                    [model.scale for model in models], dtype=np.float32)

                for model in models:
                    model.bind_scene(self)
                pass

            def __iter__(self):
                for model in self.__models:
                    yield model

            def __len__(self):
                return len(self.__models)

            def __getitem__(self, index):
                return self.__models[index]

            def __setitem__(self, key, value):
                self.__models[key] = value

            def __delitem__(self, key):
                del self.__models[key]

            def append(self, value: 'Model'):
                self.__models.append(value)

        def __init__(self, models: list['Model']) -> None:
            models.sort()  # 模型排序
            _model = Scene.multiModels.Models(models.copy())
            self.__models = [_model]  # 分类后的模型
            self.__models.pop()
            # 模型分类
            for i, model in enumerate(models[1:]):
                if isinstance(model, type(models[i])):  # 类型相同
                    _model.append(model)
                    if model is models[-1]:
                        self.__models.append(_model)
                else:
                    self.__models.append(_model)
                    _model = Scene.multiModels.Models([])
            del _model

        def __iter__(self):
            for models in self.__models:
                yield models

        def __len__(self):
            return len(self.__models)

        def __getitem__(self, index):
            return self.__models[index]

        def __setitem__(self, key, value):
            self.__models[key] = value

        def __delitem__(self, key):
            del self.__models[key]
