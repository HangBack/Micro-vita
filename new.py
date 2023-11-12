class a(object):

    def __iter__(self):
        for i in [1, 2, 3]:
            yield i

class b(a):

    def __iter__(self):
        yield super().__iter__()
    
print([i for i in b()])