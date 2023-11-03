import abc

class Event(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def trigger(self):
        "触发器，必选"
        ...