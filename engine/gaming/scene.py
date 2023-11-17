from engine.const import *


def __import():
    global Model, Game, ShaderProgram
    from modules.model import Model
    from game import Game
    from OpenGL.GL.shaders import ShaderProgram


class Scene:

    def __init__(self, path: os.PathLike) -> None:
        self._VBO: list = []  # 顶点缓冲对象
        self._EBO: list = []  # 元素缓冲对象
        self._IBO: list = []  # 实例缓冲对象
        self.scene_path = path + '.json'
        self._position = np.zeros(3, dtype=np.float32)
        self._rotation = np.zeros(3, dtype=np.float32)
        self._scale = np.ones(3, dtype=np.float32)

    def init(self):
        with open(self.scene_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.name = data['name']
            self.models: list[ModelSet] = []
            for modelset in data['content']:
                self.models.append(ModelSet(**modelset))
        file.close()
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

    def render(self):
        "渲染场景"
        glEnable(GL_LIGHTING)
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
        glDisable(GL_LIGHTING)

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

    def export(self, path: os.PathLike = None):
        "导出场景"
        start = time.time()
        if path is None:
            path = self.scene_path
        with open(path, 'w+', encoding='utf-8') as file:
            data = []
            for modelset in self.models:
                data.append(modelset.export())
            data = {
                'content': data,
                'name': self.name
            }
            json.dump(data, file, sort_keys=True)
        file.close()
        end = time.time()
        duration = end - start
        logging.info(f"保存“{self.name}”耗时：{duration}s")

    def __call__(self, *args, **kwds):
        return self

    def __getitem__(self, index):
        return self.__flattened_models[index]

class ModelSet(object):

    def __init__(self,**kwargs) -> None:

        self.shaderPath: str = kwargs['shaderPath']
        self.shader: 'ShaderProgram' = compile_shader(self.shaderPath)

        self.indices: np.ndarray = np.array(
            kwargs['indices'], dtype=np.int32)
        self.count = kwargs['count']
        self.instancecount = kwargs['instancecount']

        self.vertices: np.ndarray = np.array(
            kwargs['vertices'], dtype=np.float32)
        self.colors: np.ndarray = np.array(
            kwargs['colors'], dtype=np.float32)

        self.positions: np.ndarray = np.array(
            kwargs['positions'], dtype=np.float32)
        self.scales: np.ndarray = np.array(
            kwargs['scales'], dtype=np.float32)

    def export(self) -> str:
        keys = get_attributes(self)
        data = {}
        for key in keys:
            value = getattr(self, key)
            if isinstance(value, (list, tuple, int, float, str, bool)):
                data.__setitem__(key, value)
            elif isinstance(value, np.ndarray):
                value = value.tolist()
                data.__setitem__(key, value)
        return data
