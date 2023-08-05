from abc import ABC, abstractmethod


class Interactive(ABC):
    @abstractmethod
    def create(self):
        raise NotImplementedError

    @abstractmethod
    def ask_to_save(self):
        raise NotImplementedError

    def run(self):
        self.create()
        self.ask_to_save()
