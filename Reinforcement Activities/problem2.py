# Evan-Soobin Jeon
# ejeon2@uci.edu
# problem2.py

class HashableByAttributes:
    def __hash__(self):
        attrs = tuple(
            (key, value) for key, value in self.__dict__.items()
            if isinstance(value, (int, float, str, tuple, bool, type(None)))
        )
        return hash(attrs)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__


class Person(HashableByAttributes):
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Coordinate(HashableByAttributes):
    def __init__(self, x, y, metadata=None):
        self.x = x
        self.y = y
        self.metadata = metadata
