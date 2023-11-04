class test:

    def __init__(self) -> None:
        self._a = [1, 2, 3]

    @property
    def a(self):
        return self._a
    
    @a.setter
    def a(self, value):
        self._a = value

t = test()
t.a[0] = 10
print(t.a)