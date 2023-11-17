from engine.const import *
from ..scene import Scene as parent


def __import():
    global Model
    from ..model import Model


class ModelSet(object):

    def __init__(self, models: list['Model'] = []) -> None:
        self.__models = models
        self.shaderPath: str = models[0].shader

        self.indices: np.ndarray = np.array(models[0].indices, dtype=np.int32)
        self.count = len(models[0].indices)
        self.instancecount = len(models)

        self.vertices: np.ndarray = np.array(
            models[0].vertices, dtype=np.float32)

        self.colors: np.ndarray = np.array(
            [model.colors for model in models], dtype=np.float32)
        self.positions: np.ndarray = np.array(
            [model.position for model in models], dtype=np.float32)
        self.scales: np.ndarray = np.array(
            [model.scale for model in models], dtype=np.float32)

    def append(self, value: 'Model'):
        self.__models.append(value)

    def export(self, path: os.PathLike = None, mode: str = 'get') -> str:
        keys = get_attributes(self)
        data = {}
        for key in keys:
            value = getattr(self, key)
            if isinstance(value, (list, tuple, int, float, str, bool)):
                data.__setitem__(key, value)
            elif isinstance(value, np.ndarray):
                value = value.tolist()
                data.__setitem__(key, value)
            else:
                continue
        if path is None and mode == 'get':
            return data
        elif mode == 'file':
            with open(path, 'w+', encoding='utf-8') as file:
                json.dump(data, file, sort_keys=True)


class Scene(parent):

    def __init__(self, name: str, models: list['Model']) -> None:
        self.name = name                 # 场景名称
        self.models = self.sort(models)  # 场景模型

    def sort(self, models: list['Model']):
        "整理场景模型集"
        modelset = ModelSet(models.copy()) # 模型集
        result = [modelset]                # 分类后的模型
        result.pop()
        
        "模型分类"
        for i, model in enumerate(models[1:]):
            if isinstance(model, type(models[i])):  # 类型相同
                modelset.append(model)
                if model is models[-1]:             # 如果当前模型是最后一个模型，则直接向结果追加模型集
                    result.append(modelset)
            else:
                result.append(modelset)
                modelset = ModelSet()
        del modelset
        return result

    def export(self, path: os.PathLike = None, mode: str = 'get') -> str:
        "导出3d场景"
        data = []
        for model in self.models:
            value = model.export()
            data.append(value)
        data = {
            'content': data,
            'name': self.name
        }
        if path is None and mode == 'get':
            return data
        elif mode == 'file':
            with open(path, 'w+', encoding='utf-8') as file:
                json.dump(data, file, sort_keys=True)
    
    def __iter__(self):
        for modelset in self.models:
            yield modelset

    def __len__(self):
        return len(self.models)

    def __getitem__(self, index):
        return self.models[index]

    def __setitem__(self, key, value):
        self.models[key] = value

    def __delitem__(self, key):
        del self.models[key]
