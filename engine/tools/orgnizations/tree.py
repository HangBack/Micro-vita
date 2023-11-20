from engine.const import *


class Node:

    def __init__(self, data: Any) -> None:
        self._parent: Node
        self._left: Node   # 左节点
        self._right: Node  # 右节点
        self._children: list[Node] = []
        self._data = data
        self._visited: bool = False

    @property
    def visited(self) -> bool:
        "是否被访问"
        return self._visited

    @visited.setter
    def visited(self, value: bool) -> bool:
        "是否被访问"
        self._visited = value

    @property
    def parent(self) -> 'Node':
        "父节点"
        return self._parent

    @parent.setter
    def parent(self, node: 'Node'):
        """
        - node: `Node`，设置该节点的父亲节点
        """
        if isinstance(node, Node):
            self._parent = node
            self._parent.children.append(self)
        else:
            raise ValueError(f'希望赋值为一个"Node"而不是{type(node)}')

    @property
    def children(self):
        "子节点"
        return self._children

    @children.setter
    def children(self, value):
        "子节点"
        self._children = value

    @property
    def data(self):
        "节点数据"
        return self._data

    @data.setter
    def data(self, value: Any):
        "节点数据"
        self._data = value

    @property
    def type(self):
        "节点类型"
        return type(self._data)


class Tree:

    def __init__(self, node: Node, name: str = '无名树') -> None:
        """
        - node: `Node`, 传入任意一个节点，作为该树的根节点。
        - name: `str`, 树的名字，用于查询。
        """
        self.name: str = name
        self.root: Node = node
        self.__nodecount: int = 1

    @property
    def nodecount(self) -> int:
        return self.__nodecount

    """
    
    栈
    queue = [time1 -> a, time2 -> b...]
    以下循环：直到栈空
    栈出
    queue.popleft() 现在 queue 相当于 [time2 -> b, time3 -> c...]
    栈入
    queue.extend(nodeList) 现在 queue 相当于 [time2 -> b, time3 -> c...timeN1 -> Na, timeN2 -> Nb...]

    """

    def BFS(self, callback: Callable[[Node], bool] = lambda node: True) -> Node | None:
        """
        广度优先搜索（层次搜索）
        - callback: `Callable`, 用于判断node是否符合指定条件
        """
        visited = set()
        queue = deque([self.root])
        while queue:
            current_node = queue.popleft()
            
            if callback(current_node):
                return current_node  # 第一个符合条件的节点
            
            visited.add(current_node)

            queue.extend(child 
                         for child in current_node.children 
                         if child not in visited 
                            and 
                            child not in queue)
        return None  # 没有任何满足条件的节点

    def BFT(self, callback: Callable[[Node], bool] = lambda node: True) -> list[Node] | None:
        """
        广度优先遍历（层次遍历）
        - callback: `Callable`, 用于判断node是否符合指定条件
        """
        visited = set()
        queue = deque([self.root])
        result = []
        while queue:
            current_node = queue.popleft()

            if callback(current_node):
                result.append(current_node)  # 追加一个符合条件的节点
            
            visited.add(current_node)

            queue.extend(child 
                         for child in current_node.children 
                         if child not in visited 
                            and 
                            child not in queue)

        return result

    """
    
    递归
    从当前节点开始优先找子节点，子节点也优先找子节点，直到到底了都还没找到则返回父节点并找该节点的另一个子节点，以此类推

    """

    def DFS(self, node=None, callback: Callable[[Node], bool] = lambda node: True) -> Node | None:
        """
        深度优先搜索
        - node: `Node`, 传入的节点，默认为根节点
        - callback: `Callable`, 用于判断node是否符合指定条件
        """
        result = None
        if node is None:
            node = self.root

        if callback(node):
            return node  # 找到符合条件的节点
        
        node.visited = True
        for child in node.children:
            if not child.visited:
                result = self.DFS(child, callback)
            if result is not None:
                return result  # 在子树中找到符合条件的节点
        node.visited = False

        return None  # 在当前子树未找到符合条件的节点

    def DFT(self, node=None, callback: Callable[[Node], bool] = lambda node: True) -> list[Node]:
        """
        深度优先遍历
        - node: `Node`, 传入的节点，默认为根节点
        - callback: `Callable`, 用于判断node是否符合指定条件
        """
        result = None
        if node is None:
            node = self.root

        result = []

        if callback(node):
            result.append(node)  # 找到符合条件的节点
        
        node.visited = True
        for child in node.children:
            if not child.visited:
                current_node = self.DFT(child, callback)
                result.extend(current_node)
        node.visited = False

        return result
