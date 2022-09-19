from abc import ABC, abstractmethod


class AbstractErrorHandler(ABC):

    @abstractmethod
    def process_error(self, error, event):
        pass

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__
