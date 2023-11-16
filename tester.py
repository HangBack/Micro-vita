from typing import Any


class obj:

    def __init__(self) -> None:
        self.__list = [0, 1, 2, 3]

    def __getitem__(self, index):
        return self.__list[index]
        pass

print(obj()[1])