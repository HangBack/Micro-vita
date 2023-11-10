from const import *

def __import():
    global Model, Game
    from modules.model import Model
    from game import Game

class Scene:

    def __init__(self, models: list['Model'] | Callable) -> None:
        if callable(models):
            models: list['Model'] = models()
        self._VBO: list = []  # 顶点缓冲对象
        self._EBO: list = [] # 元素缓冲对象
        self.__models = models
        self._rotation = np.zeros(3, dtype=np.float32)
        self._scale = np.ones(3, dtype=np.float32)
        pass

    def init(self):
        self.models = self.multiModels(self.__models)
        for _ in self.models:
            self._VBO.append(glGenBuffers(1))
            self._EBO.append(glGenBuffers(1))
        self.load()
        return self

    def load(self):
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)
        for i in range(len(self._VBO)):
            VBO = self._VBO[i]
            EBO = self._EBO[i]
            for model in self.models:
                break
            glBindBuffer(GL_ARRAY_BUFFER, VBO)
            glBufferData(GL_ARRAY_BUFFER, model.vertices.nbytes + model.positions.nbytes + model.scales.nbytes + model.colors.nbytes,
                            None, GL_STATIC_DRAW)
            glBufferSubData(GL_ARRAY_BUFFER, 0,
                            model.vertices.nbytes, model.vertices)
            
            glBufferSubData(GL_ARRAY_BUFFER, model.vertices.nbytes,
                            model.positions.nbytes, model.positions)
            
            glBufferSubData(GL_ARRAY_BUFFER, model.vertices.nbytes + model.positions.nbytes,
                            model.scales.nbytes, model.scales) # 第二个参数是起始位，第三个参数是偏移量
            
            glBufferSubData(GL_ARRAY_BUFFER, model.vertices.nbytes + model.positions.nbytes + model.scales.nbytes,
                            model.colors.nbytes, model.colors)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, model.indices.nbytes,
                            model.indices, GL_STATIC_DRAW)
            glUseProgram(model.shader)
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT,
                                GL_FALSE, 12, ctypes.c_void_p(0))
            
            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, model.vertices.shape[1], GL_FLOAT,
                                GL_FALSE, model.vertices[1].nbytes, ctypes.c_void_p(model.vertices.nbytes))
            glVertexAttribDivisor(1, 1)

            glEnableVertexAttribArray(2)
            glVertexAttribPointer(2, model.positions.shape[1], GL_FLOAT,
                                GL_FALSE, model.positions[1].nbytes, ctypes.c_void_p(model.vertices.nbytes + model.positions.nbytes))
            glVertexAttribDivisor(2, 1)

            glEnableVertexAttribArray(3)
            glVertexAttribPointer(3, model.colors.shape[1], GL_FLOAT,
                                GL_FALSE, model.colors[0].nbytes * 8, ctypes.c_void_p(model.vertices.nbytes + model.positions.nbytes + model.scales.nbytes))
            glVertexAttribDivisor(3, 1)


            glBindBuffer(GL_ARRAY_BUFFER, 0)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
            glUseProgram(0)
        glBindVertexArray(0)
        return self

    def draw(self):
        glBindVertexArray(self.VAO)
        for i, model in enumerate(self.models):
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._EBO[i])
            glUseProgram(model.shader)
            self.view_loc = glGetUniformLocation(model.shader, "view")
            glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, self.game.user.camera.view_matrix)
            
            self.model_loc = glGetUniformLocation(model.shader, "model")
            glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.spin(0.01, 0.01, 0.01))
            glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.resize(-0.001, -0.001, -0.001))

            self.projection_loc = glGetUniformLocation(model.shader, "projection")
            glUniformMatrix4fv(self.projection_loc, 1, GL_FALSE, self.game.projection)
            glDrawElementsInstanced(GL_TRIANGLES, model.count, GL_UNSIGNED_INT, None, model.instancecount)
            glUseProgram(0)

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

    def spin(self, x: float | int = 0, y: float | int = 0, z: float | int = 0):
        self.rotation = self.rotation + np.array([x, y, z], dtype=np.float32)
        rot_x = pyrr.matrix44.create_from_x_rotation(self.rotation[0])
        rot_y = pyrr.matrix44.create_from_y_rotation(self.rotation[1])
        rot_z = pyrr.matrix44.create_from_z_rotation(self.rotation[2])
        return rot_z @ rot_y @ rot_x

    def rotate(self, x: float | int = 0, y: float | int = 0, z: float | int = 0):
        self.rotation = np.array([x, y, z], dtype=np.float32)
        rot_x = pyrr.matrix44.create_from_x_rotation(self.rotation[0])
        rot_y = pyrr.matrix44.create_from_y_rotation(self.rotation[1])
        rot_z = pyrr.matrix44.create_from_z_rotation(self.rotation[2])
        return rot_z @ rot_y @ rot_x

    def resize(self, x: float | int = 0, y: float | int = 0, z: float | int = 0):
        self.scale = self.scale + np.array([x, y, z], dtype=np.float32)
        scale = pyrr.matrix44.create_from_scale(self.scale)
        return scale

    def zoom(self, x: float | int = 0, y: float | int = 0, z: float | int = 0):
        self.scale = self.scale * np.array([x, y, z], dtype=np.float32)
        scale = pyrr.matrix44.create_from_scale(self.scale)
        return scale

    def bind_game(self, game: 'Game'):
        self.game = game
        return self


    class multiModels(object):
    

        class Models(object):

            def __init__(self, models: list['Model']) -> None:
                self.shader = compile_shader(type(models[0]).shader)
                self.__models = models
                self.vertices: np.ndarray = models[0].vertices
                self.indices: np.ndarray = models[0].indices
                self.count = len(models[0].indices)
                self.instancecount = len(models)
                self.positions: np.ndarray = np.array([model.position for model in models], dtype=np.float32)
                self.colors: np.ndarray = np.array([model.color for model in models], dtype=np.float32)
                self.colors = self.colors.reshape(len(self.colors) * self.colors.shape[1], self.colors.shape[2])
                self.scales: np.ndarray = np.array([model.scale for model in models], dtype=np.float32)
                for model in models:
                    model.bind_scene(self)
                pass

            def __iter__(self):
                for model in self.__models:
                    yield model

            def __len__(self):
                return len(self.__models)

            def append(self, value: 'Model'):
                self.__models.append(value)

        def __init__(self, models: list['Model']) -> None:
            models.sort() # 模型排序
            _model = self.Models(models.copy())
            self.__models = [_model]  # 分类后的模型
            self.__models.pop()
            # 模型分类
            for i, model in enumerate(models[1:]):
                if isinstance(model, type(models[i])): # 类型相同
                    _model.append(model)
                    if model is models[-1]:
                        self.__models.append(_model)
                else:
                    self.__models.append(_model)
                    _model = self.Models([])
            del _model
        
        def __iter__(self):
            for models in self.__models:
                yield models

        def __len__(self):
            return len(self.__models)