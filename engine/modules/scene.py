from engine.const import *

class Scene(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def export(self, path: os.PathLike = None, mode: str = 'get'):
        "导出场景"
        ...