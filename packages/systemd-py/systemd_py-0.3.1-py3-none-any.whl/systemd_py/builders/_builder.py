"""
# Builder Base Class
"""

from typing import List
from abc import abstractmethod, ABC


class _Builder(ABC):
    @abstractmethod
    def build(self):
        """
        Builds the object
        """

        raise NotImplementedError

    def __call__(self):
        """
        Builds the object
        """

        self._check()
        return self.build()

    @property
    @abstractmethod
    def allowed_none_fields(self) -> List[str]:
        """
        Returns a list of fields that are allowed to be None
        """

        raise NotImplementedError

    def _make_dict(self) -> dict:
        """
        Returns a dict of the object
        """

        return {s: getattr(self, s) for s in self.__slots__}

    def _check(self):
        """
        if value is None and field is not allowed to be None, raise TypeError
        """

        for s in self.__slots__:
            if getattr(self, s) is ...:
                setattr(self, s, None)
            if getattr(self, s) in (None, '', [], (), {}, ..., Ellipsis) and s not in self.allowed_none_fields:
                raise TypeError(f'{s[1:]} is not allowed to be None')

    def __repr__(self):
        return f'{self.__class__.__name__}({self._make_dict()})'

    def __str__(self):
        return f'{self.__class__.__name__}({self._make_dict()})'
