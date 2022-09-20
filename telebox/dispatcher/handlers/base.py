from abc import ABC, abstractmethod


class AbstractHandler(ABC):

    @abstractmethod
    def process(self, *args, **kwargs):
        pass

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__
