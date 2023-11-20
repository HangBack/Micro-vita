from engine.tools.orgnizations import Node, Tree
import time

root = Node(0)
a = Node(123)
b = Node(456)
c = Node(789)
d = Node(111)
e = Node(222)
f = Node(333)

b.parent = a
a.parent = c
c.parent = b

# a -> b
# |    |
# |----c

c.parent = root

tree = Tree(root, '你好')


s = time.time()
for _ in range(100000):
    tree.BFS(callback=lambda x: x.data == 1)
print(time.time() - s)