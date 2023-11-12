import numpy as np

class Vector(object):

    def __init__(self, amount_tuple: tuple = None, *args) -> None:
        """
        Vector
        - positional_arguments
          - amount_tuple: tuple, accept a tuple.
        """
        if args:
            amount_tuple = (amount_tuple, *args)
        self.array = np.array(amount_tuple)
        self.tuple = amount_tuple

    def __str__(self) -> str:
        return f"Vector {tuple(self.array)}"
    
    def __iter__(self):
        for element in self.tuple:
            yield f"{type(element).__name__}({element})"

    def __len__(self):
        return len(self.tuple)

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(tuple(self.array + other.array))
        else:
            raise ValueError("You can only add a Vector to another Vector")
        
    def __mul__(self, other):
        def _opr(a, b):
            return Vector(tuple(a * b))
        
        try:
            return other.__mul__(other, self)
        except:
            if isinstance(other, Vector):
                return _opr(self.array, other.array)
            elif isinstance(other, (int, float)):
                return _opr(self.array, other)
            else:
                raise ValueError(f"can't multiply Vector by type '{type(other).__name__}'")