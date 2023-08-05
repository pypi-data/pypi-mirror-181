from enum import Enum as _Enum


class Enum(_Enum):
    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        if isinstance(other, Enum):
            return self.value == other.value

        raise TypeError(f"Cannot compare {self.__class__.__name__} with {other.__class__.__name__}")
