from ..tree import Tree
from ..tree import Node

class Octree(Tree):
    
    def __init__(self, data, name: str = '无名八叉树') -> None:
        """
        - data: `object`, 传入任意一个对象，作为该八叉树的根节点。
        - name: `str`, 树的名字，用于查询。
        """
        super().__init__(data, name)